# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
