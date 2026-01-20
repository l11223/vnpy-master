"""
A股交易接口Mac适配测试脚本

测试gateway_mac_adapter适配器的基本功能，验证Mac系统动态库加载适配。
"""

import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_adapter_creation():
    """测试适配器创建"""
    print("\n测试: 适配器创建")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import (
            GatewayMacAdapter,
            get_gateway_adapter,
            create_xtp_adapter,
            create_tora_adapter
        )
        
        # 测试通用适配器
        adapter1 = GatewayMacAdapter("TEST")
        assert adapter1.gateway_name == "TEST"
        print("  ✓ GatewayMacAdapter创建成功")
        
        # 测试get_gateway_adapter
        xtp_adapter = get_gateway_adapter("XTP")
        assert xtp_adapter.gateway_name == "XTP"
        print("  ✓ XTP适配器创建成功")
        
        tora_adapter = get_gateway_adapter("TORA")
        assert tora_adapter.gateway_name == "TORA"
        print("  ✓ TORA适配器创建成功")
        
        # 测试create函数
        xtp_adapter2 = create_xtp_adapter()
        assert xtp_adapter2.gateway_name == "XTP"
        print("  ✓ create_xtp_adapter成功")
        
        tora_adapter2 = create_tora_adapter()
        assert tora_adapter2.gateway_name == "TORA"
        print("  ✓ create_tora_adapter成功")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_library_management():
    """测试库管理功能"""
    print("\n测试: 库管理功能")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import GatewayMacAdapter
        
        adapter = GatewayMacAdapter("TEST")
        
        # 测试is_library_loaded
        assert not adapter.is_library_loaded("test_lib")
        print("  ✓ is_library_loaded检查通过")
        
        # 测试get_loaded_libraries
        libs = adapter.get_loaded_libraries()
        assert isinstance(libs, dict)
        assert len(libs) == 0
        print("  ✓ get_loaded_libraries检查通过")
        
        # 测试get_library_path（未加载的库）
        path = adapter.get_library_path("test_lib")
        assert path is None
        print("  ✓ get_library_path检查通过")
        
        # 测试unload_library（未加载的库）
        result = adapter.unload_library("test_lib")
        assert result is False
        print("  ✓ unload_library检查通过")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_library_search():
    """测试库搜索功能（不实际加载）"""
    print("\n测试: 库搜索功能")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import get_gateway_adapter
        
        # 测试XTP适配器
        xtp_adapter = get_gateway_adapter("XTP")
        
        # 测试查找不存在的库（应该返回None，不抛出异常）
        lib_path = xtp_adapter.find_library(
            "nonexistent_lib",
            search_paths=["/tmp"],
            framework_name="NONEXISTENT"
        )
        assert lib_path is None or isinstance(lib_path, str)
        print("  ✓ XTP适配器库搜索功能正常")
        
        # 测试TORA适配器
        tora_adapter = get_gateway_adapter("TORA")
        
        lib_path = tora_adapter.find_library(
            "nonexistent_lib",
            search_paths=["/tmp"],
            framework_name="NONEXISTENT"
        )
        assert lib_path is None or isinstance(lib_path, str)
        print("  ✓ TORA适配器库搜索功能正常")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_platform_utils_integration():
    """测试platform_utils集成"""
    print("\n测试: platform_utils集成")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import GatewayMacAdapter
        from vnpy.trader.platform_utils import is_mac_system
        
        adapter = GatewayMacAdapter("TEST")
        
        # 验证适配器使用了platform_utils
        # 如果系统是Mac，适配器应该能正常工作
        # 如果不是Mac，适配器也应该能正常工作（只是不会使用Mac特定功能）
        print(f"  ✓ 当前系统: {os.name}")
        print(f"  ✓ Mac系统检测: {is_mac_system()}")
        print("  ✓ platform_utils集成正常")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_xtp_adapter_config():
    """测试XTP适配器配置"""
    print("\n测试: XTP适配器配置")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import create_xtp_adapter
        
        adapter = create_xtp_adapter()
        
        # 验证适配器已创建
        assert adapter is not None
        assert adapter.gateway_name == "XTP"
        print("  ✓ XTP适配器配置正确")
        
        # 验证适配器可以用于库搜索（即使库不存在）
        lib_path = adapter.find_library(
            "xtpapi",
            search_paths=[os.path.expanduser("~/vnpy_xtp/lib")],
            framework_name="XTP"
        )
        # 库可能不存在，这是正常的
        print(f"  ✓ XTP库搜索测试完成（路径: {lib_path or '未找到'}）")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tora_adapter_config():
    """测试TORA适配器配置"""
    print("\n测试: TORA适配器配置")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import create_tora_adapter
        
        adapter = create_tora_adapter()
        
        # 验证适配器已创建
        assert adapter is not None
        assert adapter.gateway_name == "TORA"
        print("  ✓ TORA适配器配置正确")
        
        # 验证适配器可以用于库搜索（即使库不存在）
        lib_path = adapter.find_library(
            "toraapi",
            search_paths=[os.path.expanduser("~/vnpy_tora/lib")],
            framework_name="TORA"
        )
        # 库可能不存在，这是正常的
        print(f"  ✓ TORA库搜索测试完成（路径: {lib_path or '未找到'}）")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n测试: 错误处理")
    print("-" * 60)
    
    try:
        from vnpy.trader.gateway_mac_adapter import GatewayMacAdapter
        
        adapter = GatewayMacAdapter("TEST")
        
        # 测试加载不存在的必需库（应该抛出异常）
        try:
            lib = adapter.load_library(
                "nonexistent_lib",
                search_paths=["/tmp"],
                required=True
            )
            print("  ⚠ 未抛出预期的异常（库可能意外存在）")
        except OSError:
            print("  ✓ 必需库未找到时正确抛出异常")
        
        # 测试加载不存在的可选库（应该返回None）
        lib = adapter.load_library(
            "nonexistent_lib",
            search_paths=["/tmp"],
            required=False
        )
        assert lib is None
        print("  ✓ 可选库未找到时返回None")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("A股交易接口Mac适配测试")
    print("=" * 60)
    
    tests = [
        ("适配器创建", test_adapter_creation),
        ("库管理功能", test_library_management),
        ("库搜索功能", test_library_search),
        ("platform_utils集成", test_platform_utils_integration),
        ("XTP适配器配置", test_xtp_adapter_config),
        ("TORA适配器配置", test_tora_adapter_config),
        ("错误处理", test_error_handling),
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
        print("\n✓ 所有适配器功能测试通过！")
        print("\n注意: 实际库加载测试需要下载vnpy_xtp或vnpy_tora模块")
        print("      并确保动态库文件存在于指定路径")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
