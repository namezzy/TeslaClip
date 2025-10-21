#!/usr/bin/env python3
"""
测试视频输出功能

测试运动检测和轮廓绘制的视频输出功能
"""

import cv2
import subprocess
import os
from pathlib import Path


def test_video_output():
    """测试视频输出功能"""
    print("=" * 60)
    print("测试视频输出功能")
    print("=" * 60)
    
    # 1. 创建测试视频（如果不存在）
    test_video_path = "test_video.mp4"
    if not os.path.exists(test_video_path):
        print("\n步骤 1: 创建测试视频...")
        result = subprocess.run(
            ["python", "create_test_video.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"创建测试视频失败: {result.stderr}")
            return False
        print("✓ 测试视频创建成功")
    else:
        print(f"\n步骤 1: 使用已存在的测试视频 '{test_video_path}'")
    
    # 2. 运行主程序，启用视频输出
    print("\n步骤 2: 运行主程序并生成输出视频...")
    output_dir = "./test_output_video"
    result = subprocess.run(
        [
            "python", "main.py",
            "-i", test_video_path,
            "-o", output_dir,
            "-s", "30",
            "--min-interval", "0.5",
            "--output-video"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"运行主程序失败: {result.stderr}")
        return False
    
    print("✓ 主程序运行完成")
    print("\n程序输出:")
    print(result.stdout)
    
    # 3. 检查输出视频是否存在
    print("\n步骤 3: 检查输出视频...")
    # 新的输出结构：每个视频有独立的文件夹
    video_folder = Path(output_dir) / "test_video"
    output_video_path = video_folder / "test_video_motion_detected.mp4"
    
    if not video_folder.exists():
        print(f"✗ 视频输出文件夹不存在: {video_folder}")
        return False
    
    if not output_video_path.exists():
        print(f"✗ 输出视频不存在: {output_video_path}")
        return False
    
    print(f"✓ 输出视频存在: {output_video_path}")
    
    # 4. 验证输出视频的基本属性
    print("\n步骤 4: 验证输出视频属性...")
    cap = cv2.VideoCapture(str(output_video_path))
    
    if not cap.isOpened():
        print("✗ 无法打开输出视频")
        return False
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"  视频帧数: {frame_count}")
    print(f"  帧率: {fps:.2f} FPS")
    print(f"  分辨率: {width}x{height}")
    
    if frame_count == 0:
        print("✗ 输出视频为空（0帧）")
        cap.release()
        return False
    
    print("✓ 视频属性正常")
    
    # 5. 读取并显示第一帧（验证内容）
    print("\n步骤 5: 读取视频内容...")
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("✗ 无法读取视频帧")
        return False
    
    print("✓ 成功读取视频帧")
    
    # 6. 检查输出文件大小
    file_size = output_video_path.stat().st_size
    print(f"\n步骤 6: 检查文件大小...")
    print(f"  文件大小: {file_size / 1024:.2f} KB")
    
    if file_size < 1000:  # 小于 1KB 可能有问题
        print("✗ 文件大小异常小，可能生成失败")
        return False
    
    print("✓ 文件大小正常")
    
    # 测试成功
    print("\n" + "=" * 60)
    print("✓ 所有测试通过！")
    print("=" * 60)
    print(f"\n输出文件夹: {video_folder.absolute()}")
    print(f"输出视频: {output_video_path.absolute()}")
    print("\n重要提示:")
    print("  - 输出视频只包含检测到运动的帧（不是所有帧）")
    print("  - 这使得视频更短，文件更小，更易于查看")
    print("  - 所有截图都包含运动检测的轮廓标注")
    print("\n你可以使用以下命令播放输出视频:")
    print(f"  ffplay {output_video_path}")
    print(f"  vlc {output_video_path}")
    print(f"  或直接用视频播放器打开文件")
    
    return True


def main():
    """主函数"""
    success = test_video_output()
    
    if not success:
        print("\n✗ 测试失败")
        exit(1)
    else:
        print("\n✓ 测试成功")
        exit(0)


if __name__ == '__main__':
    main()
