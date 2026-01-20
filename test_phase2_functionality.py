"""
阶段二功能测试脚本

测试所有阶段二创建的核心模块的实际功能，验证关键方法是否正常工作。
"""

import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_optimization_metrics():
    """测试优化指标模块"""
    print("\n测试: OptimizationMetrics")
    print("-" * 60)
    try:
        from vnpy.trader.optimization_metrics import OptimizationMetrics
        
        metrics = OptimizationMetrics()
        
        # 测试数据
        returns = [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.01, 0.02]
        equity_curve = [100, 101, 99, 102, 101, 103, 102, 104]
        
        # 测试各种指标
        sharpe = metrics.calculate_sharpe_ratio(returns)
        sortino = metrics.calculate_sortino_ratio(returns)
        r_cubed = metrics.calculate_r_cubed(returns)
        max_dd = metrics.calculate_max_drawdown(equity_curve)
        win_rate = metrics.calculate_win_rate(returns)
        profit_factor = metrics.calculate_profit_factor(returns)
        all_metrics = metrics.calculate_all_metrics(returns, equity_curve)
        
        print(f"  ✓ Sharpe Ratio: {sharpe:.4f}")
        print(f"  ✓ Sortino Ratio: {sortino:.4f}")
        print(f"  ✓ R-Cubed: {r_cubed:.4f}")
        print(f"  ✓ Max Drawdown: {max_dd['max_drawdown_pct']:.2%}")
        print(f"  ✓ Win Rate: {win_rate:.2%}")
        print(f"  ✓ Profit Factor: {profit_factor:.4f}")
        print(f"  ✓ All Metrics: {len(all_metrics)} 个指标")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_filter():
    """测试数据过滤模块"""
    print("\n测试: DataFilter")
    print("-" * 60)
    try:
        from vnpy.trader.data_filter import DataFilter
        from vnpy.trader.object import TickData, BarData
        from vnpy.trader.constant import Exchange
        from datetime import datetime
        
        filter_obj = DataFilter()
        
        # 创建测试数据
        tick = TickData(
            gateway_name="test",
            symbol="000001",
            exchange=Exchange.SSE,
            datetime=datetime(2024, 1, 15, 10, 30, 0)  # 交易时间内
        )
        
        bar = BarData(
            gateway_name="test",
            symbol="000001",
            exchange=Exchange.SSE,
            datetime=datetime(2024, 1, 15, 10, 30, 0),
            interval=None
        )
        
        # 测试过滤
        is_trading = filter_obj.is_trading_time(tick.datetime)
        filtered_tick = filter_obj.filter_tick(tick)
        filtered_bar = filter_obj.filter_bar(bar)
        
        print(f"  ✓ 交易时间检查: {is_trading}")
        print(f"  ✓ Tick过滤: {filtered_tick is not None}")
        print(f"  ✓ Bar过滤: {filtered_bar is not None}")
        
        stats = filter_obj.get_filter_stats()
        print(f"  ✓ 过滤统计: {stats}")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_risk_manager():
    """测试增强型风险控制管理器"""
    print("\n测试: EnhancedRiskManager")
    print("-" * 60)
    try:
        from vnpy.trader.enhanced_risk_manager import EnhancedRiskManager
        from vnpy.trader.object import OrderRequest
        from vnpy.trader.constant import Direction, Exchange
        
        risk_mgr = EnhancedRiskManager()
        
        # 设置限制
        risk_mgr.set_order_rate_limit(10, 1.0)
        risk_mgr.set_cancel_ratio_limit(0.5)
        risk_mgr.set_position_limit("000001.SSE", 1000.0)
        
        # 创建订单请求
        req = OrderRequest(
            symbol="000001",
            exchange=Exchange.SSE,
            direction=Direction.LONG,
            offset=None,
            type=None,
            volume=100,
            price=10.0
        )
        
        # 测试检查
        passed, error = risk_mgr.check_order_request(req, current_position=0.0)
        print(f"  ✓ 订单检查: {passed}, 错误: {error if not passed else '无'}")
        
        # 测试速率检查
        for i in range(5):
            passed, error = risk_mgr.check_order_rate("000001.SSE")
            if not passed:
                print(f"  ✓ 速率限制生效: {error}")
                break
        
        # 获取统计
        stats = risk_mgr.get_risk_stats("000001.SSE")
        print(f"  ✓ 风控统计: {stats}")
        
        config = risk_mgr.get_config()
        print(f"  ✓ 配置项数: {len(config)}")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_status_monitor():
    """测试状态监控模块"""
    print("\n测试: StatusMonitor")
    print("-" * 60)
    try:
        from vnpy.trader.status_monitor import StatusMonitor
        from vnpy.trader.object import PositionData, LogData
        from vnpy.trader.constant import Direction, Exchange
        from datetime import datetime
        
        monitor = StatusMonitor()
        
        # 更新策略状态
        monitor.update_strategy_status("test_strategy", "running", {"param1": 10})
        status = monitor.get_strategy_status("test_strategy")
        print(f"  ✓ 策略状态: {status.get('status', 'N/A')}")
        
        # 记录持仓变动
        position = PositionData(
            gateway_name="test",
            symbol="000001",
            exchange=Exchange.SSE,
            direction=Direction.LONG,
            volume=100,
            frozen=0,
            price=10.0,
            pnl=0.0,
            yd_volume=0
        )
        monitor.record_position_change("000001.SSE", position)
        history = monitor.get_position_history("000001.SSE")
        print(f"  ✓ 持仓历史: {len(history)} 条记录")
        
        # 记录日志
        log = LogData(
            gateway_name="test",
            msg="测试日志"
        )
        monitor.record_log(log)
        logs = monitor.get_recent_logs(10)
        print(f"  ✓ 最近日志: {len(logs)} 条")
        
        # 获取监控摘要
        summary = monitor.get_monitoring_summary()
        print(f"  ✓ 监控摘要: {summary}")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_optimization_visualization():
    """测试优化可视化模块"""
    print("\n测试: OptimizationVisualization")
    print("-" * 60)
    try:
        from vnpy.trader.optimization_visualization import OptimizationVisualization
        
        viz = OptimizationVisualization()
        
        # 测试数据
        param1_values = [5, 10, 15, 20]
        param2_values = [0.1, 0.2, 0.3]
        metric_values = [
            [0.5, 0.6, 0.7],
            [0.6, 0.7, 0.8],
            [0.7, 0.8, 0.9],
            [0.6, 0.7, 0.8]
        ]
        
        # 测试热力图（不保存文件）
        result = viz.plot_heatmap(
            "参数1", param1_values,
            "参数2", param2_values,
            metric_values,
            output_path=None
        )
        print(f"  ✓ 热力图生成: {'成功' if result is None else '失败'}")
        
        # 测试参数曲线
        param_values = [5, 10, 15, 20]
        metric_vals = [0.5, 0.7, 0.8, 0.6]
        result = viz.plot_parameter_curve(
            "参数", param_values, metric_vals,
            output_path=None
        )
        print(f"  ✓ 参数曲线生成: {'成功' if result is None else '失败'}")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("阶段二功能测试")
    print("=" * 60)
    
    tests = [
        ("优化指标", test_optimization_metrics),
        ("数据过滤", test_data_filter),
        ("风险控制", test_enhanced_risk_manager),
        ("状态监控", test_status_monitor),
        ("优化可视化", test_optimization_visualization),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} 测试异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\n通过: {passed}/{total}")
    
    if passed == total:
        print("\n✓ 所有功能测试通过！")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
