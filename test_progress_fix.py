#!/usr/bin/env python3
"""
测试进度条修复的脚本
"""

import sys
import subprocess

print("=" * 60)
print("测试进度条修复")
print("=" * 60)
print()

# 首先创建测试视频
print("1. 创建测试视频...")
result = subprocess.run(["python3", "create_test_video.py"], capture_output=True, text=True)
if result.returncode != 0:
    print("✗ 创建测试视频失败")
    print(result.stderr)
    sys.exit(1)
print("✓ 测试视频创建成功")
print()

# 运行主程序处理视频
print("2. 测试进度条显示...")
print("   运行命令: python3 main.py -i test_video.mp4")
print()
result = subprocess.run(["python3", "main.py", "-i", "test_video.mp4"], text=True)

if result.returncode == 0:
    print()
    print("=" * 60)
    print("✓ 测试完成！请检查进度条是否正确显示到100%")
    print("=" * 60)
else:
    print()
    print("✗ 测试失败")
    sys.exit(1)
