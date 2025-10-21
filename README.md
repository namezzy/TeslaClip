# TeslaClip 🚗⚡

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

**Intelligent Activity Frame Extractor for Tesla Dashcam & Sentry Mode Videos**

[English](#english) | [中文文档](./README_CN.md)

</div>

---

## 📖 English

### 🎯 What is TeslaClip?

TeslaClip is a powerful computer vision tool that automatically extracts key moments from Tesla dashcam and Sentry Mode recordings. Using advanced motion detection algorithms, it helps you quickly discover what happened around your vehicle without watching hours of footage.

### ✨ Key Features

- 🎥 **Smart Motion Detection** - Advanced frame differencing algorithm detects activity automatically
- 📸 **Auto Screenshot Extraction** - Saves key frames when motion is detected
- 🎬 **Video Output with Contours** - Generate videos with motion detection visualization (NEW!)
- ⏰ **Timestamp Naming** - Files named with video timestamp (e.g., `00h05m30s.jpg`) for easy navigation
- 📦 **Batch Processing** - Process multiple videos or entire folders at once
- ⚙️ **Configurable Parameters** - Fine-tune sensitivity, interval, and FPS for different scenarios
- 📊 **Progress Tracking** - Real-time progress bars and statistics
- 👁️ **Preview Mode** - Visual debugging to optimize detection settings

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/namezzy/TeslaClip.git
cd TeslaClip

# Quick install (recommended)
./install.sh

# Or install manually
pip3 install opencv-python numpy tqdm
```

#### Basic Usage

```bash
# Process a single video
python3 main.py -i your_video.mp4

# Process entire folder
python3 main.py -i /path/to/tesla/videos -o ./output

# Generate video with motion contours (NEW!)
python3 main.py -i video.mp4 --output-video

# Preview mode for parameter tuning
python3 main.py -i video.mp4 --preview
```

#### Create Test Video

```bash
# Generate a test video with motion
python3 create_test_video.py

# Run demo
./run_demo.sh
```

### 📋 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input video file or directory | Required |
| `-o, --output` | Output directory for screenshots | `./extracted_frames` |
| `-s, --sensitivity` | Motion detection sensitivity (0-100, lower = more sensitive) | `25` |
| `--min-interval` | Minimum interval between screenshots (seconds) | `1.0` |
| `--fps` | Processing frame rate | `2` |
| `--format` | Output format (jpg/png) | `jpg` |
| `--preview` | Enable real-time preview window | `false` |
| `--output-video` | Generate video with motion detection visualization | `false` |

### 🎨 Usage Examples

#### Sentry Mode (Parking)
```bash
python3 main.py -i sentry_video.mp4 -s 18 --min-interval 3.0
```
*More sensitive settings for static camera, captures people/vehicles approaching*

#### Driving Mode
```bash
python3 main.py -i driving_video.mp4 -s 30 --min-interval 1.5
```
*Filters normal road changes, captures only significant events*

#### High Sensitivity
```bash
python3 main.py -i video.mp4 -s 15 --min-interval 0.5 --fps 4
```
*Captures all subtle changes (generates more screenshots)*

### 📂 Output Structure

```
extracted_frames/
├── video1/                          # Each video gets its own folder
│   ├── video1_00h05m30s.jpg       # Screenshot with contours at 5min 30sec
│   ├── video1_00h07m15s.jpg       # Screenshot with contours at 7min 15sec
│   └── video1_motion_detected.mp4 # Video with only motion frames
├── video2/
│   ├── video2_00h00m45s.jpg
│   └── video2_motion_detected.mp4
└── ...
```

**Key Features:**
- 📁 **Independent folders** - Each video gets its own subfolder
- 🎨 **Annotated screenshots** - All screenshots include motion contours, bounding boxes, and labels
- 🎬 **Motion-only videos** - Output videos contain only frames with detected motion (70-90% smaller)

Filename format: `{video_name}_{HH}h{MM}m{SS}s.{format}`

### 🎬 Video Output Feature (NEW!)

Generate annotated videos showing motion detection in real-time:

```bash
python3 main.py -i video.mp4 --output-video -s 25
```

**Key Behavior:**
- ⚡ **Motion frames only** - Output video contains ONLY frames where motion was detected
- 📉 **Smaller file size** - Typically 70-90% smaller than original
- ⏱️ **Time efficient** - Watch only the action, skip all static content

**Visualization includes:**
- 🟢 **Green contours** - Detected motion boundaries
- 🔴 **Red bounding boxes** - Minimum enclosing rectangles
- 🔢 **Area labels** - Size of each motion region in pixels
- ⏱️ **Timestamps** - Current video time (HH:MM:SS)
- 📊 **Contour count** - Number of motion regions detected

**Output:** `{video_name}_motion_detected.mp4` (in dedicated folder)

**Use cases:**
- Quick review of parking lot events (1 hour → 5 minutes)
- Create highlight reels from driving footage
- Insurance evidence with motion annotations
- Debug and tune sensitivity parameters visually

For detailed documentation, see [FEATURE_CORRECTION.md](./FEATURE_CORRECTION.md)

### 🔧 How It Works

1. **Frame Differencing** - Compares consecutive frames to detect changes
2. **Background Modeling** - Adapts to gradual lighting changes
3. **Noise Filtering** - Removes small motion artifacts
4. **Smart Interval** - Prevents duplicate captures of the same event

```
Video Input → Motion Detection → Key Frame Extraction → Timestamp Naming → Screenshot Output
```

### 🎯 Use Cases

- 🚗 Find moments when people/vehicles approach your parked Tesla
- 📹 Extract key events from driving footage
- 🔍 Review what happened during specific time periods
- 📊 Create video summaries or highlight reels

### ⚙️ Configuration Presets

The `config_example.py` includes optimized presets:

| Preset | Sensitivity | Interval | FPS | Best For |
|--------|-------------|----------|-----|----------|
| `sentry` | 18 | 3.0s | 2 | Parking/Sentry Mode |
| `driving` | 30 | 1.5s | 3 | Driving footage |
| `sensitive` | 15 | 0.5s | 4 | Capture all changes |
| `conservative` | 35 | 5.0s | 1 | Only major events |

### 🛠️ Technical Stack

- **Python 3.8+** - Core language
- **OpenCV** - Video processing and motion detection
- **NumPy** - Numerical computations
- **tqdm** - Progress bars

### 📚 Documentation

- [Quick Start Guide](./QUICKSTART.md) - Detailed setup instructions
- ### 📚 Documentation

- [How to Run](./How_to_run.md) - Quick start tutorial
- [Documentation Index](./docs/README.md) - Complete technical documentation
  - [Video Clip Feature Guide](./docs/VIDEO_CLIP_FEATURE.md) - Video clip extraction feature
  - [Changelog](./docs/CHANGELOG.md) - Version history and updates
  - [Quick Start](./docs/QUICKSTART.md) - Detailed quick start guide
  - [Bug Fix Records](./docs/) - All bug fixes and solutions

### 🐛 Troubleshooting

#### No screenshots extracted
- Lower sensitivity: `-s 15`
- Check if video actually has motion

#### Too many duplicate screenshots
- Increase sensitivity: `-s 35`
- Increase interval: `--min-interval 3.0`

#### Program runs slowly
- Reduce FPS: `--fps 1`
- Process specific files only

### 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests

### 📝 Roadmap

- [ ] Deep learning object detection (YOLO/MobileNet)
- [ ] Multi-camera sync for Tesla's 4-camera system
- [ ] HTML report generation with timeline visualization
- [ ] GPU acceleration support
- [ ] Intelligent classification (person, vehicle, animal)
- [ ] Mobile app support

### 🙏 Acknowledgments

Inspired by the need to efficiently review Tesla's extensive dashcam recordings.

### 📄 License

MIT License - feel free to use and modify!

### 🔗 Links

- **GitHub**: https://github.com/namezzy/TeslaClip
- **Issues**: https://github.com/namezzy/TeslaClip/issues

---

<div align="center">

**Made with ❤️ for Tesla owners**

If you find this useful, please ⭐ star the repo!

</div>
