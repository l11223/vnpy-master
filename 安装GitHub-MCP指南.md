# GitHub MCP 安装指南

## 🎯 为什么需要GitHub MCP？

安装GitHub MCP后，我们可以：
- ✅ **直接查看GitHub Actions状态**（不用手动复制错误）
- ✅ **查看工作流运行日志**（实时查看编译进度）
- ✅ **查看错误信息**（自动分析错误原因）
- ✅ **管理Issues和PR**（方便协作）
- ✅ **搜索代码仓库**（快速查找代码）

## 📦 安装步骤

### 前置要求

1. **Node.js**（版本18+）
2. **GitHub Personal Access Token**（需要生成）

### 步骤1：生成GitHub Token

1. 打开：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 设置：
   - **Note**: `Cursor MCP GitHub`（随便起个名字）
   - **Expiration**: 选择过期时间（建议90天或更长）
   - **Scopes**: 勾选以下权限：
     - ✅ `repo`（完整仓库访问）
     - ✅ `workflow`（查看和管理工作流）
     - ✅ `read:org`（如果需要访问组织仓库）
4. 点击 **"Generate token"**
5. **重要**：复制生成的token（只显示一次！）

### 步骤2：安装GitHub MCP服务器

#### 方式1：自动安装（推荐）✅

使用Smithery CLI自动安装：

```bash
npx -y @smithery/cli@latest install @smithery-ai/github \
  --client cursor \
  --config '{"githubPersonalAccessToken":"你的GitHub_Token"}'
```

**注意**：将 `你的GitHub_Token` 替换为步骤1中生成的token。

#### 方式2：手动配置

1. **安装GitHub MCP服务器**：
   ```bash
   npm install -g @modelcontextprotocol/server-github
   ```

2. **编辑Cursor MCP配置**：
   
   打开文件：`~/.cursor/mcp.json`
   
   添加以下配置：
   ```json
   {
     "mcpServers": {
       "github": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-github"
         ],
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "你的GitHub_Token"
         }
       }
     }
   }
   ```

   **注意**：
   - 如果文件已存在其他MCP服务器配置，在`mcpServers`对象中添加`github`即可
   - 将 `你的GitHub_Token` 替换为步骤1中生成的token

### 步骤3：重启Cursor

配置完成后，**完全重启Cursor**（退出并重新打开）。

### 步骤4：验证安装

重启后，在Cursor中问我：
```
检查GitHub MCP是否安装成功
```

或者直接说：
```
查看GitHub Actions状态
```

如果我能直接访问GitHub信息，说明安装成功！✅

## 🔧 故障排查

### 问题1：找不到npx命令

**解决**：安装Node.js
```bash
# 使用Homebrew安装
brew install node
```

### 问题2：Token无效

**解决**：
1. 检查token是否过期
2. 检查token权限是否包含`repo`和`workflow`
3. 重新生成token并更新配置

### 问题3：MCP服务器无法启动

**解决**：
1. 检查`~/.cursor/mcp.json`格式是否正确（JSON格式）
2. 检查token是否正确设置
3. 查看Cursor的MCP日志（如果有）

## 💡 使用示例

安装成功后，你可以这样使用：

```
查看GitHub Actions的最新运行状态
```

```
查看vnpy-master仓库的Actions错误日志
```

```
查看最近的workflow运行情况
```

```
帮我分析GitHub Actions的编译错误
```

## 🎉 完成！

安装完成后，以后GitHub Actions报错时，你只需要说：
```
GitHub Actions报错了，帮我看看
```

我就能直接查看错误日志并帮你修复！💪
