# TeslaClip v1.0.0 Release Notes

## 🎉 First Stable Release!

We're excited to announce the first stable release of **TeslaClip** - an intelligent activity frame extractor for Tesla Dashcam and Sentry Mode videos!

## 🚀 What is TeslaClip?

TeslaClip automatically extracts key moments from your Tesla recordings using advanced computer vision. No more watching hours of footage - just get the important frames with precise timestamps!

## ✨ Key Features

### 🎥 Smart Motion Detection
- Advanced frame differencing algorithm using OpenCV
- Background subtraction adapts to lighting changes
- Configurable sensitivity (0-100 scale)
- Noise filtering for accurate detection

### 📸 Automatic Screenshot Extraction
- Saves key frames when motion is detected
- Timestamp-based filenames: `video_00h05m30s.jpg`
- Supports JPG and PNG formats
- Prevents duplicate captures with smart interval control

### 📦 Batch Processing
- Process single files or entire directories
- Real-time progress tracking
- Processing statistics and summary
- Recursive directory scanning

### ⚙️ Flexible Configuration
Four optimized presets included:
- **Sentry Mode**: Sensitive settings for parking surveillance
- **Driving Mode**: Filters normal road changes
- **Sensitive**: Captures all subtle movements
- **Conservative**: Only major events

### 👁️ Preview Mode
- Real-time visualization of detection
- Perfect for parameter tuning
- Visual debugging support

### 🌍 Dual-Language Documentation
- Complete English documentation
- Full Chinese documentation (中文文档)
- Quick start guides
- Configuration examples

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/namezzy/TeslaClip.git
cd TeslaClip

# Quick install
./install.sh

# Or manual install
pip3 install opencv-python numpy tqdm
```

## 🎯 Quick Start

```bash
# Process a video
python3 main.py -i your_video.mp4

# Process entire folder
python3 main.py -i /path/to/videos -o ./output

# Preview mode
python3 main.py -i video.mp4 --preview

# Sentry mode optimized
python3 main.py -i sentry.mp4 -s 18 --min-interval 3.0
```

## 📋 What's Included

- **Core Module**: `video_processor.py` - Motion detection engine
- **Main Script**: `main.py` - CLI interface
- **Installation**: `install.sh` - Auto-setup script
- **Demo**: `run_demo.sh` - One-click demo
- **Test Generator**: `create_test_video.py` - Create test videos
- **Documentation**: Comprehensive guides in EN/CN
- **Configuration**: Preset examples for different scenarios

## 🛠️ Technical Details

- **Language**: Python 3.8+
- **Core Library**: OpenCV 4.8+
- **Dependencies**: NumPy, tqdm
- **Supported Formats**: MP4, AVI, MOV, MKV, FLV, WMV, M4V
- **Platforms**: Linux, macOS, Windows

## 📚 Documentation

- [README (English)](./README.md)
- [README (中文)](./README_CN.md)
- [Quick Start Guide](./QUICKSTART.md)
- [How to Run (如何运行)](./如何运行.md)
- [Changelog](./CHANGELOG.md)

## 🐛 Known Issues

None reported yet! Please open an issue if you find any bugs.

## 🔮 Future Plans

- [ ] Deep learning object detection (YOLO/MobileNet)
- [ ] Multi-camera synchronization for Tesla's 4-camera system
- [ ] HTML report generation with timeline
- [ ] GPU acceleration support
- [ ] Intelligent classification (person, vehicle, animal)
- [ ] Mobile app support

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details

## 🙏 Acknowledgments

Thank you to all Tesla owners who inspired this project!

## 🔗 Links

- **GitHub**: https://github.com/namezzy/TeslaClip
- **Issues**: https://github.com/namezzy/TeslaClip/issues
- **Discussions**: https://github.com/namezzy/TeslaClip/discussions

---

## 📦 Download

Download the source code or install via git:

```bash
git clone --branch v1.0.0 https://github.com/namezzy/TeslaClip.git
```

Or download the release assets from GitHub.

---

<div align="center">

**Made with ❤️ for Tesla owners**

If you find this useful, please ⭐ star the repo!

**Happy Extracting! 🚗⚡**

</div>
