#!/usr/bin/env python3
"""
Mac系统启动测试脚本

用于测试VNPY在Mac系统上的基础功能：
1. 测试主窗口启动
2. 测试引擎启动
"""

import sys
import platform
from pathlib import Path

# 添加vnpy路径
sys.path.insert(0, str(Path(__file__).parent))

def test_platform_detection():
    """测试平台检测功能"""
    print("=" * 60)
    print("测试1: 平台检测功能")
    print("=" * 60)
    
    try:
        from vnpy.trader.platform_utils import is_mac_system, is_windows_system, get_mac_arch
        
        print(f"当前系统: {platform.system()}")
        print(f"系统架构: {platform.machine()}")
        print(f"is_mac_system(): {is_mac_system()}")
        print(f"is_windows_system(): {is_windows_system()}")
        
        if is_mac_system():
            print(f"Mac架构: {get_mac_arch()}")
            print("✓ 平台检测功能正常")
        else:
            print("⚠ 当前不在Mac系统上")
        
        return True
    except Exception as e:
        print(f"✗ 平台检测功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qt_app_creation():
    """测试Qt应用创建"""
    print("\n" + "=" * 60)
    print("测试2: Qt应用创建")
    print("=" * 60)
    
    try:
        from vnpy.trader.ui.qt import create_qapp
        
        print("正在创建Qt应用...")
        qapp = create_qapp("VeighNa Trader Test")
        print("✓ Qt应用创建成功")
        print(f"应用对象: {qapp}")
        
        # 不执行exec()，只测试创建
        return True, qapp
    except Exception as e:
        print(f"✗ Qt应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_engine_startup():
    """测试引擎启动"""
    print("\n" + "=" * 60)
    print("测试3: 引擎启动")
    print("=" * 60)
    
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        
        print("正在创建事件引擎...")
        event_engine = EventEngine()
        print("✓ 事件引擎创建成功")
        
        print("正在创建主引擎...")
        main_engine = MainEngine(event_engine)
        print("✓ 主引擎创建成功")
        print(f"主引擎对象: {main_engine}")
        print(f"事件引擎状态: {event_engine._active}")
        
        # 清理
        main_engine.close()
        event_engine.stop()
        print("✓ 引擎清理完成")
        
        return True
    except Exception as e:
        print(f"✗ 引擎启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_window_creation():
    """测试主窗口创建（不显示）"""
    print("\n" + "=" * 60)
    print("测试4: 主窗口创建")
    print("=" * 60)
    
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.ui.qt import create_qapp
        from vnpy.trader.ui.mainwindow import MainWindow
        
        print("正在创建Qt应用...")
        qapp = create_qapp("VeighNa Trader Test")
        
        print("正在创建事件引擎...")
        event_engine = EventEngine()
        
        print("正在创建主引擎...")
        main_engine = MainEngine(event_engine)
        
        print("正在创建主窗口...")
        main_window = MainWindow(main_engine, event_engine)
        print("✓ 主窗口创建成功")
        print(f"窗口标题: {main_window.windowTitle()}")
        print(f"窗口对象: {main_window}")
        
        # 清理
        main_window.close()
        main_engine.close()
        event_engine.stop()
        print("✓ 主窗口清理完成")
        
        return True
    except Exception as e:
        print(f"✗ 主窗口创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("VNPY Mac系统基础功能测试")
    print("=" * 60)
    print(f"Python版本: {sys.version}")
    print(f"系统信息: {platform.platform()}")
    print()
    
    results = []
    
    # 测试1: 平台检测
    results.append(("平台检测", test_platform_detection()))
    
    # 测试2: Qt应用创建
    qt_success, qapp = test_qt_app_creation()
    results.append(("Qt应用创建", qt_success))
    
    # 测试3: 引擎启动
    results.append(("引擎启动", test_engine_startup()))
    
    # 测试4: 主窗口创建
    results.append(("主窗口创建", test_main_window_creation()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！Mac系统基础功能正常")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
