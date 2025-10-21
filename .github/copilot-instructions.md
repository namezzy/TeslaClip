# Copilot Instructions for Tesla Video Activity Extractor

## Project Overview
This is a Python-based computer vision tool that extracts activity frames from Tesla dashcam and Sentry Mode videos. It uses OpenCV motion detection to identify and save key moments with timestamp-based filenames.

## Architecture

### Core Components
- **`video_processor.py`**: Contains motion detection and video processing logic
  - `MotionDetector`: Frame-difference based motion detection with background subtraction
  - `VideoProcessor`: Orchestrates video analysis, frame extraction, and timestamp formatting
- **`main.py`**: CLI interface and batch processing orchestration
  - `BatchProcessor`: Handles multiple videos, progress tracking, and file management
  - Command-line argument parsing with validation

### Key Design Patterns
- **Callback-based processing**: `VideoProcessor.process_video()` accepts a callback for real-time progress updates and preview display
- **Stateful detection**: `MotionDetector` maintains previous frame state for accurate frame-differencing
- **Timestamp formatting**: Frames are named `{video_name}_{HH}h{MM}m{SS}s.{format}` for easy video navigation

## Configuration Parameters

### Motion Detection Tuning
- `sensitivity` (0-100): Lower = more sensitive. Default 25 is balanced
  - Sentry mode (static camera): 15-20 recommended
  - Driving footage: 25-35 to filter normal road changes
- `min_interval` (seconds): Prevents duplicate captures of same event
  - Sentry: 3-5s (slower activity)
  - Driving: 1-2s (rapid changes)
- `fps`: Processing frame rate (default 2) - higher = more CPU but better detection
- `min_area`: Minimum motion region pixels (default 500) - filters small noise

### Algorithm Details
1. **Frame Differencing**: Compares consecutive grayscale frames after Gaussian blur (21x21 kernel)
2. **Binary Thresholding**: `sensitivity * 2.55` converts 0-100 scale to 0-255 threshold
3. **Morphological Operations**: Dilation (2 iterations) then erosion (1 iteration) removes noise
4. **Contour Analysis**: Only triggers extraction if contour area > `min_area`

## Development Workflows

### Testing Motion Detection
```bash
# Use preview mode to visually tune sensitivity
python main.py -i test_video.mp4 --preview -s 20 --min-interval 1.0
```

### Batch Processing
```bash
# Process entire directory with optimized settings
python main.py -i /path/to/tesla/videos -o ./output -s 25 --fps 2
```

### Adding New Features
- **Object detection**: Extend `MotionDetector` to use YOLO/MobileNet for person/vehicle classification
- **Multi-camera sync**: Modify `BatchProcessor` to group Tesla's 4-camera angles by timestamp
- **HTML report generation**: Add post-processing step to create visual timeline from extracted frames

## Common Issues

### False Positives
- Camera shake/vibration: Increase `sensitivity` value
- Lighting changes: Background subtractor (`createBackgroundSubtractorMOG2`) helps but may need tuning
- Tree shadows/weather: Increase `min_area` to require larger motion regions

### Performance
- High CPU usage: Reduce `fps` parameter (process fewer frames per second)
- Slow on large files: OpenCV reads frames sequentially; consider parallel video processing

## Dependencies
- `opencv-python` (4.8.0+): Video I/O and computer vision algorithms
- `numpy` (1.24.0+): Array operations for frame manipulation
- `tqdm` (4.65.0+): Progress bar display

## File Output Structure
```
extracted_frames/
├── front_camera_00h05m30s.jpg  # Front camera at 5min 30sec
├── front_camera_00h07m15s.jpg
└── rear_camera_00h00m45s.jpg
```

## Code Style Notes
- Type hints used throughout for clarity
- Docstrings follow Google style (Args/Returns sections)
- Path handling uses `pathlib.Path` for cross-platform compatibility
- Error handling includes user-friendly messages in Chinese
