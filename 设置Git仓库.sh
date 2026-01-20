#!/bin/bash
# VNPY Git仓库快速设置脚本

echo "=================================================================================="
echo "VNPY Git仓库设置"
echo "=================================================================================="
echo ""

# 进入项目目录
cd "$(dirname "$0")"
echo "当前目录: $(pwd)"
echo ""

# 检查是否已有git仓库
if [ ! -d .git ]; then
    echo "初始化git仓库..."
    git init
    echo "✅ Git仓库已初始化"
else
    echo "✅ Git仓库已存在"
fi

echo ""
echo "=================================================================================="
echo "下一步操作"
echo "=================================================================================="
echo ""
echo "1. 添加远程仓库（连接到GitHub）:"
echo "   git remote add origin https://github.com/你的用户名/你的仓库名.git"
echo ""
echo "2. 或者如果已有远程仓库，检查:"
echo "   git remote -v"
echo ""
echo "3. 添加文件:"
echo "   git add .github/workflows/vnpy_mac_dmg.yml"
echo "   git add .gitignore"
echo "   git add ."
echo ""
echo "4. 提交:"
echo "   git commit -m '添加Mac DMG自动打包工作流和配置文件'"
echo ""
echo "5. 推送到GitHub:"
echo "   git push -u origin main"
echo ""
echo "=================================================================================="
echo "如果还没有GitHub仓库："
echo "=================================================================================="
echo ""
echo "1. 访问 https://github.com/new 创建新仓库"
echo "2. 复制仓库URL（如: https://github.com/用户名/仓库名.git）"
echo "3. 运行: git remote add origin <你的仓库URL>"
echo ""
echo "=================================================================================="
