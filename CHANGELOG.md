# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🐛 Fixed
- **Progress Bar Display** - Fixed progress bar stuck at low percentage (~7%)
  - Progress bar now correctly shows 0-100% during video processing
  - Updated progress calculation to account for frame intervals
  - Affects both single video and batch processing modes
  - See [BUGFIX_PROGRESS_BAR.md](./BUGFIX_PROGRESS_BAR.md) for details

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
