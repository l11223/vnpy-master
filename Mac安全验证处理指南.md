# Mac安全验证处理指南

## 问题说明

当您首次打开从DMG安装的VNPY应用时，可能会看到以下安全警告：

> **"Apple 无法验证 'VNPY' 是否包含可能危害 Mac 安全或泄漏隐私的恶意软件。"**

这是macOS Gatekeeper的正常安全机制，因为我们的应用没有经过Apple的代码签名和公证。

## 解决方案

### 方法1：使用终端命令移除隔离属性（最简单快速）⭐

在终端中执行以下命令：

```bash
xattr -d com.apple.quarantine /Applications/VNPY.app
```

**说明**：
- `xattr` 是macOS的文件扩展属性管理工具
- `-d` 表示删除属性
- `com.apple.quarantine` 是macOS的隔离属性，用于标记未验证的应用
- 删除后即可正常双击打开，无需每次右键

**如果应用还在DMG中**，先拖到Applications，再执行：
```bash
xattr -d com.apple.quarantine /Applications/VNPY.app
```

**验证是否成功**：
```bash
# 检查隔离属性是否已移除（应该没有输出）
xattr -l /Applications/VNPY.app | grep quarantine
```

### 方法2：右键打开

1. **不要直接双击**应用图标
2. **右键点击** `VNPY.app`
3. 选择 **"打开"**
4. 在弹出的安全对话框中，点击 **"打开"**

这样会告诉macOS您信任这个应用，以后就可以正常双击打开了。

### 方法3：系统设置中允许

1. 打开 **系统设置**（System Settings）
2. 进入 **隐私与安全性**（Privacy & Security）
3. 找到关于VNPY的阻止提示
4. 点击 **"仍要打开"**（Open Anyway）

### 方法4：临时禁用Gatekeeper（不推荐）

```bash
# 临时允许运行未签名应用（仅限当前会话）
sudo spctl --master-disable

# 使用后重新启用（重要！）
sudo spctl --master-enable
```

⚠️ **警告**：禁用Gatekeeper会降低系统安全性，不推荐使用。

## 为什么会出现这个提示？

1. **未代码签名**：应用没有使用Apple Developer证书签名
2. **未公证**：应用没有经过Apple的公证（Notarization）流程
3. **安全机制**：macOS Gatekeeper保护用户免受恶意软件侵害

## 长期解决方案

### 选项1：添加代码签名（需要Apple Developer账号）

如果您有Apple Developer账号（$99/年），可以：

1. **获取开发者证书**
   ```bash
   # 在Xcode中登录Apple ID
   # 自动获取Developer ID证书
   ```

2. **签名应用**
   ```bash
   codesign --force --deep --sign "Developer ID Application: Your Name" VNPY.app
   ```

3. **公证应用**
   ```bash
   xcrun notarytool submit VNPY.dmg --keychain-profile "notarytool-profile" --wait
   ```

### 选项2：使用自签名证书（免费，但仍有警告）

```bash
# 创建自签名证书
security create-certificate -n "VNPY Developer" -k login.keychain

# 签名应用
codesign --force --deep --sign "VNPY Developer" VNPY.app
```

⚠️ **注意**：自签名证书仍然会显示警告，但会显示证书信息。

### 选项3：保持现状（最简单）

- 用户首次使用时右键打开即可
- 在README中添加说明
- 这是开源项目的常见做法

## 在DMG中添加说明

我们已经在DMG中包含了`README.txt`文件，其中说明了：

```
安装步骤：
1. 将 VNPY.app 拖拽到 Applications 文件夹
2. 在启动台找到并打开 VNPY优化版
3. 首次运行时，右键点击应用 -> 打开（绕过安全验证）
```

## 更新GitHub Actions工作流（可选）

如果需要添加代码签名，可以在`.github/workflows/vnpy_mac_dmg.yml`中添加：

```yaml
# 在"Organize Mac App Structure"步骤后添加
- name: Code Sign App (Optional)
  if: env.APPLE_CERTIFICATE != ''
  run: |
    security create-keychain -p "${{ secrets.APPLE_KEYCHAIN_PASSWORD }}" build.keychain
    security default-keychain -s build.keychain
    security unlock-keychain -p "${{ secrets.APPLE_KEYCHAIN_PASSWORD }}" build.keychain
    security import "${{ secrets.APPLE_CERTIFICATE }}" -k build.keychain -P "${{ secrets.APPLE_CERTIFICATE_PASSWORD }}" -T /usr/bin/codesign
    security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "${{ secrets.APPLE_KEYCHAIN_PASSWORD }}" build.keychain
    codesign --force --deep --sign "Developer ID Application: Your Name" VNPY.app
```

## 推荐方案

对于开源项目，**推荐使用方法1（xattr命令）**：

1. ✅ **最简单**：一条命令即可解决
2. ✅ **永久有效**：删除后无需每次操作
3. ✅ **安全**：不降低系统安全性
4. ✅ **快速**：比右键打开更快

**使用方法**：
```bash
xattr -d com.apple.quarantine /Applications/VNPY.app
```

执行后即可正常双击打开应用！

## 相关链接

- [Apple代码签名文档](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [macOS Gatekeeper说明](https://support.apple.com/zh-cn/HT202491)
