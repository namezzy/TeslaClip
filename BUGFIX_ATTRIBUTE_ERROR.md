# Bug 修复说明

## 🐛 问题描述

**错误信息**:
```
AttributeError: 'BatchProcessor' object has no attribute 'output_video'
```

**触发命令**:
```bash
python3 main.py -i video.mp4 --extract-clips
```

## 🔍 问题原因

在重构代码时，将 `BatchProcessor` 的 `__init__` 方法中的 `output_video` 参数改为了 `extract_clips`，但在以下两个地方仍然引用了已删除的 `self.output_video` 属性：

1. `process_single_video()` 方法中的结果显示代码
2. `process_all()` 方法中的启动信息显示

## ✅ 修复内容

### 修复 1: process_single_video() 方法

**旧代码**:
```python
# 显示结果信息
result_info = f"✓ 完成: 提取了 {saved_count} 个活动帧"
if self.output_video and output_video_path and os.path.exists(output_video_path):
    video_size = os.path.getsize(output_video_path) / (1024 * 1024)
    result_info += f"，生成视频 {video_size:.2f}MB"
result_info += f"\n  输出目录: {video_output_dir}"
print(result_info)
```

**新代码**:
```python
# 显示截图提取结果
result_info = f"✓ 截图提取完成: {saved_count} 张"
print(result_info)

# 2. 如果启用视频片段提取
if self.extract_clips:
    print(f"\n开始提取视频片段...")
    clips_output_dir = video_output_dir / "clips"
    clips = self.clip_extractor.process_video(...)
    ...
```

### 修复 2: process_all() 方法

**旧代码**:
```python
if self.output_video:
    print(f"视频输出: 启用（只包含检测到运动的帧）")
```

**新代码**:
```python
if self.extract_clips:
    print(f"视频片段提取: 启用（连续运动>{self.min_motion_duration}秒，前后{self.clip_before}/{self.clip_after}秒）")
```

### 修复 3: 清理重复代码

移除了由于之前替换操作导致的重复代码块。

## 🧪 验证

所有 Python 文件通过语法检查：
```bash
python3 -m py_compile main.py video_processor.py video_clip_extractor.py
✓ 所有 Python 文件语法检查通过
```

## 📝 Git 提交

```
commit 8d2b3f1
fix: Remove references to removed output_video attribute

Fixed AttributeError: 'BatchProcessor' object has no attribute 'output_video'
```

## ✅ 修复后的正确用法

### 1. 只提取截图（带绿色矩形框）
```bash
python3 main.py -i video.mp4
```

### 2. 提取截图 + 视频片段
```bash
python3 main.py -i video.mp4 --extract-clips
```

### 3. 自定义视频片段参数
```bash
python3 main.py -i video.mp4 --extract-clips \
  --motion-duration 5 \
  --clip-before 30 \
  --clip-after 30
```

### 4. 批量处理
```bash
python3 main.py -i /path/to/videos/ --extract-clips
```

## 📋 BatchProcessor 当前属性

```python
class BatchProcessor:
    def __init__(self, 
                 output_dir: str,
                 sensitivity: int = 25,
                 min_interval: float = 1.0,
                 fps: int = 2,
                 image_format: str = 'jpg',
                 preview: bool = False,
                 extract_clips: bool = False,      # ← 新参数
                 min_motion_duration: float = 3.0,  # ← 新参数
                 clip_before: float = 20.0,         # ← 新参数
                 clip_after: float = 20.0):         # ← 新参数
```

**已移除的参数**:
- ❌ `output_video` (已被 `extract_clips` 替代)

**新增的参数**:
- ✅ `extract_clips`: 是否提取视频片段
- ✅ `min_motion_duration`: 最小连续运动时长
- ✅ `clip_before`: 事件前提取时长
- ✅ `clip_after`: 事件后提取时长

## 🔗 相关文档

- [VIDEO_CLIP_FEATURE.md](./VIDEO_CLIP_FEATURE.md) - 视频片段提取功能完整说明
- [CHANGELOG.md](./CHANGELOG.md) - 版本更新日志

---

**修复时间**: 2025-10-21  
**状态**: ✅ 已修复并推送到 GitHub
