# PyInstaller macOS .app结构修复说明

## 问题根源

根据PyInstaller官方GitHub Issues（#4413, #1060, #8927），`(null)`错误的根本原因是：

**在`--onedir`模式下，`BUNDLE`对象必须接收`COLLECT`对象，而不是`EXE`对象！**

这是PyInstaller的一个已知问题，使用命令行参数`--windowed --onedir`时，PyInstaller可能不会正确处理这个结构。

## 解决方案

### 使用spec文件（已实现）

创建`vnpy_mac.spec`文件，明确指定：

```python
# 1. 创建EXE对象
exe = EXE(...)

# 2. 创建COLLECT对象（关键！）
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='VNPY-Optimized',
)

# 3. 创建BUNDLE对象，使用coll而不是exe
app = BUNDLE(
    coll,  # ✅ 正确：使用COLLECT对象
    # exe,  # ❌ 错误：不能直接使用EXE对象
    name='VNPY-Optimized.app',
    info_plist={
        'CFBundleExecutable': 'VNPY-Optimized',  # 明确指定
        ...
    },
)
```

### 为什么这样修复？

1. **PyInstaller官方要求**：在onedir模式下，BUNDLE必须接收COLLECT对象
2. **命令行参数的限制**：`--windowed --onedir`可能不会正确处理这个结构
3. **spec文件的优势**：可以精确控制打包过程，确保结构正确

## 验证方法

编译后，检查：

```bash
# 1. 检查.app结构
ls -la dist/VNPY-Optimized.app/Contents/

# 2. 检查可执行文件
ls -la dist/VNPY-Optimized.app/Contents/MacOS/

# 3. 检查Info.plist
plutil -p dist/VNPY-Optimized.app/Contents/Info.plist | grep CFBundleExecutable

# 4. 测试运行（在终端中）
./dist/VNPY-Optimized.app/Contents/MacOS/VNPY-Optimized
```

## 参考链接

- [PyInstaller Issue #4413](https://github.com/pyinstaller/pyinstaller/issues/4413)
- [PyInstaller Issue #1060](https://github.com/pyinstaller/pyinstaller/issues/1060)
- [PyInstaller Issue #8927](https://github.com/pyinstaller/pyinstaller/issues/8927)
