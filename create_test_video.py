#!/usr/bin/env python3
"""
测试脚本 - 创建一个简单的测试视频用于演示
需要先安装依赖: pip3 install opencv-python numpy
"""

import cv2
import numpy as np
import os

def create_test_video(output_path='test_video.mp4', duration=10, fps=30):
    """
    创建一个测试视频，包含运动的物体
    
    Args:
        output_path: 输出视频路径
        duration: 视频时长（秒）
        fps: 帧率
    """
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    print(f"正在创建测试视频: {output_path}")
    print(f"时长: {duration}秒, 分辨率: {width}x{height}, 帧率: {fps}")
    
    for i in range(total_frames):
        # 创建黑色背景
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 在前3秒没有运动（静止）
        if i < fps * 3:
            cv2.putText(frame, "No Motion", (50, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 100, 100), 3)
        
        # 3-7秒有一个移动的圆形（模拟车辆或人）
        elif i < fps * 7:
            t = (i - fps * 3) / (fps * 4)  # 0到1的进度
            x = int(50 + t * (width - 100))
            y = height // 2
            cv2.circle(frame, (x, y), 30, (0, 255, 0), -1)
            cv2.putText(frame, "Motion Detected", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 7-10秒再次静止
        else:
            cv2.putText(frame, "No Motion", (50, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 100, 100), 3)
        
        # 添加时间戳
        timestamp = f"{i/fps:.1f}s"
        cv2.putText(frame, timestamp, (width-150, height-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print(f"✓ 测试视频创建完成: {output_path}")
    print(f"  文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"\n现在可以运行:")
    print(f"  python3 main.py -i {output_path} --preview")

if __name__ == '__main__':
    try:
        create_test_video()
    except Exception as e:
        print(f"创建测试视频失败: {e}")
        print("请先安装依赖: pip3 install opencv-python numpy")
