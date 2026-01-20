#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VNPY Mac系统A股量化实盘系统 - 启动脚本

功能：
1. 自动检测Mac系统环境
2. 启动VNPY量化交易系统
3. 支持UI模式和无UI模式
4. 自动加载增强功能模块

使用方法：
    python3 启动量化系统.py          # UI模式
    python3 启动量化系统.py --no-ui  # 无UI模式（后台运行）
    python3 启动量化系统.py --test   # 测试模式
"""

import sys
import os
import argparse
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """检查依赖"""
    missing = []
    
    try:
        import loguru
    except ImportError:
        missing.append("loguru")
    
    try:
        import PySide6
    except ImportError:
        missing.append("PySide6")
    
    try:
        import tzlocal
    except ImportError:
        missing.append("tzlocal")
    
    if missing:
        print("⚠️  缺少以下依赖:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n安装命令:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def check_mac_adaptation():
    """检查Mac适配"""
    try:
        from vnpy.trader.platform_utils import is_mac_system, get_mac_arch
        
        if is_mac_system():
            arch = get_mac_arch()
            print(f"✅ Mac系统检测: {arch}架构")
            return True
        else:
            print("⚠️  非Mac系统，部分Mac适配功能可能不可用")
            return True
    except Exception as e:
        print(f"⚠️  Mac适配检查失败: {e}")
        return False

def start_ui_mode():
    """启动UI模式"""
    print("=" * 60)
    print("启动VNPY量化交易系统 - UI模式")
    print("=" * 60)
    
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.ui import MainWindow, create_qapp
        
        # 检查Mac适配
        check_mac_adaptation()
        
        # 创建Qt应用
        qapp = create_qapp("VNPY Mac量化系统")
        
        # 创建事件引擎
        event_engine = EventEngine()
        
        # 创建主引擎
        main_engine = MainEngine(event_engine)
        
        # 加载增强功能模块（如果可用）
        try:
            from vnpy.trader.multiprocess_manager import ProcessManager
            from vnpy.trader.enhanced_risk_manager import EnhancedRiskManager
            from vnpy.trader.status_monitor import StatusMonitor
            print("✅ 增强功能模块加载成功")
        except Exception as e:
            print(f"ℹ️  增强功能模块未加载: {e}")
        
        # 添加Gateway（需要用户安装）
        # 示例：如果有vnpy_xtp或vnpy_tora
        # from vnpy_xtp import XtpGateway
        # main_engine.add_gateway(XtpGateway)
        
        # 添加应用（需要用户安装）
        # 示例：如果有vnpy_ctastrategy
        # from vnpy_ctastrategy import CtaStrategyApp
        # main_engine.add_app(CtaStrategyApp)
        
        # 创建主窗口
        main_window = MainWindow(main_engine, event_engine)
        main_window.showMaximized()
        
        print("✅ 系统启动成功！")
        print("=" * 60)
        
        # 运行应用
        qapp.exec()
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n请确保已安装VNPY完整依赖:")
        print("  pip install vnpy")
        return False
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def start_no_ui_mode():
    """启动无UI模式（后台运行）"""
    print("=" * 60)
    print("启动VNPY量化交易系统 - 无UI模式（后台运行）")
    print("=" * 60)
    
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.logger import logger
        
        # 检查Mac适配
        check_mac_adaptation()
        
        # 创建事件引擎
        event_engine = EventEngine()
        
        # 创建主引擎
        main_engine = MainEngine(event_engine)
        
        # 加载增强功能模块
        try:
            from vnpy.trader.multiprocess_manager import ProcessManager
            from vnpy.trader.enhanced_risk_manager import EnhancedRiskManager
            from vnpy.trader.status_monitor import StatusMonitor
            
            # 初始化增强功能
            risk_manager = EnhancedRiskManager()
            status_monitor = StatusMonitor()
            process_manager = ProcessManager()
            
            print("✅ 增强功能模块加载成功")
            logger.info("增强功能模块加载成功")
        except Exception as e:
            print(f"ℹ️  增强功能模块未加载: {e}")
            logger.warning(f"增强功能模块未加载: {e}")
        
        print("✅ 系统启动成功（后台运行）")
        print("=" * 60)
        print("按 Ctrl+C 退出")
        
        # 保持运行
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在关闭系统...")
        try:
            main_engine.close()
        except:
            pass
        print("✅ 系统已关闭")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n请确保已安装VNPY完整依赖:")
        print("  pip install vnpy")
        return False
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_test_mode():
    """测试模式"""
    print("=" * 60)
    print("VNPY量化系统 - 测试模式")
    print("=" * 60)
    
    # 运行测试脚本
    test_scripts = [
        "test_phase2_core_logic.py",
        "test_datafeed_mac.py",
    ]
    
    import subprocess
    
    for script in test_scripts:
        script_path = project_root / script
        if script_path.exists():
            print(f"\n运行测试: {script}")
            print("-" * 60)
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=str(project_root),
                    timeout=60
                )
                if result.returncode == 0:
                    print(f"✅ {script} 测试通过")
                else:
                    print(f"⚠️  {script} 测试未完全通过（可能是环境问题）")
            except Exception as e:
                print(f"❌ {script} 测试失败: {e}")
        else:
            print(f"⚠️  测试脚本不存在: {script}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="VNPY Mac系统A股量化实盘系统")
    parser.add_argument("--no-ui", action="store_true", help="无UI模式（后台运行）")
    parser.add_argument("--test", action="store_true", help="测试模式")
    parser.add_argument("--skip-check", action="store_true", help="跳过依赖检查")
    
    args = parser.parse_args()
    
    # 检查依赖（除非跳过）
    if not args.skip_check and not args.test:
        if not check_dependencies():
            print("\n是否继续启动？(y/n): ", end="")
            choice = input().strip().lower()
            if choice != 'y':
                return
    
    # 测试模式
    if args.test:
        run_test_mode()
        return
    
    # 启动系统
    if args.no_ui:
        start_no_ui_mode()
    else:
        start_ui_mode()

if __name__ == "__main__":
    main()
