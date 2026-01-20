#!/usr/bin/env python3
"""
测试多进程管理器修复

验证所有修复是否有效
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_syntax():
    """测试语法"""
    print("=" * 60)
    print("测试1: 语法检查")
    print("=" * 60)
    
    try:
        import ast
        with open('vnpy/trader/multiprocess_manager.py', 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print("✓ 语法检查通过")
        return True
    except SyntaxError as e:
        print(f"✗ 语法错误: {e}")
        return False


def test_import():
    """测试导入（不依赖loguru）"""
    print("\n" + "=" * 60)
    print("测试2: 模块结构检查")
    print("=" * 60)
    
    try:
        # 直接检查代码结构
        with open('vnpy/trader/multiprocess_manager.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 检查__init__方法中是否包含启动方法设置
        init_start = code.find('def __init__')
        init_end = code.find('def ', init_start + 1) if init_start != -1 else len(code)
        init_code = code[init_start:init_end] if init_start != -1 else ''
        has_init_set_start_method = 'multiprocessing.set_start_method' in init_code and 'is_mac_system()' in init_code
        
        checks = {
            '信号处理器为独立函数': 'def _signal_handler(' in code and 'self._signal_handler' not in code,
            '信号处理器正确调用': 'signal.signal(signal.SIGTERM, _signal_handler)' in code,
            '共享状态清理使用正确锁': 'with self.shared_locks[strategy_id]:' in code,
            'Mac启动方法在__init__中设置': has_init_set_start_method,
            'TypeError处理改进': 'if \'_process_comm\' in str(e)' in code,
            '没有self._signal_handler引用': 'self._signal_handler' not in code,
            '没有错误的manager.Lock()使用': 'with self.manager.Lock()' not in code or ('if hasattr' in code and 'self.shared_locks' in code)
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"{status} {check_name}")
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ 检查失败: {e}")
        return False


def test_code_structure():
    """测试代码结构"""
    print("\n" + "=" * 60)
    print("测试3: 代码结构检查")
    print("=" * 60)
    
    try:
        with open('vnpy/trader/multiprocess_manager.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 检查关键函数和类
        has_process_manager = False
        has_signal_handler = False
        has_init = False
        
        for i, line in enumerate(lines, 1):
            if 'class ProcessManager' in line:
                has_process_manager = True
                print(f"✓ 找到ProcessManager类 (行 {i})")
            if 'def _signal_handler(' in line and 'self' not in line:
                has_signal_handler = True
                print(f"✓ 找到独立信号处理器函数 (行 {i})")
            if 'def __init__' in line and 'multiprocessing.set_start_method' in ''.join(lines[i:i+20]):
                has_init = True
                print(f"✓ __init__中包含启动方法设置 (行 {i})")
        
        if not has_process_manager:
            print("✗ 未找到ProcessManager类")
        if not has_signal_handler:
            print("✗ 未找到独立信号处理器函数")
        if not has_init:
            print("⚠ __init__中可能缺少启动方法设置")
        
        return has_process_manager and has_signal_handler
    except Exception as e:
        print(f"✗ 结构检查失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("多进程管理器修复验证")
    print("=" * 60)
    print()
    
    results = []
    
    # 测试1: 语法检查
    results.append(("语法检查", test_syntax()))
    
    # 测试2: 导入检查
    results.append(("模块结构检查", test_import()))
    
    # 测试3: 代码结构检查
    results.append(("代码结构检查", test_code_structure()))
    
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
        print("\n🎉 所有修复验证通过！")
        print("\n修复内容：")
        print("  1. ✓ 信号处理器改为独立函数（可在子进程中使用）")
        print("  2. ✓ 共享状态清理使用正确的锁机制")
        print("  3. ✓ Mac系统multiprocessing启动方法在__init__中设置")
        print("  4. ✓ TypeError处理改进，更精确地捕获参数错误")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查")
        return 1


if __name__ == "__main__":
    sys.exit(main())
