# DMG打包方案对比

## 结论：DMG完全支持，问题在于配置方式

DMG是macOS的标准安装包格式，**完全支持**。问题在于PyInstaller的配置细节。

## 两种方案对比

### 方案1：--onedir模式（当前使用，复杂但灵活）

**优点：**
- 启动速度快（文件分散）
- 便于调试（可以看到所有文件）
- 体积相对较小

**缺点：**
- 结构复杂，需要COLLECT对象
- 容易出现(null)错误
- 配置要求高

**适用场景：** 大型应用，需要频繁更新

### 方案2：--onefile模式（推荐，简单可靠）

**优点：**
- **结构简单**：BUNDLE直接接收EXE对象
- **配置简单**：不需要COLLECT对象
- **更可靠**：避免onedir的复杂问题
- **单文件**：用户使用更方便

**缺点：**
- 启动稍慢（需要解压）
- 体积稍大（所有文件打包在一起）

**适用场景：** 中小型应用，追求简单可靠

## 推荐方案

**建议使用--onefile模式**，原因：

1. **更简单**：避免onedir的COLLECT/BUNDLE复杂关系
2. **更可靠**：PyInstaller对onefile的支持更成熟
3. **更易调试**：如果出问题，更容易定位
4. **用户体验**：单文件应用更符合Mac用户习惯

## 实施步骤

1. 使用`vnpy_mac_simple.spec`（--onefile模式）
2. 如果还有问题，可以尝试：
   - 使用`py2app`（Mac专用打包工具）
   - 使用`cx_Freeze`（跨平台，Mac支持好）
   - 手动创建.app结构（最可靠但最复杂）

## 参考

- PyInstaller官方文档：https://pyinstaller.org/
- PyQt5 macOS打包教程：https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/
- 成功案例：很多Python GUI应用都使用onefile模式成功打包
