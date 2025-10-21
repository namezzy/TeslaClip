# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🚀 Improved - 运动检测连续性和边界框优化
- **大幅改进运动检测质量和视觉效果**
  - 🔗 增强形态学操作：3次小核膨胀 + 2次大核膨胀，确保检测连续性
  - 📏 扩大边界框：动态边距（15%+15px），完整框住运动物体
  - 🎯 降低阈值：最小面积从 500 降到 300 像素，捕捉更多运动
  - 💪 更粗线条：边框从 2 像素增到 3 像素，更清晰可见
  - ✅ 解决断续标注问题
  - ✅ 解决遗漏小物体问题
  - ✅ 解决矩形框太小问题

### ✨ Enhanced - 视频片段全程运动标注
- **实现视频片段持续运动检测和标注功能**
  - 🎯 整个视频片段（前后缓冲区）持续进行运动检测
  - 🟢 实时标注：检测到运动立即绘制绿色矩形框
  - 🔧 预热机制：处理前 5 帧确保检测器状态稳定
  - ♻️ 连续检测：对每一帧都进行运动分析
  - 📹 完整追踪：不错过事件前后的任何运动
  - ✅ 比之前"只在事件期间标注"更全面
  
### 🐛 Fixed - 运动标注问题修复历史
- ~~第一次尝试：只在事件期间标注~~ - 遗漏事件外的运动
- ~~第二次尝试：整个片段标注但有bug~~ - 标注错乱
- ✅ 最终方案：预热 + 全程检测，标注准确且完整

### 🔧 Fixed - 重要功能修正 v2
- **截图轮廓简化** - 根据用户反馈优化标注
  - ❌ 移除不规则轮廓绘制
  - ❌ 移除红色边界框
  - ❌ 移除面积标签和轮廓计数
  - ✅ 只保留绿色矩形边界框
  - ✅ 保留时间戳
  - 画面更简洁清晰
  
- **视频输出重新设计** - 完全重写视频处理逻辑
  - ❌ 移除旧的逐帧视频输出功能
  - ✅ 新增独立的视频片段提取器 (`video_clip_extractor.py`)
  - ✅ 检测连续运动超过 N 秒的事件
  - ✅ 提取事件前后各 M 秒的视频片段
  - ✅ 支持自定义参数（运动时长、前后缓冲时间）
  - 更实用、更易于分析

### ✨ Added
- **VideoClipExtractor 模块** - 独立的视频片段提取功能
  - `detect_motion_events()`: 检测所有运动事件
  - `extract_clip()`: 提取单个事件的视频片段
  - `process_video()`: 完整处理流程
  - 支持批量处理
  - 每个事件生成独立的视频文件

### 📚 Documentation
- 添加 VIDEO_CLIP_FEATURE.md 详细说明新功能
- 更新命令行参数说明

### 🔧 Fixed - 重要功能修正
- **截图轮廓标注** - 所有提取的截图现在都包含运动检测可视化
  - 绿色轮廓标记运动区域
  - 红色边界框和黄色面积标签
  - 白色时间戳和轮廓计数
  
- **视频输出功能修正** - 重新实现视频输出逻辑
  - ❌ 旧实现：输出所有帧（错误理解需求）
  - ✅ 新实现：只输出检测到运动的帧
  - 输出视频大小减少 70-90%
  - 观看效率显著提升，无需跳过静止内容
  
- **文件组织优化** - 改进批量处理的输出结构
  - 为每个输入视频创建独立的子文件夹
  - 文件夹命名与视频文件名相同
  - 每个文件夹包含该视频的截图和输出视频
  - 避免多个视频文件混在一起

### 📚 Documentation
- 添加 FEATURE_CORRECTION.md 详细说明功能修正
- 更新输出示例和使用说明

### ✨ Added
- **Video Output with Motion Visualization** - Generate annotated videos showing detected motion
  - Draws green contours around motion regions
  - Displays red bounding boxes for each motion area
  - Shows area labels (in pixels) for each contour
  - Overlays timestamp (HH:MM:SS) and contour count on each frame
  - Output filename format: `{video_name}_motion_detected.mp4`
  - Enabled via `--output-video` CLI flag
  - See [FEATURE_VIDEO_OUTPUT.md](./FEATURE_VIDEO_OUTPUT.md) for full documentation
  
- **Enhanced Motion Detection API** - MotionDetector now returns contours list
  - New return signature: `(has_motion, motion_mask, contours)`
  - Enables advanced visualization and analysis
  
### 📚 Documentation
- Added comprehensive video output feature documentation
- Updated README.md and README_CN.md with new feature descriptions
- Added usage examples for video output mode

### 🐛 Fixed
- **Progress Bar Display (Updated)** - Fixed multiple progress bar issues
  - Short videos (e.g., 10s) now correctly show 100% completion
  - Previous fix for ~7% stuck issue
  - Ensures all frames are accounted for in progress calculation
  
### ✨ Enhanced
- **Enhanced Progress Information** - Rich real-time processing details
  - Processing speed display (frames/sec)
  - Estimated time remaining (seconds)
  - Current video timestamp (MM:SS format)
  - All displayed using tqdm's set_postfix for clean output
  
### 📚 Previous Documentation
- See [BUGFIX_PROGRESS_ENHANCEMENT.md](./BUGFIX_PROGRESS_ENHANCEMENT.md) for details

## [1.0.0] - 2025-10-21

### 🎉 Initial Release

This is the first stable release of TeslaClip - an intelligent activity frame extractor for Tesla Dashcam and Sentry Mode videos.

### ✨ Features

#### Core Functionality
- **Smart Motion Detection** - Advanced frame differencing algorithm using OpenCV
  - Background subtraction to adapt to lighting changes
  - Morphological operations for noise filtering
  - Configurable sensitivity (0-100 scale)
  - Minimum motion area threshold

- **Auto Screenshot Extraction** - Saves key frames when activity is detected
  - Timestamp-based filename format: `{video_name}_{HH}h{MM}m{SS}s.{format}`
  - JPEG and PNG format support
  - Configurable JPEG quality

- **Batch Processing** - Process multiple videos efficiently
  - Single file or entire directory support
  - Recursive directory scanning
  - Real-time progress tracking with tqdm
  - Processing statistics and summary

#### Configuration & Customization
- **Flexible Parameters**
  - Sensitivity control (0-100)
  - Minimum interval between captures (seconds)
  - Processing frame rate (FPS)
  - Output format (JPG/PNG)
  
- **Preset Configurations** (`config_example.py`)
  - Sentry mode preset (sensitivity: 18, interval: 3.0s)
  - Driving mode preset (sensitivity: 30, interval: 1.5s)
  - Sensitive preset (sensitivity: 15, interval: 0.5s)
  - Conservative preset (sensitivity: 35, interval: 5.0s)

#### Developer Tools
- **Preview Mode** - Real-time visualization of motion detection
  - Visual debugging for parameter tuning
  - Press 'q' to quit preview

- **Test Video Generator** - Create test videos with motion
  - Automated test video creation script
  - Includes motion sequences for validation

#### Documentation
- **Comprehensive Documentation**
  - English README with badges and visual formatting
  - Chinese README (README_CN.md)
  - Quick Start Guide (QUICKSTART.md)
  - Detailed run instructions (如何运行.md)
  - Copilot instructions for AI coding assistants

#### Utilities
- **Installation Scripts**
  - `install.sh` - Automatic dependency installation
  - `run_demo.sh` - One-click demo execution
  - Requirements file for pip installation

### 🛠️ Technical Stack
- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- tqdm 4.65+

### 📦 Supported Video Formats
- MP4, AVI, MOV, MKV, FLV, WMV, M4V

### 🌍 Language Support
- English documentation
- Chinese documentation (中文文档)

### 📄 License
- MIT License

### 🔗 Links
- GitHub Repository: https://github.com/namezzy/TeslaClip
- Issue Tracker: https://github.com/namezzy/TeslaClip/issues

---

## Future Releases

See [Roadmap](./README.md#-roadmap) for planned features:
- Deep learning object detection (YOLO/MobileNet)
- Multi-camera synchronization
- HTML report generation
- GPU acceleration
- Intelligent classification
- Mobile app support
