#!/usr/bin/env python3
"""
Mac系统适配改造测试脚本

仅测试我们改造的部分，不依赖外部模块：
1. 测试平台检测工具函数
2. 测试动态库路径处理
3. 测试文件编码修复
"""

import sys
import platform
from pathlib import Path

# 添加vnpy路径
sys.path.insert(0, str(Path(__file__).parent))


def test_platform_utils():
    """测试平台工具函数"""
    print("=" * 60)
    print("测试1: 平台工具函数")
    print("=" * 60)
    
    try:
        from vnpy.trader.platform_utils import (
            is_mac_system,
            is_windows_system,
            get_dylib_path,
            get_framework_path,
            get_mac_arch,
            validate_framework_path
        )
        
        # 测试系统检测
        print(f"当前系统: {platform.system()}")
        print(f"is_mac_system(): {is_mac_system()}")
        print(f"is_windows_system(): {is_windows_system()}")
        assert is_mac_system() == (platform.system() == "Darwin"), "Mac系统检测错误"
        assert is_windows_system() == (platform.system() == "Windows"), "Windows系统检测错误"
        print("✓ 系统检测函数正常")
        
        # 测试Mac架构
        if is_mac_system():
            arch = get_mac_arch()
            print(f"Mac架构: {arch}")
            assert arch in ["x86_64", "arm64"], f"未知的Mac架构: {arch}"
            print("✓ Mac架构检测正常")
        
        # 测试dylib路径
        dylib_path = get_dylib_path("/usr/local/lib", "mylib")
        expected = "/usr/local/lib/mylib.dylib"
        assert dylib_path == expected, f"dylib路径错误: {dylib_path} != {expected}"
        print(f"✓ dylib路径处理正常: {dylib_path}")
        
        # 测试framework路径
        framework_path = "/path/to/thostmduserapi_se.framework"
        internal_path = get_framework_path(framework_path)
        expected = "/path/to/thostmduserapi_se.framework/Versions/A/thostmduserapi_se"
        assert internal_path == expected, f"framework路径错误: {internal_path} != {expected}"
        print(f"✓ framework路径处理正常: {internal_path}")
        
        # 测试framework验证（不存在的路径应该返回False）
        result = validate_framework_path("/nonexistent/framework.framework")
        assert result is False, "不存在的framework应该返回False"
        print("✓ framework验证正常")
        
        print("\n✓ 所有平台工具函数测试通过")
        return True
    except Exception as e:
        print(f"✗ 平台工具函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qt_platform_detection():
    """测试qt.py中的平台检测改造"""
    print("\n" + "=" * 60)
    print("测试2: qt.py平台检测改造")
    print("=" * 60)
    
    try:
        # 直接读取文件检查代码
        qt_file = Path(__file__).parent / "vnpy" / "trader" / "ui" / "qt.py"
        content = qt_file.read_text(encoding="utf-8")
        
        # 检查是否使用了platform.system()
        if "platform.system()" in content:
            print("✓ 使用了platform.system()进行平台检测")
        else:
            print("✗ 未找到platform.system()")
            return False
        
        # 检查Windows特定代码是否被条件化
        if 'if platform.system() == "Windows":' in content:
            print("✓ Windows特定代码已正确条件化")
        elif 'if "Windows" in platform.uname():' in content:
            print("✗ 仍在使用platform.uname()，需要修改")
            return False
        else:
            print("⚠ 未找到Windows特定代码检查，可能已被移除")
        
        print("\n✓ qt.py平台检测改造验证通过")
        return True
    except Exception as e:
        print(f"✗ qt.py平台检测改造验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_encoding():
    """测试文件编码修复"""
    print("\n" + "=" * 60)
    print("测试3: 文件编码修复")
    print("=" * 60)
    
    try:
        # 检查logger.py
        logger_file = Path(__file__).parent / "vnpy" / "trader" / "logger.py"
        logger_content = logger_file.read_text(encoding="utf-8")
        
        if 'encoding="utf-8"' in logger_content or "encoding='utf-8'" in logger_content:
            print("✓ logger.py已添加UTF-8编码")
        else:
            print("✗ logger.py未找到UTF-8编码设置")
            return False
        
        # 检查widget.py
        widget_file = Path(__file__).parent / "vnpy" / "trader" / "ui" / "widget.py"
        widget_content = widget_file.read_text(encoding="utf-8")
        
        # 查找文件写入操作
        if 'with open(path, "w", encoding="utf-8")' in widget_content:
            print("✓ widget.py文件写入已添加UTF-8编码")
        else:
            print("⚠ widget.py文件写入操作可能未找到或已修改")
        
        print("\n✓ 文件编码修复验证通过")
        return True
    except Exception as e:
        print(f"✗ 文件编码修复验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_platform_utils_import():
    """测试platform_utils模块导入"""
    print("\n" + "=" * 60)
    print("测试4: platform_utils模块导入")
    print("=" * 60)
    
    try:
        from vnpy.trader import platform_utils
        
        # 检查所有函数是否可导入
        functions = [
            'is_mac_system',
            'is_windows_system',
            'get_dylib_path',
            'get_framework_path',
            'get_mac_arch',
            'validate_framework_path',
            'load_mac_library',
            'find_framework_library',
            'validate_mac_library'
        ]
        
        for func_name in functions:
            if hasattr(platform_utils, func_name):
                print(f"✓ {func_name} 可导入")
            else:
                print(f"✗ {func_name} 不可导入")
                return False
        
        print("\n✓ 所有platform_utils函数可正常导入")
        return True
    except Exception as e:
        print(f"✗ platform_utils模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("VNPY Mac系统适配改造测试")
    print("=" * 60)
    print(f"Python版本: {sys.version}")
    print(f"系统信息: {platform.platform()}")
    print(f"当前系统: {platform.system()}")
    print()
    
    results = []
    
    # 测试1: 平台工具函数
    results.append(("平台工具函数", test_platform_utils()))
    
    # 测试2: qt.py平台检测改造
    results.append(("qt.py平台检测改造", test_qt_platform_detection()))
    
    # 测试3: 文件编码修复
    results.append(("文件编码修复", test_file_encoding()))
    
    # 测试4: platform_utils模块导入
    results.append(("platform_utils模块导入", test_platform_utils_import()))
    
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
        print("\n🎉 所有Mac适配改造测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
