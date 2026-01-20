#!/bin/bash

# GitHub MCP 自动安装脚本
# 用于Cursor IDE

echo "=================================================================================="
echo "📦 GitHub MCP 安装脚本"
echo "=================================================================================="
echo ""

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装："
    echo "   brew install node"
    exit 1
fi

echo "✅ Node.js版本: $(node --version)"
echo "✅ npm版本: $(npm --version)"
echo ""

# 检查是否需要GitHub Token
echo "⚠️  需要GitHub Personal Access Token"
echo ""
echo "如果还没有Token，请先："
echo "1. 打开: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选权限: repo, workflow"
echo "4. 生成并复制Token"
echo ""

read -p "是否已有GitHub Token？(y/n): " has_token

if [ "$has_token" != "y" ] && [ "$has_token" != "Y" ]; then
    echo ""
    echo "请先生成Token，然后重新运行此脚本"
    echo "Token生成地址: https://github.com/settings/tokens"
    exit 0
fi

echo ""
read -p "请输入你的GitHub Token: " github_token

if [ -z "$github_token" ]; then
    echo "❌ Token不能为空"
    exit 1
fi

echo ""
echo "=================================================================================="
echo "开始安装GitHub MCP服务器..."
echo "=================================================================================="
echo ""

# 方式1：使用Smithery CLI自动安装（推荐）
echo "📦 方式1：使用Smithery CLI自动安装（推荐）"
echo ""

npx -y @smithery/cli@latest install @smithery-ai/github \
  --client cursor \
  --config "{\"githubPersonalAccessToken\":\"$github_token\"}"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 自动安装成功！"
    echo ""
    echo "=================================================================================="
    echo "🎉 安装完成！"
    echo "=================================================================================="
    echo ""
    echo "下一步："
    echo "1. 完全重启Cursor（退出并重新打开）"
    echo "2. 重启后，在Cursor中问我：'检查GitHub MCP是否安装成功'"
    echo ""
    exit 0
fi

echo ""
echo "⚠️  自动安装失败，尝试手动配置..."
echo ""

# 方式2：手动配置
CURSOR_MCP_CONFIG="$HOME/.cursor/mcp.json"

# 检查配置文件是否存在
if [ ! -f "$CURSOR_MCP_CONFIG" ]; then
    echo "创建新的MCP配置文件..."
    mkdir -p "$HOME/.cursor"
    cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$github_token"
      }
    }
  }
}
EOF
    echo "✅ 配置文件已创建"
else
    echo "检测到现有配置文件，需要手动添加GitHub配置"
    echo ""
    echo "请手动编辑: $CURSOR_MCP_CONFIG"
    echo ""
    echo "添加以下内容到 mcpServers 对象中："
    echo ""
    cat << EOF
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$github_token"
      }
    }
EOF
    echo ""
    read -p "是否要自动添加？(y/n): " auto_add
    
    if [ "$auto_add" = "y" ] || [ "$auto_add" = "Y" ]; then
        # 备份原配置
        cp "$CURSOR_MCP_CONFIG" "$CURSOR_MCP_CONFIG.backup"
        echo "✅ 已备份原配置到: $CURSOR_MCP_CONFIG.backup"
        
        # 使用Python或Node.js来安全地添加配置
        python3 << PYTHON_SCRIPT
import json
import os

config_path = os.path.expanduser("$CURSOR_MCP_CONFIG")
token = "$github_token"

try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except:
    config = {"mcpServers": {}}

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["github"] = {
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-github"
    ],
    "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": token
    }
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 配置已添加")
PYTHON_SCRIPT
    fi
fi

echo ""
echo "=================================================================================="
echo "🎉 配置完成！"
echo "=================================================================================="
echo ""
echo "下一步："
echo "1. 完全重启Cursor（退出并重新打开）"
echo "2. 重启后，在Cursor中问我：'检查GitHub MCP是否安装成功'"
echo ""
echo "配置文件位置: $CURSOR_MCP_CONFIG"
echo ""
