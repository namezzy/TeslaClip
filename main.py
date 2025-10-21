"""
主程序入口
处理命令行参数，批量处理视频文件
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import List
import cv2
from tqdm import tqdm

from video_processor import VideoProcessor
from video_clip_extractor import VideoClipExtractor


class BatchProcessor:
    """批量视频处理器"""
    
    def __init__(self, 
                 output_dir: str,
                 sensitivity: int = 25,
                 min_interval: float = 1.0,
                 fps: int = 2,
                 image_format: str = 'jpg',
                 preview: bool = False,
                 extract_clips: bool = False,
                 min_motion_duration: float = 3.0,
                 clip_before: float = 20.0,
                 clip_after: float = 20.0):
        """
        初始化批量处理器
        
        Args:
            output_dir: 输出目录
            sensitivity: 运动检测灵敏度
            min_interval: 最小截图间隔
            fps: 处理帧率
            image_format: 输出图像格式
            preview: 是否显示预览窗口
            extract_clips: 是否提取视频片段
            min_motion_duration: 最小连续运动时长（秒）
            clip_before: 片段前提取时长（秒）
            clip_after: 片段后提取时长（秒）
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sensitivity = sensitivity
        self.min_interval = min_interval
        self.fps = fps
        self.image_format = image_format.lower()
        self.preview = preview
        self.extract_clips = extract_clips
        self.min_motion_duration = min_motion_duration
        self.clip_before = clip_before
        self.clip_after = clip_after
        self.processor = VideoProcessor(sensitivity, min_interval, fps)
        
        # 如果启用视频片段提取，初始化提取器
        if self.extract_clips:
            self.clip_extractor = VideoClipExtractor(
                sensitivity=sensitivity,
                min_motion_duration=min_motion_duration,
                clip_before=clip_before,
                clip_after=clip_after
            )
        
        self.total_videos = 0
        self.total_frames_extracted = 0
    
    def find_video_files(self, input_path: str) -> List[Path]:
        """
        查找所有视频文件
        
        Args:
            input_path: 输入路径（文件或目录）
            
        Returns:
            视频文件路径列表
        """
        input_path = Path(input_path)
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v'}
        
        if input_path.is_file():
            if input_path.suffix.lower() in video_extensions:
                return [input_path]
            else:
                print(f"警告: {input_path} 不是支持的视频格式")
                return []
        elif input_path.is_dir():
            video_files = []
            for ext in video_extensions:
                video_files.extend(input_path.rglob(f'*{ext}'))
                video_files.extend(input_path.rglob(f'*{ext.upper()}'))
            return sorted(set(video_files))
        else:
            print(f"错误: {input_path} 不存在")
            return []
    
    def process_single_video(self, video_path: Path) -> int:
        """
        处理单个视频文件
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            提取的帧数
        """
        print(f"\n正在处理: {video_path.name}")
        
        # 创建进度条
        pbar = None
        last_frame_count = 0
        start_time = None
        
        def progress_callback(frame, timestamp, has_motion, current_frame, total_frames):
            nonlocal pbar, last_frame_count, start_time
            if pbar is None:
                pbar = tqdm(total=total_frames, unit='帧', desc="处理进度")
                start_time = time.time()
            
            # 更新进度：计算自上次回调以来处理的帧数
            frames_processed = current_frame - last_frame_count
            if frames_processed > 0:
                pbar.update(frames_processed)
                last_frame_count = current_frame
            
            # 计算处理速度和预计剩余时间
            elapsed = time.time() - start_time
            if elapsed > 0 and current_frame > 0:
                fps = current_frame / elapsed
                remaining_frames = total_frames - current_frame
                eta = remaining_frames / fps if fps > 0 else 0
                
                # 格式化时间戳
                timestamp_str = f"{int(timestamp//60):02d}:{int(timestamp%60):02d}"
                
                # 更新进度条显示信息
                pbar.set_postfix({
                    '速度': f'{fps:.1f}帧/s',
                    '剩余': f'{int(eta)}s',
                    '时间': timestamp_str
                })
            
            # 如果启用预览
            if self.preview and has_motion:
                display_frame = frame.copy()
                cv2.putText(display_frame, f"Motion Detected at {timestamp:.1f}s", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Motion Detection Preview', display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return False
        
        try:
            # 为每个视频创建独立的输出文件夹
            video_name = video_path.stem
            video_output_dir = self.output_dir / video_name
            video_output_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. 提取截图（始终执行）
            extracted_frames = self.processor.process_video(
                str(video_path),
                callback=progress_callback,
                output_video_path=None  # 不再使用旧的视频输出功能
            )
            
            # 确保进度条达到100%
            if pbar:
                cap = cv2.VideoCapture(str(video_path))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()
                
                remaining = total_frames - last_frame_count
                if remaining > 0:
                    pbar.update(remaining)
                
                pbar.close()
            
            # 保存提取的帧到视频专属文件夹
            saved_count = 0
            
            for frame, timestamp in extracted_frames:
                timestamp_str = VideoProcessor.format_timestamp(timestamp)
                output_filename = f"{video_name}_{timestamp_str}.{self.image_format}"
                output_path = video_output_dir / output_filename
                
                if VideoProcessor.save_frame(frame, str(output_path)):
                    saved_count += 1
                else:
                    print(f"警告: 无法保存 {output_path}")
            
            # 显示截图提取结果
            result_info = f"✓ 截图提取完成: {saved_count} 张"
            print(result_info)
            
            # 2. 如果启用视频片段提取
            if self.extract_clips:
                print(f"\n开始提取视频片段...")
                clips_output_dir = video_output_dir / "clips"
                clips = self.clip_extractor.process_video(
                    str(video_path),
                    str(clips_output_dir),
                    fps=self.fps
                )
                
                if clips:
                    print(f"✓ 视频片段提取完成: {len(clips)} 个片段")
                    clips_size = sum(os.path.getsize(c) for c in clips) / (1024 * 1024)
                    print(f"  总大小: {clips_size:.2f} MB")
            
            print(f"  输出目录: {video_output_dir}\n")
            
            # 显示结果信息
            result_info = f"✓ 完成: 提取了 {saved_count} 个活动帧"
            if self.output_video and output_video_path and os.path.exists(output_video_path):
                video_size = os.path.getsize(output_video_path) / (1024 * 1024)  # MB
                result_info += f"，生成视频 {video_size:.2f}MB"
            result_info += f"\n  输出目录: {video_output_dir}"
            print(result_info)
            return saved_count
            
        except Exception as e:
            if pbar:
                pbar.close()
            print(f"✗ 错误: 处理视频时出错 - {e}")
            return 0
        finally:
            if self.preview:
                cv2.destroyAllWindows()
    
    def process_all(self, input_path: str):
        """
        批量处理所有视频
        
        Args:
            input_path: 输入路径
        """
        video_files = self.find_video_files(input_path)
        
        if not video_files:
            print("未找到视频文件")
            return
        
        print(f"找到 {len(video_files)} 个视频文件")
        print(f"输出根目录: {self.output_dir}")
        print(f"文件夹结构: 每个视频将创建独立的子文件夹")
        print(f"设置: 灵敏度={self.sensitivity}, 最小间隔={self.min_interval}s, FPS={self.fps}")
        if self.output_video:
            print(f"视频输出: 启用（只包含检测到运动的帧）")
        print("=" * 60)
        
        self.total_videos = len(video_files)
        
        for video_file in video_files:
            frames_extracted = self.process_single_video(video_file)
            self.total_frames_extracted += frames_extracted
        
        # 打印总结
        print("\n" + "=" * 60)
        print("处理完成！")
        print(f"总视频数: {self.total_videos}")
        print(f"总提取帧数: {self.total_frames_extracted}")
        print(f"输出根目录: {self.output_dir.absolute()}")
        print(f"每个视频的输出都在独立的子文件夹中")
        if self.extract_clips:
            print(f"视频片段: 已提取（连续运动>{self.min_motion_duration}秒的事件）")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='特斯拉视频活动提取器 - 从录像中提取包含活动的关键帧和视频片段',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 提取截图（带绿色矩形轮廓）
  python main.py -i video.mp4
  
  # 提取截图 + 视频片段（连续运动>3秒，提取前后20秒）
  python main.py -i video.mp4 --extract-clips
  
  # 自定义视频片段参数
  python main.py -i video.mp4 --extract-clips --motion-duration 5 --clip-before 30 --clip-after 30
  
  # 处理整个文件夹
  python main.py -i /path/to/videos -o ./output --extract-clips
  
  # 调整灵敏度和间隔
  python main.py -i video.mp4 -s 20 --min-interval 2.0
  
  # 启用预览模式（用于调试）
  python main.py -i video.mp4 --preview
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                       help='输入视频文件或文件夹路径')
    parser.add_argument('-o', '--output', default='./extracted_frames',
                       help='输出目录 (默认: ./extracted_frames)')
    parser.add_argument('-s', '--sensitivity', type=int, default=25,
                       help='运动检测灵敏度 (0-100, 默认: 25, 值越小越敏感)')
    parser.add_argument('--min-interval', type=float, default=1.0,
                       help='最小截图间隔（秒） (默认: 1.0)')
    parser.add_argument('--fps', type=int, default=2,
                       help='处理帧率，每秒处理的帧数 (默认: 2)')
    parser.add_argument('--format', choices=['jpg', 'png'], default='jpg',
                       help='输出图像格式 (默认: jpg)')
    parser.add_argument('--preview', action='store_true',
                       help='启用实时预览（用于调试参数）')
    
    # 视频片段提取参数
    parser.add_argument('--extract-clips', action='store_true',
                       help='提取视频片段（检测到连续运动时）')
    parser.add_argument('--motion-duration', type=float, default=3.0,
                       help='触发提取的最小连续运动时长（秒）(默认: 3.0)')
    parser.add_argument('--clip-before', type=float, default=20.0,
                       help='运动事件前提取的时长（秒）(默认: 20.0)')
    parser.add_argument('--clip-after', type=float, default=20.0,
                       help='运动事件后提取的时长（秒）(默认: 20.0)')
    
    args = parser.parse_args()
    
    # 验证参数
    if not 0 <= args.sensitivity <= 100:
        print("错误: 灵敏度必须在 0-100 之间")
        sys.exit(1)
    
    if args.min_interval < 0:
        print("错误: 最小间隔必须为非负数")
        sys.exit(1)
    
    if args.fps <= 0:
        print("错误: FPS 必须大于 0")
        sys.exit(1)
    
    if args.motion_duration <= 0:
        print("错误: 运动时长必须大于 0")
        sys.exit(1)
    
    # 创建批量处理器并执行
    processor = BatchProcessor(
        output_dir=args.output,
        sensitivity=args.sensitivity,
        min_interval=args.min_interval,
        fps=args.fps,
        image_format=args.format,
        preview=args.preview,
        extract_clips=args.extract_clips,
        min_motion_duration=args.motion_duration,
        clip_before=args.clip_before,
        clip_after=args.clip_after
    )
    
    try:
        processor.process_all(args.input)
    except KeyboardInterrupt:
        print("\n\n用户中断处理")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
