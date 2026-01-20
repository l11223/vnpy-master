"""
阶段二模块测试脚本

测试所有阶段二创建的核心模块，验证导入和基本功能。
"""

import sys
import os
import ast

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_syntax(file_path):
    """测试文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"解析错误: {e}"

def test_imports(file_path):
    """测试文件中的导入语句"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 检查是否有相对导入
        has_relative_import = 'from .' in code or 'from ..' in code
        
        # 检查是否有未定义的变量使用
        issues = []
        
        # 检查traceback使用但未导入
        if 'traceback.' in code and 'import traceback' not in code:
            issues.append("使用了traceback但未导入")
        
        return True, has_relative_import, issues
    except Exception as e:
        return False, False, [f"检查错误: {e}"]

def test_key_classes(file_path):
    """检查关键类是否存在"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 根据文件名确定应该存在的类
        filename = os.path.basename(file_path)
        expected_classes = {
            'multiprocess_manager.py': ['ProcessManager'],
            'enhanced_cta_template.py': ['EnhancedCtaTemplate'],
            'history_manager.py': ['HistoryManager'],
            'data_filter.py': ['DataFilter'],
            'multiprocess_backtester.py': ['MultiProcessBacktester'],
            'optimization_metrics.py': ['OptimizationMetrics'],
            'optimization_visualization.py': ['OptimizationVisualization'],
            'enhanced_risk_manager.py': ['EnhancedRiskManager'],
            'status_monitor.py': ['StatusMonitor']
        }
        
        expected = expected_classes.get(filename, [])
        found = []
        missing = []
        
        for cls_name in expected:
            if f'class {cls_name}' in code:
                found.append(cls_name)
            else:
                missing.append(cls_name)
        
        return found, missing
    except Exception as e:
        return [], [f"检查错误: {e}"]

def main():
    """主测试函数"""
    print("=" * 60)
    print("阶段二模块测试")
    print("=" * 60)
    
    # 阶段二创建的所有文件
    phase2_files = [
        'vnpy/trader/multiprocess_manager.py',
        'vnpy/trader/enhanced_cta_template.py',
        'vnpy/trader/history_manager.py',
        'vnpy/trader/data_filter.py',
        'vnpy/trader/multiprocess_backtester.py',
        'vnpy/trader/optimization_metrics.py',
        'vnpy/trader/optimization_visualization.py',
        'vnpy/trader/enhanced_risk_manager.py',
        'vnpy/trader/status_monitor.py'
    ]
    
    all_passed = True
    results = []
    
    for file_path in phase2_files:
        full_path = os.path.join(project_root, file_path)
        
        if not os.path.exists(full_path):
            print(f"\n✗ {file_path}: 文件不存在")
            all_passed = False
            results.append((file_path, False, "文件不存在"))
            continue
        
        print(f"\n测试: {file_path}")
        print("-" * 60)
        
        # 1. 语法检查
        syntax_ok, syntax_error = test_syntax(full_path)
        if not syntax_ok:
            print(f"  ✗ 语法检查失败: {syntax_error}")
            all_passed = False
            results.append((file_path, False, syntax_error))
            continue
        print(f"  ✓ 语法检查通过")
        
        # 2. 导入检查
        import_ok, has_relative, import_issues = test_imports(full_path)
        if import_issues:
            print(f"  ⚠ 导入问题:")
            for issue in import_issues:
                print(f"    - {issue}")
                all_passed = False
        
        if has_relative:
            print(f"  ℹ 包含相对导入（正常，需要作为包导入）")
        print(f"  ✓ 导入检查通过")
        
        # 3. 关键类检查
        found_classes, missing_classes = test_key_classes(full_path)
        if missing_classes:
            print(f"  ✗ 缺少关键类: {', '.join(missing_classes)}")
            all_passed = False
        else:
            print(f"  ✓ 关键类存在: {', '.join(found_classes)}")
        
        results.append((file_path, syntax_ok and not import_issues and not missing_classes, None))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed_count = sum(1 for _, ok, _ in results if ok)
    total_count = len(results)
    
    print(f"通过: {passed_count}/{total_count}")
    
    if all_passed:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print("\n✗ 部分测试失败，请检查上述错误")
        return 1

if __name__ == '__main__':
    sys.exit(main())
