from collections import defaultdict

import polars as pl

from vnpy.trader.object import BarData, TradeData
from vnpy.trader.constant import Direction
from vnpy.trader.utility import round_to

from vnpy.alpha import AlphaStrategy


class EquityDemoStrategy(AlphaStrategy):
    """Equity Long-Only Demo Strategy"""

    top_k: int = 50                 # Maximum number of stocks to hold
    n_drop: int = 5                 # Number of stocks to sell each time
    min_days: int = 3               # Minimum holding period in days
    cash_ratio: float = 0.95        # Cash utilization ratio
    min_volume: int = 100           # Minimum trading unit
    open_rate: float = 0.0005       # Opening commission rate
    close_rate: float = 0.0015      # Closing commission rate
    min_commission: int = 5         # Minimum commission value
    price_add: float = 0.05         # Order price adjustment ratio

    def on_init(self) -> None:
        """Strategy initialization callback"""
        # Dictionary to track stock holding days
        self.holding_days: defaultdict = defaultdict(int)

        self.write_log("Strategy initialized")

    def on_trade(self, trade: TradeData) -> None:
        """
        Trade execution callback
        
        A股特定处理：
        - 买入时记录买入日期（用于T+1规则）
        - 卖出时清除买入日期记录
        """
        # A股T+1规则：记录买入日期
        if trade.direction == Direction.LONG and trade.offset.value == "OPEN":
            # 买入开仓：记录买入日期
            self.buy_dates[trade.vt_symbol] = trade.datetime or datetime.now()
            self.write_log(f"A股买入记录: {trade.vt_symbol} 买入日期: {self.buy_dates[trade.vt_symbol]}")
        
        # Remove holding days record when selling
        if trade.direction == Direction.SHORT:
            self.holding_days.pop(trade.vt_symbol, None)
            # A股T+1规则：卖出时清除买入日期记录
            if trade.vt_symbol in self.buy_dates:
                del self.buy_dates[trade.vt_symbol]

    def on_bars(self, bars: dict[str, BarData]) -> None:
        """K-line slice callback"""
        # Get the latest signals and sort them
        last_signal: pl.DataFrame = self.get_signal()
        last_signal = last_signal.sort("signal", descending=True)

        # Get position symbols and update holding days
        pos_symbols: list[str] = [vt_symbol for vt_symbol, pos in self.pos_data.items() if pos]

        for vt_symbol in pos_symbols:
            self.holding_days[vt_symbol] += 1

        # Generate sell list
        active_symbols: set[str] = set(last_signal["vt_symbol"][:self.top_k])                         # Extract symbols with highest signals
        active_symbols.update(pos_symbols)                                                            # Merge with currently held symbols
        active_df: pl.DataFrame = last_signal.filter(pl.col("vt_symbol").is_in(active_symbols))       # Filter signals for these symbols

        component_symbols: set[str] = set(last_signal["vt_symbol"])                 # Extract current index component symbols
        sell_symbols: set[str] = set(pos_symbols).difference(component_symbols)     # Sell positions not in components

        for vt_symbol in active_df["vt_symbol"][-self.n_drop:]:                     # Iterate through lowest signal portion
            if vt_symbol in pos_symbols:                                            # If the contract is in current positions
                sell_symbols.add(vt_symbol)                                         # Add it to sell list

        # Generate buy list
        buyable_df: pl.DataFrame = last_signal.filter(~pl.col("vt_symbol").is_in(pos_symbols))  # Filter contracts available for purchase
        buy_quantity: int = len(sell_symbols) + self.top_k - len(pos_symbols)                   # Calculate number of contracts to buy
        buy_symbols: list = list(buyable_df[:buy_quantity]["vt_symbol"])                        # Select buy contract code list

        # Sell rebalancing
        cash: float = self.get_cash_available()                     # Get available cash after yesterday's settlement

        for vt_symbol in sell_symbols:
            if self.holding_days[vt_symbol] < self.min_days:        # Check if holding period exceeds threshold
                continue

            bar: BarData | None = bars.get(vt_symbol)               # Get current price of the contract
            if not bar:
                continue
            
            # A股涨跌停判断：跌停时不能卖出
            if self.is_limit_down(bar):
                self.write_log(f"A股跌停，无法卖出: {vt_symbol}")
                continue
            
            # A股T+1规则检查：当日买入的股票不能卖出
            current_date = bar.datetime or datetime.now()
            if not self.can_sell(vt_symbol, current_date):
                self.write_log(f"A股T+1规则，当日买入不能卖出: {vt_symbol}")
                continue
            
            sell_price: float = bar.close_price

            sell_volume: float = self.get_pos(vt_symbol)            # Get current holding volume
            # A股最小交易单位：确保是100的整数倍
            sell_volume = round_to(sell_volume, self.min_volume)
            if sell_volume <= 0:
                continue

            self.set_target(vt_symbol, target=0)                    # Set target volume to 0

            turnover: float = sell_price * sell_volume                                  # Calculate selling turnover
            cost: float = max(turnover * self.close_rate, self.min_commission)          # Calculate selling cost
            cash += turnover - cost                                                     # Update available cash

        # Buy rebalancing
        if buy_symbols:
            buy_value: float = cash * self.cash_ratio / len(buy_symbols)        # Calculate investment amount per contract

            for vt_symbol in buy_symbols:
                bar: BarData = bars[vt_symbol]
                buy_price: float = bar.close_price                  # Get current price of the contract
                if not buy_price:
                    continue
                
                # A股涨跌停判断：涨停时不能买入
                if self.is_limit_up(bar):
                    self.write_log(f"A股涨停，无法买入: {vt_symbol}")
                    continue

                buy_volume: float = round_to(buy_value / buy_price, self.min_volume)    # Calculate volume to buy
                # A股最小交易单位：确保是100的整数倍
                if buy_volume < self.min_volume:
                    continue

                self.set_target(vt_symbol, buy_volume)                          # Set target holding volume

        # Execute trading
        self.execute_trading(bars, price_add=self.price_add)
