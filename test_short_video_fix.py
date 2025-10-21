#!/usr/bin/env python3
"""
测试短视频进度条修复
创建一个10秒的短视频并测试进度条是否正确显示到100%
"""

import cv2
import numpy as np
import subprocess
import sys
import os

def create_short_test_video(output_path='test_short_video.mp4', duration=10, fps=30):
    """创建一个10秒的测试视频"""
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    print(f"创建 {duration} 秒测试视频: {output_path}")
    print(f"  分辨率: {width}x{height}")
    print(f"  帧率: {fps} fps")
    print(f"  总帧数: {total_frames}")
    
    for i in range(total_frames):
        # 创建黑色背景
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 添加运动的圆形（3-7秒）
        if 3 * fps <= i < 7 * fps:
            t = (i - 3 * fps) / (4 * fps)
            x = int(50 + t * (width - 100))
            y = height // 2
            cv2.circle(frame, (x, y), 30, (0, 255, 0), -1)
            cv2.putText(frame, "Motion", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 添加帧号和时间戳
        timestamp = f"{i/fps:.1f}s (Frame {i}/{total_frames})"
        cv2.putText(frame, timestamp, (10, height-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    file_size = os.path.getsize(output_path) / 1024
    print(f"✓ 视频创建完成: {file_size:.1f} KB\n")
    return output_path

def test_progress_bar():
    """测试进度条"""
    print("=" * 70)
    print("测试短视频进度条修复")
    print("=" * 70)
    print()
    
    # 创建测试视频
    video_path = create_short_test_video()
    
    # 测试处理
    print("开始处理视频...")
    print("请观察进度条是否达到 100%")
    print("-" * 70)
    
    result = subprocess.run(
        ["python3", "main.py", "-i", video_path],
        text=True
    )
    
    print("-" * 70)
    
    if result.returncode == 0:
        print("\n✓ 测试完成！")
        print("\n请确认以下几点：")
        print("  1. 进度条是否从 0% 增长到 100%")
        print("  2. 是否显示了处理速度（帧/s）")
        print("  3. 是否显示了预计剩余时间")
        print("  4. 是否显示了当前视频时间戳")
        print("  5. 进度条最终是否正确到达 100%")
    else:
        print("\n✗ 测试失败")
        return 1
    
    # 清理测试文件（可选）
    cleanup = input("\n是否删除测试视频? (y/n): ")
    if cleanup.lower() == 'y':
        os.remove(video_path)
        print(f"✓ 已删除 {video_path}")
    
    return 0

if __name__ == '__main__':
    sys.exit(test_progress_bar())
