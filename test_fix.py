#!/usr/bin/env python3
"""
快速测试脚本 - 验证修复是否成功
"""

import sys
import os

def test_import():
    """测试模块导入"""
    print("测试 1: 导入模块...")
    try:
        from main import BatchProcessor
        from video_clip_extractor import VideoClipExtractor
        print("  ✓ 模块导入成功")
        return True
    except Exception as e:
        print(f"  ✗ 模块导入失败: {e}")
        return False


def test_batch_processor_init():
    """测试 BatchProcessor 初始化"""
    print("\n测试 2: 初始化 BatchProcessor...")
    try:
        from main import BatchProcessor
        
        # 测试不启用视频片段提取
        processor1 = BatchProcessor(
            output_dir="./test_output",
            extract_clips=False
        )
        print("  ✓ 基本初始化成功")
        
        # 测试启用视频片段提取
        processor2 = BatchProcessor(
            output_dir="./test_output",
            extract_clips=True,
            min_motion_duration=3.0,
            clip_before=20.0,
            clip_after=20.0
        )
        print("  ✓ 带视频片段提取的初始化成功")
        
        # 验证属性
        assert not hasattr(processor1, 'output_video'), "不应该有 output_video 属性"
        assert hasattr(processor1, 'extract_clips'), "应该有 extract_clips 属性"
        assert hasattr(processor2, 'clip_extractor'), "启用片段提取时应该有 clip_extractor"
        print("  ✓ 属性验证通过")
        
        return True
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_video_clip_extractor():
    """测试 VideoClipExtractor"""
    print("\n测试 3: 初始化 VideoClipExtractor...")
    try:
        from video_clip_extractor import VideoClipExtractor, MotionEvent
        
        extractor = VideoClipExtractor(
            sensitivity=25,
            min_motion_duration=3.0,
            clip_before=20.0,
            clip_after=20.0
        )
        print("  ✓ VideoClipExtractor 初始化成功")
        
        # 测试 MotionEvent
        event = MotionEvent(
            start_time=10.0,
            end_time=15.0,
            duration=5.0,
            start_frame=300,
            end_frame=450
        )
        print(f"  ✓ MotionEvent 创建成功: {event}")
        
        return True
    except Exception as e:
        print(f"  ✗ VideoClipExtractor 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("TeslaClip 功能测试")
    print("=" * 60)
    
    results = []
    
    results.append(test_import())
    results.append(test_batch_processor_init())
    results.append(test_video_clip_extractor())
    
    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过！")
        print("\n现在可以安全使用:")
        print("  python3 main.py -i video.mp4")
        print("  python3 main.py -i video.mp4 --extract-clips")
        return 0
    else:
        print("✗ 部分测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
