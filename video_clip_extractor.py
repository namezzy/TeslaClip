"""
视频片段提取器
独立模块，用于检测连续运动并提取视频片段
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from video_processor import MotionDetector


@dataclass
class MotionEvent:
    """运动事件记录"""
    start_time: float  # 运动开始时间（秒）
    end_time: float    # 运动结束时间（秒）
    duration: float    # 持续时间（秒）
    start_frame: int   # 开始帧号
    end_frame: int     # 结束帧号
    
    def __repr__(self):
        return f"MotionEvent({self.start_time:.1f}s-{self.end_time:.1f}s, {self.duration:.1f}s)"


class VideoClipExtractor:
    """视频片段提取器
    
    检测连续运动超过指定时长的事件，并提取前后指定时长的视频片段
    """
    
    def __init__(self,
                 sensitivity: int = 25,
                 min_motion_duration: float = 3.0,
                 clip_before: float = 20.0,
                 clip_after: float = 20.0,
                 min_area: int = 500):
        """
        初始化视频片段提取器
        
        Args:
            sensitivity: 运动检测灵敏度 (0-100)
            min_motion_duration: 触发提取的最小连续运动时长（秒）
            clip_before: 运动事件前提取的时长（秒）
            clip_after: 运动事件后提取的时长（秒）
            min_area: 最小运动区域面积
        """
        self.sensitivity = sensitivity
        self.min_motion_duration = min_motion_duration
        self.clip_before = clip_before
        self.clip_after = clip_after
        self.min_area = min_area
        self.motion_detector = MotionDetector(sensitivity, min_area)
    
    def detect_motion_events(self, video_path: str, fps: int = 2) -> List[MotionEvent]:
        """
        检测视频中的所有运动事件
        
        Args:
            video_path: 视频文件路径
            fps: 处理帧率（每秒处理的帧数）
            
        Returns:
            运动事件列表
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = int(video_fps / fps) if video_fps > 0 else 1
        
        self.motion_detector.reset()
        
        motion_events = []
        current_motion_start = None
        current_motion_start_frame = None
        last_motion_time = None
        frame_count = 0
        
        print(f"分析视频中的运动事件...")
        print(f"最小连续运动时长: {self.min_motion_duration}秒")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 只处理间隔帧
            if frame_count % frame_interval == 0:
                current_time = frame_count / video_fps if video_fps > 0 else 0
                
                # 检测运动
                has_motion, _, _ = self.motion_detector.detect_motion(frame)
                
                if has_motion:
                    # 如果是新的运动事件
                    if current_motion_start is None:
                        current_motion_start = current_time
                        current_motion_start_frame = frame_count
                    
                    last_motion_time = current_time
                else:
                    # 如果之前有运动，现在停止了
                    if current_motion_start is not None and last_motion_time is not None:
                        duration = last_motion_time - current_motion_start
                        
                        # 如果持续时间超过阈值，记录事件
                        if duration >= self.min_motion_duration:
                            event = MotionEvent(
                                start_time=current_motion_start,
                                end_time=last_motion_time,
                                duration=duration,
                                start_frame=current_motion_start_frame,
                                end_frame=int(last_motion_time * video_fps)
                            )
                            motion_events.append(event)
                            print(f"  检测到运动事件: {event}")
                        
                        # 重置状态
                        current_motion_start = None
                        current_motion_start_frame = None
                        last_motion_time = None
            
            frame_count += 1
        
        # 处理视频结束时还在进行的运动
        if current_motion_start is not None and last_motion_time is not None:
            duration = last_motion_time - current_motion_start
            if duration >= self.min_motion_duration:
                event = MotionEvent(
                    start_time=current_motion_start,
                    end_time=last_motion_time,
                    duration=duration,
                    start_frame=current_motion_start_frame,
                    end_frame=int(last_motion_time * video_fps)
                )
                motion_events.append(event)
                print(f"  检测到运动事件: {event}")
        
        cap.release()
        
        print(f"共检测到 {len(motion_events)} 个运动事件")
        return motion_events
    
    def extract_clip(self,
                    video_path: str,
                    event: MotionEvent,
                    output_path: str,
                    draw_contours: bool = True) -> bool:
        """
        提取单个运动事件的视频片段
        
        Args:
            video_path: 原始视频路径
            event: 运动事件
            output_path: 输出视频路径
            draw_contours: 是否绘制运动检测轮廓
            
        Returns:
            是否成功提取
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"错误: 无法打开视频 {video_path}")
            return False
        
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 计算提取范围（前后各加指定时长）
        clip_start_time = max(0, event.start_time - self.clip_before)
        clip_end_time = event.end_time + self.clip_after
        
        clip_start_frame = int(clip_start_time * video_fps)
        clip_end_frame = int(clip_end_time * video_fps)
        
        print(f"  提取片段: {clip_start_time:.1f}s - {clip_end_time:.1f}s " +
              f"(事件: {event.start_time:.1f}s - {event.end_time:.1f}s)")
        
        # 初始化视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, video_fps, (width, height))
        
        if not writer.isOpened():
            print(f"错误: 无法创建输出视频 {output_path}")
            cap.release()
            return False
        
        # 重置运动检测器
        self.motion_detector.reset()
        
        # 定位到起始帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, clip_start_frame)
        
        frame_count = clip_start_frame
        written_frames = 0
        
        while frame_count <= clip_end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            
            current_time = frame_count / video_fps
            
            # 如果需要绘制轮廓，在整个视频中都进行运动检测和绘制
            if draw_contours:
                # 检测运动并获取轮廓
                has_motion, _, contours = self.motion_detector.detect_motion(frame)
                
                if has_motion and contours:
                    # 只绘制绿色矩形边界框
                    for contour in contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 添加时间戳
            timestamp_str = self._format_timestamp(current_time)
            cv2.putText(frame, timestamp_str, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            writer.write(frame)
            written_frames += 1
            frame_count += 1
        
        cap.release()
        writer.release()
        
        print(f"  成功提取 {written_frames} 帧")
        return True
    
    def process_video(self,
                     video_path: str,
                     output_dir: str,
                     fps: int = 2) -> List[str]:
        """
        处理视频，检测运动事件并提取所有片段
        
        Args:
            video_path: 输入视频路径
            output_dir: 输出目录
            fps: 处理帧率
            
        Returns:
            生成的视频片段路径列表
        """
        video_path = Path(video_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n处理视频: {video_path.name}")
        print("=" * 60)
        
        # 检测运动事件
        events = self.detect_motion_events(str(video_path), fps)
        
        if not events:
            print("未检测到符合条件的运动事件")
            return []
        
        # 提取每个事件的视频片段
        output_paths = []
        video_name = video_path.stem
        
        for i, event in enumerate(events, 1):
            output_filename = f"{video_name}_clip_{i:03d}_" + \
                            f"{self._format_timestamp(event.start_time).replace(':', '')}.mp4"
            output_path = output_dir / output_filename
            
            print(f"\n提取片段 {i}/{len(events)}:")
            if self.extract_clip(str(video_path), event, str(output_path)):
                output_paths.append(str(output_path))
        
        print(f"\n完成! 共生成 {len(output_paths)} 个视频片段")
        return output_paths
    
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """格式化时间戳为 HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def main():
    """测试函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python3 video_clip_extractor.py <video_file>")
        return
    
    video_path = sys.argv[1]
    output_dir = "./video_clips"
    
    extractor = VideoClipExtractor(
        sensitivity=25,
        min_motion_duration=3.0,  # 最小连续运动3秒
        clip_before=20.0,          # 前20秒
        clip_after=20.0            # 后20秒
    )
    
    clips = extractor.process_video(video_path, output_dir, fps=2)
    
    print(f"\n生成的视频片段:")
    for clip in clips:
        print(f"  - {clip}")


if __name__ == '__main__':
    main()
