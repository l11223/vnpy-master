# 启动错误"(null)"问题修复

## 错误含义

**错误信息：** "应用程序'程序坞'没有权限打开'(null)'"

**含义：**
- macOS Dock无法找到应用的可执行文件
- `(null)`表示Info.plist中的`CFBundleExecutable`配置有问题
- 可能的原因：
  1. Info.plist中的`CFBundleExecutable`值不正确
  2. 可执行文件不存在或路径不对
  3. 可执行文件没有执行权限
  4. .app结构不完整

## 修复方案

### 1. 确保Info.plist正确配置

Info.plist中的`CFBundleExecutable`必须指向：
- 可执行文件的**文件名**（不是完整路径）
- 文件必须在`Contents/MacOS/`目录中
- 文件名必须完全匹配（区分大小写）

### 2. 验证.app结构

正确的结构：
```
VNPY.app/
  Contents/
    Info.plist          # CFBundleExecutable = "VNPY-Optimized"
    MacOS/
      VNPY-Optimized    # 可执行文件（必须有执行权限）
      _internal/        # PyInstaller依赖
      vnpy/             # 数据文件
    Resources/
      vnpy.icns         # 图标（可选）
```

### 3. 验证命令

```bash
# 检查Info.plist
plutil -p VNPY.app/Contents/Info.plist | grep CFBundleExecutable

# 检查可执行文件
ls -lh VNPY.app/Contents/MacOS/VNPY-Optimized

# 检查文件类型
file VNPY.app/Contents/MacOS/VNPY-Optimized

# 检查权限
stat -f "%A %N" VNPY.app/Contents/MacOS/VNPY-Optimized
```
