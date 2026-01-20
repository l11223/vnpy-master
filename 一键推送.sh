#!/bin/bash
# VNPY一键推送到GitHub

echo "=================================================================================="
echo "VNPY一键推送到GitHub"
echo "=================================================================================="
echo ""

cd "$(dirname "$0")"

# 检查是否已有远程仓库
REMOTE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REMOTE_URL" ] || [[ "$REMOTE_URL" == *"你的用户名"* ]]; then
    echo "⚠️  需要配置GitHub仓库URL"
    echo ""
    echo "请输入你的GitHub仓库URL（例如: https://github.com/用户名/仓库名.git）"
    echo "或者SSH格式（例如: git@github.com:用户名/仓库名.git）"
    echo ""
    read -p "仓库URL: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo "❌ 未输入仓库URL，退出"
        exit 1
    fi
    
    # 移除旧的远程仓库（如果存在）
    git remote remove origin 2>/dev/null
    
    # 添加新的远程仓库
    git remote add origin "$REPO_URL"
    echo "✅ 已添加远程仓库: $REPO_URL"
else
    echo "✅ 远程仓库已配置: $REMOTE_URL"
    echo ""
    read -p "是否使用当前远程仓库？(y/n): " USE_CURRENT
    if [ "$USE_CURRENT" != "y" ]; then
        read -p "请输入新的仓库URL: " REPO_URL
        git remote set-url origin "$REPO_URL"
        echo "✅ 已更新远程仓库URL"
    fi
fi

echo ""
echo "=================================================================================="
echo "开始推送..."
echo "=================================================================================="
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "发现未提交的更改，正在添加..."
    git add .
    git commit -m "更新文件: $(date '+%Y-%m-%d %H:%M:%S')"
fi

# 推送到GitHub
echo "正在推送到GitHub..."
if git push -u origin main 2>&1; then
    echo ""
    echo "=================================================================================="
    echo "✅ 推送成功！"
    echo "=================================================================================="
    echo ""
    echo "下一步："
    echo "1. 访问你的GitHub仓库页面"
    echo "2. 点击 Actions 标签"
    echo "3. 选择 'VNPY Mac DMG Auto Build'"
    echo "4. 点击 'Run workflow' 手动触发打包"
    echo ""
else
    echo ""
    echo "=================================================================================="
    echo "❌ 推送失败"
    echo "=================================================================================="
    echo ""
    echo "可能的原因："
    echo "1. 仓库URL不正确"
    echo "2. 没有推送权限（需要配置SSH密钥或Personal Access Token）"
    echo "3. 网络问题"
    echo ""
    echo "解决方案："
    echo "1. 检查仓库URL是否正确"
    echo "2. 如果使用HTTPS，可能需要输入GitHub用户名和密码（或Token）"
    echo "3. 如果使用SSH，确保已配置SSH密钥"
    echo ""
fi
