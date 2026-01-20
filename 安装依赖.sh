#!/bin/bash
# VNPY量化系统 - 依赖安装脚本

echo "=================================================================================="
echo "VNPY量化系统 - 依赖安装"
echo "=================================================================================="
echo ""

echo "正在安装基础依赖..."
python3 -m pip install loguru tzlocal TA-Lib

echo ""
echo "正在安装UI依赖..."
python3 -m pip install qdarkstyle PySide6

echo ""
echo "正在安装VNPY..."
python3 -m pip install vnpy

echo ""
echo "=================================================================================="
echo "✅ 依赖安装完成！"
echo "=================================================================================="
echo ""
echo "已安装的依赖:"
python3 -m pip list | grep -E "(loguru|tzlocal|TA-Lib|qdarkstyle|PySide6|vnpy)" | head -10

echo ""
echo "现在可以运行:"
echo "  python3 启动量化系统.py          # UI模式"
echo "  python3 启动量化系统.py --no-ui  # 无UI模式"
echo "  python3 测试量化功能.py          # 测试功能"
echo "=================================================================================="
