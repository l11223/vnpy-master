# GitHub Actions 工作流说明

## 📦 VNPY Mac DMG 自动打包

### 文件
- `vnpy_mac_dmg.yml` - Mac DMG自动打包工作流

### 使用方法

1. **推送到GitHub后自动触发**（推送到main分支）
2. **手动触发**：Actions → VNPY Mac DMG Auto Build → Run workflow

### 生成产物

打包完成后，在Artifacts中下载：
- `VNPY-Mac-DMG` - 可直接安装的dmg文件

### 配置说明

详见根目录 `GitHub Actions打包说明.md`
