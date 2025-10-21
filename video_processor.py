"""
视频运动检测核心模块
使用OpenCV实现帧差法检测视频中的运动区域
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List


class MotionDetector:
    """运动检测器类，负责检测视频帧中的运动"""
    
    def __init__(self, sensitivity: int = 25, min_area: int = 500):
        """
        初始化运动检测器
        
        Args:
            sensitivity: 运动检测灵敏度 (0-100)，值越小越敏感
            min_area: 最小运动区域面积（像素），小于此值的运动被忽略
        """
        self.sensitivity = sensitivity
        self.min_area = min_area
        self.prev_frame = None
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=False
        )
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, np.ndarray, List]:
        """
        检测单帧中的运动
        
        Args:
            frame: 输入视频帧 (BGR格式)
            
        Returns:
            (has_motion, motion_mask, contours): 是否检测到运动、运动区域的掩码、检测到的轮廓列表
        """
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # 如果是第一帧，初始化
        if self.prev_frame is None:
            self.prev_frame = gray
            return False, np.zeros_like(gray), []
        
        # 计算帧差
        frame_diff = cv2.absdiff(self.prev_frame, gray)
        
        # 二值化
        threshold_value = self.sensitivity * 2.55  # 转换为0-255范围
        _, thresh = cv2.threshold(frame_diff, threshold_value, 255, cv2.THRESH_BINARY)
        
        # 形态学操作，去除噪声
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        thresh = cv2.erode(thresh, kernel, iterations=1)
        
        # 查找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤出足够大的运动区域轮廓
        has_motion = False
        motion_contours = []
        for contour in contours:
            if cv2.contourArea(contour) > self.min_area:
                has_motion = True
                motion_contours.append(contour)
        
        # 更新前一帧
        self.prev_frame = gray
        
        return has_motion, thresh, motion_contours
    
    def reset(self):
        """重置检测器状态"""
        self.prev_frame = None
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=False
        )


class VideoProcessor:
    """视频处理器类，负责处理视频文件并提取活动帧"""
    
    def __init__(self, 
                 sensitivity: int = 25,
                 min_interval: float = 1.0,
                 fps: int = 2,
                 min_area: int = 500):
        """
        初始化视频处理器
        
        Args:
            sensitivity: 运动检测灵敏度 (0-100)
            min_interval: 两次截图之间的最小时间间隔（秒）
            fps: 处理帧率，每秒处理的帧数
            min_area: 最小运动区域面积
        """
        self.sensitivity = sensitivity
        self.min_interval = min_interval
        self.process_fps = fps
        self.min_area = min_area
        self.motion_detector = MotionDetector(sensitivity, min_area)
    
    def process_video(self, 
                     video_path: str,
                     callback=None,
                     output_video_path: Optional[str] = None) -> list:
        """
        处理单个视频文件，提取包含运动的截图
        
        Args:
            video_path: 视频文件路径
            callback: 回调函数，接收 (frame, timestamp, has_motion, current_frame, total_frames) 参数
            output_video_path: 已弃用，保留用于向后兼容
            
        Returns:
            提取的帧列表，每个元素为 (frame, timestamp) 元组
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        # 获取视频信息
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 计算帧间隔
        frame_interval = int(video_fps / self.process_fps) if video_fps > 0 else 1
        
        extracted_frames = []
        last_extract_time = -self.min_interval  # 确保第一帧可以被提取
        frame_count = 0
        
        self.motion_detector.reset()
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # 只处理间隔帧
            if frame_count % frame_interval == 0:
                current_time = frame_count / video_fps if video_fps > 0 else 0
                
                # 检测运动
                has_motion, motion_mask, contours = self.motion_detector.detect_motion(frame)
                
                # 如果检测到运动
                if has_motion:
                    # 创建带有运动检测标注的帧（绿色矩形框）
                    annotated_frame = self._draw_motion_contours(frame.copy(), contours, current_time)
                    
                    # 提取截图（如果距离上次提取已超过最小间隔）
                    if (current_time - last_extract_time) >= self.min_interval:
                        extracted_frames.append((annotated_frame.copy(), current_time))
                        last_extract_time = current_time
                
                # 调用回调函数（每个间隔帧调用一次）
                if callback:
                    callback(frame, current_time, has_motion, frame_count, total_frames)
            
            frame_count += 1
        
        cap.release()
            
        return extracted_frames
    
    def _draw_motion_contours(self, frame: np.ndarray, contours: list, current_time: float) -> np.ndarray:
        """
        在帧上绘制运动检测的轮廓和相关信息
        
        Args:
            frame: 要绘制的帧
            contours: 运动轮廓列表
            current_time: 当前时间（秒）
            
        Returns:
            绘制后的帧
        """
        # 只为每个轮廓绘制绿色矩形边界框
        for contour in contours:
            # 获取边界框
            x, y, w, h = cv2.boundingRect(contour)
            
            # 只绘制绿色边界框
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 添加时间戳（左上角，白色）
        timestamp_str = self.format_timestamp(current_time)
        cv2.putText(frame, timestamp_str, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame
    
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """
        将秒数转换为时间戳格式字符串
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化的时间戳字符串 (例如: "00h05m30s")
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}h{minutes:02d}m{secs:02d}s"
    
    @staticmethod
    def save_frame(frame: np.ndarray, 
                   output_path: str,
                   quality: int = 95) -> bool:
        """
        保存帧为图像文件
        
        Args:
            frame: 要保存的帧
            output_path: 输出文件路径
            quality: JPEG质量 (0-100)
            
        Returns:
            是否成功保存
        """
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            return cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        else:
            return cv2.imwrite(output_path, frame)
