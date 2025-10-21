#!/bin/bash

# 特斯拉视频活动提取器 - 安装脚本

echo "=========================================="
echo "特斯拉视频活动提取器 - 安装向导"
echo "=========================================="
echo ""

# 检查Python版本
echo "1. 检查Python环境..."
if command -v python3 &> /dev/null
then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ 找到 $PYTHON_VERSION"
else
    echo "✗ 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

echo ""
echo "2. 安装依赖包..."
echo "   这可能需要几分钟时间..."
echo ""

pip3 install opencv-python numpy tqdm

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 依赖包安装成功！"
else
    echo ""
    echo "✗ 依赖包安装失败，请检查网络连接或手动安装："
    echo "  pip3 install opencv-python numpy tqdm"
    exit 1
fi

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "快速开始："
echo ""
echo "  # 查看帮助"
echo "  python3 main.py --help"
echo ""
echo "  # 处理单个视频"
echo "  python3 main.py -i your_video.mp4"
echo ""
echo "  # 处理文件夹中的所有视频"
echo "  python3 main.py -i /path/to/videos -o ./output"
echo ""
echo "详细使用说明请查看: QUICKSTART.md"
echo ""
