# VNPY Mac版 GitHub Actions 自动打包DMG说明

## 📁 文件位置

配置文件已创建在：
```
.github/workflows/vnpy_mac_dmg.yml
```

## 🚀 快速使用

### 1. 推送到GitHub

```bash
# 确保在main分支（或你配置的分支）
git add .github/workflows/vnpy_mac_dmg.yml
git commit -m "添加Mac DMG自动打包工作流"
git push origin main
```

### 2. 触发打包

#### 方式1：自动触发
- 推送到 `main` 分支后，GitHub Actions 会自动运行

#### 方式2：手动触发（推荐）
1. 进入 GitHub 仓库页面
2. 点击顶部 **Actions** 标签
3. 左侧选择 **VNPY Mac DMG Auto Build**
4. 点击 **Run workflow** 按钮
5. 选择分支，点击 **Run workflow** 确认

### 3. 下载DMG

打包完成后：
1. 进入该次 Action 运行记录
2. 滚动到最下方 **Artifacts** 部分
3. 点击 **VNPY-Mac-DMG** 下载生成的 dmg 文件

## ⚙️ 配置说明

### 已配置项

✅ **Python版本**: 3.9（VNPY兼容最优）
✅ **启动脚本**: `启动量化系统.py`
✅ **程序名称**: VNPY-Optimized
✅ **DMG名称**: VNPY-Mac-Optimized.dmg
✅ **隐藏导入**: 已包含所有增强模块

### 需要修改的地方

#### 1. VNPY安装方式（第3步）

根据你的情况选择：

```yaml
# 方式1：修改了VNPY框架核心源码（开发版）
pip install -e .

# 方式2：仅修改自定义策略/脚本（未改框架）
pip install vnpy
```

**当前配置**: 使用方式1（`pip install -e .`）

#### 2. 启动脚本（第4步）

如果启动脚本不是 `启动量化系统.py`，修改：

```yaml
pyinstaller -F -w 你的启动脚本.py \
```

#### 3. 添加Gateway模块（第4步）

如果使用了其他Gateway，添加：

```yaml
--hidden-import vnpy_xtp \
--hidden-import vnpy_tora \
--hidden-import vnpy_ctp \
```

#### 4. 分支名称（顶部）

如果主分支不是 `main`：

```yaml
on:
  push:
    branches: [ dev ]  # 改为你的分支名
```

## 📦 打包内容

当前配置会打包：

- ✅ VNPY核心框架
- ✅ Mac适配模块（platform_utils）
- ✅ 多进程管理器
- ✅ 增强策略模板
- ✅ 历史数据管理器
- ✅ 数据过滤器
- ✅ 优化指标计算
- ✅ 风险管理器
- ✅ 状态监控
- ✅ Gateway适配器

## 🔧 常见问题

### 1. TA-Lib缺失

配置中已预装 `ta-lib`，无需额外操作。

### 2. 图标问题

如果需要图标：
1. 准备 `vnpy.icns` 文件（Mac图标格式）
2. 放在仓库根目录
3. 取消注释配置中的图标相关行

### 3. 无法验证开发者

本地运行dmg时：
- 右键 `VNPY.app` → **打开**
- 即可绕过Mac系统安全验证

### 4. 打包体积

VNPY依赖较多，dmg包 **200-500M** 属正常，无需精简。

### 5. 打包失败

检查：
- Python版本是否为3.9
- 所有依赖是否正确安装
- 启动脚本路径是否正确
- 隐藏导入是否包含所有使用的模块

## 📋 验证打包结果

下载dmg后：

1. 双击打开 dmg 文件
2. 将 `VNPY.app` 拖入 Applications
3. 启动台找到并打开
4. 确认功能与本地运行的优化源码一致

## 🎯 优化建议

### 减小体积（可选）

如果dmg太大，可以：

1. 排除不必要的模块
2. 使用 `--exclude-module` 排除未使用的库
3. 压缩资源文件

### 添加版本号

在DMG名称中添加版本：

```yaml
"VNPY-Mac-Optimized-v1.0.0.dmg"
```

### 自动发布

可以添加自动发布到GitHub Releases的步骤（需要配置token）。

---

**配置文件已就绪，推送到GitHub后即可使用！**
