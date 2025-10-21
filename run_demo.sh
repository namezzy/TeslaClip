#!/bin/bash

# 一键运行脚本 - 自动安装并运行测试

echo "================================================"
echo "  特斯拉视频活动提取器 - 一键运行演示"
echo "================================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "✓ Python 环境: $(python3 --version)"
echo ""

# 检查依赖
echo "正在检查依赖..."
python3 -c "import cv2, numpy, tqdm" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠ 需要安装依赖包"
    echo ""
    read -p "是否现在安装？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在安装依赖..."
        pip3 install opencv-python numpy tqdm
        if [ $? -ne 0 ]; then
            echo "❌ 安装失败，请手动运行: pip3 install opencv-python numpy tqdm"
            exit 1
        fi
        echo "✓ 依赖安装完成"
    else
        echo "取消安装，退出"
        exit 0
    fi
else
    echo "✓ 所有依赖已安装"
fi

echo ""
echo "================================================"
echo ""

# 检查是否有测试视频
if [ ! -f "test_video.mp4" ]; then
    echo "未找到测试视频，正在创建..."
    python3 create_test_video.py
    echo ""
fi

if [ -f "test_video.mp4" ]; then
    echo "================================================"
    echo "  开始处理测试视频"
    echo "================================================"
    echo ""
    echo "命令: python3 main.py -i test_video.mp4"
    echo ""
    
    python3 main.py -i test_video.mp4
    
    echo ""
    echo "================================================"
    echo "  处理完成！"
    echo "================================================"
    echo ""
    echo "提取的截图保存在: ./extracted_frames/"
    echo ""
    
    if [ -d "extracted_frames" ]; then
        echo "提取的文件:"
        ls -lh extracted_frames/ 2>/dev/null | tail -n +2 | head -10
        
        count=$(ls extracted_frames/*.jpg 2>/dev/null | wc -l)
        echo ""
        echo "共提取 $count 个活动帧"
    fi
    
    echo ""
    echo "下一步："
    echo "  • 查看截图: ls extracted_frames/"
    echo "  • 处理自己的视频: python3 main.py -i 你的视频.mp4"
    echo "  • 查看帮助: python3 main.py --help"
    echo "  • 阅读文档: cat 如何运行.md"
    echo ""
else
    echo "❌ 无法创建测试视频"
    echo ""
    echo "您可以直接处理自己的视频："
    echo "  python3 main.py -i 你的视频.mp4"
    echo ""
fi
