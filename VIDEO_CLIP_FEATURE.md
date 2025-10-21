# 视频片段提取功能说明

## 🎯 功能概述

根据用户需求重新设计的视频处理功能，现在分为两个独立的部分：

### 1. 截图提取（默认功能）
- 检测运动并提取关键帧
- **只绘制绿色矩形边界框**（不再有不规则轮廓和红色框）
- 添加时间戳

### 2. 视频片段提取（可选功能）
- 检测**连续运动超过 3 秒**的事件
- 提取事件前后各 20 秒的视频片段
- 在运动期间绘制绿色矩形边界框

## 🚀 使用方法

### 基本使用 - 只提取截图

```bash
python3 main.py -i video.mp4
```

**输出**:
```
extracted_frames/
└── video/
    ├── video_00h00m15s.jpg  ✅ 只有绿色矩形框
    ├── video_00h00m32s.jpg  ✅ 只有绿色矩形框
    └── ...
```

### 提取视频片段

```bash
python3 main.py -i video.mp4 --extract-clips
```

**输出**:
```
extracted_frames/
└── video/
    ├── video_00h00m15s.jpg
    ├── video_00h00m32s.jpg
    └── clips/                           ← 视频片段文件夹
        ├── video_clip_001_000327.mp4   ← 事件1 (从3分27秒开始)
        ├── video_clip_002_001045.mp4   ← 事件2 (从10分45秒开始)
        └── ...
```

### 自定义视频片段参数

```bash
python3 main.py -i video.mp4 --extract-clips \
  --motion-duration 5 \    # 最小连续运动5秒
  --clip-before 30 \       # 事件前30秒
  --clip-after 30          # 事件后30秒
```

## 📋 命令行参数

### 基本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-i, --input` | 输入视频文件或文件夹 | 必需 |
| `-o, --output` | 输出目录 | `./extracted_frames` |
| `-s, --sensitivity` | 运动检测灵敏度 (0-100) | 25 |
| `--min-interval` | 最小截图间隔（秒） | 1.0 |
| `--fps` | 处理帧率 | 2 |
| `--format` | 截图格式 (jpg/png) | jpg |
| `--preview` | 启用预览窗口 | false |

### 视频片段提取参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--extract-clips` | 启用视频片段提取 | false |
| `--motion-duration` | 最小连续运动时长（秒） | 3.0 |
| `--clip-before` | 事件前提取时长（秒） | 20.0 |
| `--clip-after` | 事件后提取时长（秒） | 20.0 |

## 🔧 工作原理

### 截图提取流程

```
1. 逐帧分析视频（按 fps 参数采样）
2. 检测运动（帧差法 + 背景建模）
3. 如果检测到运动：
   a. 获取运动轮廓
   b. 计算每个轮廓的边界框
   c. 绘制绿色矩形边界框
   d. 添加时间戳
   e. 如果距离上次截图 >= min_interval，保存图片
```

**截图标注**:
- ✅ 绿色矩形边界框 (BGR: 0, 255, 0)
- ✅ 白色时间戳 (左上角)
- ❌ 不再有不规则轮廓
- ❌ 不再有红色框
- ❌ 不再有面积标签

### 视频片段提取流程

```
第一阶段：运动事件检测
1. 逐帧分析整个视频
2. 记录每个运动帧的时间
3. 识别连续运动序列
4. 筛选持续时间 >= min_motion_duration 的事件

第二阶段：视频片段提取
对每个事件：
1. 计算提取范围：
   - 开始时间 = 事件开始 - clip_before
   - 结束时间 = 事件结束 + clip_after
2. 重置运动检测器并预热（处理几帧以稳定状态）
3. 读取该范围内的所有帧
4. **仅在运动事件期间**（event.start_time 到 event.end_time）：
   - 进行运动检测
   - 绘制绿色矩形框标注运动物体
5. 事件外的帧也让检测器处理（保持状态连续）
6. 写入所有帧到输出视频文件
```

**关键特性**:
- ⚡ 只提取包含运动的片段（不是整个视频）
- 🎯 事件前后留有缓冲时间，便于理解上下文
- 🟢 **运动期间**持续标注运动物体，精准追踪
- 🔧 检测器预热机制，确保标注准确性
- 📝 文件名包含事件时间，便于定位

## 📊 示例场景

### 场景 1: 停车场监控（哨兵模式）

**输入**: 1小时停车场录像，有3次车辆经过

**处理**:
```bash
python3 main.py -i parking.mp4 --extract-clips \
  -s 18 \
  --motion-duration 3 \
  --clip-before 15 \
  --clip-after 15
```

**输出**:
```
extracted_frames/parking/
├── parking_00h12m30s.jpg
├── parking_00h35m15s.jpg
├── parking_00h48m22s.jpg
└── clips/
    ├── parking_clip_001_001215.mp4  (12:00-12:45, 45秒)
    ├── parking_clip_002_003500.mp4  (34:45-35:30, 45秒)
    └── parking_clip_003_004807.mp4  (47:52-48:37, 45秒)
```

**效果**:
- 原视频: 1小时 = 2.5 GB
- 3个片段: 共2分15秒 = 约30 MB
- **数据减少 99%，只看关键内容**

### 场景 2: 行驶录像分析

**输入**: 30分钟行驶录像，有多次急刹车/变道

**处理**:
```bash
python3 main.py -i driving.mp4 --extract-clips \
  -s 25 \
  --motion-duration 5 \
  --clip-before 20 \
  --clip-after 20
```

**输出**:
```
extracted_frames/driving/
├── driving_00h05m12s.jpg
├── driving_00h15m43s.jpg
├── driving_00h22m08s.jpg
└── clips/
    ├── driving_clip_001_000452.mp4  (4:32-5:32, 1分钟)
    ├── driving_clip_002_001523.mp4  (15:03-16:03, 1分钟)
    └── driving_clip_003_002148.mp4  (21:28-22:28, 1分钟)
```

## 🎨 输出示例

### 截图示例

```
┌─────────────────────────────┐
│ 00:12:30        (时间戳)    │
│                             │
│    ┌────────┐  (绿色矩形)  │
│    │        │               │
│    │ 运动区域│               │
│    │        │               │
│    └────────┘               │
│                             │
└─────────────────────────────┘
```

### 视频片段内容

```
时间轴：
|─────────|===========|─────────|
  前20秒    运动3秒     后20秒
  (有绿框)  (有绿框)   (有绿框)

- 00:00-43:00: 整个视频都实时检测运动并绘制绿色矩形框
- 检测到运动的区域会被标注
- 没有运动的帧则不显示框（干净画面）
```

## 🔍 与之前版本的区别

### 截图变化

| 特性 | 旧版本 | 新版本 |
|------|--------|--------|
| 轮廓绘制 | ✅ 绿色不规则轮廓 | ❌ 不绘制 |
| 边界框 | ✅ 红色矩形 | ✅ 绿色矩形 |
| 面积标签 | ✅ 黄色文字 | ❌ 不显示 |
| 轮廓计数 | ✅ 白色文字 | ❌ 不显示 |
| 时间戳 | ✅ 白色文字 | ✅ 白色文字 |

**结果**: 更简洁、更清晰

### 视频输出变化

| 特性 | 旧版本 | 新版本 |
|------|--------|--------|
| 输出内容 | 所有运动帧 | 连续运动事件片段 |
| 文件数量 | 1个大文件 | 多个小片段 |
| 上下文 | 无 | 前后各20秒 |
| 实用性 | 需要手动查找事件 | 每个片段是完整事件 |

**结果**: 更实用、更易分析

## 💡 使用建议

### 1. 参数调优

**第一步**: 不启用视频片段提取，只测试截图
```bash
python3 main.py -i test.mp4 -s 25
```
查看截图质量，调整 sensitivity

**第二步**: 启用视频片段提取，测试一个短视频
```bash
python3 main.py -i test.mp4 --extract-clips --motion-duration 3
```
查看是否正确识别运动事件

**第三步**: 批量处理
```bash
python3 main.py -i /path/to/videos/ -o ./output --extract-clips
```

### 2. 不同场景的推荐参数

**停车场/哨兵模式**:
```bash
--sensitivity 18 \
--motion-duration 3 \
--clip-before 15 \
--clip-after 15
```

**行驶录像**:
```bash
--sensitivity 30 \
--motion-duration 5 \
--clip-before 20 \
--clip-after 20
```

**高敏感度（捕获所有变化）**:
```bash
--sensitivity 15 \
--motion-duration 2 \
--clip-before 10 \
--clip-after 10
```

### 3. 性能优化

- `--fps 1`: 更快但可能漏检（每秒1帧）
- `--fps 2`: 平衡（推荐）
- `--fps 3-5`: 更精确但更慢

## 📁 输出文件组织

```
extracted_frames/
├── video1/
│   ├── video1_00h05m12s.jpg       ← 截图（绿色矩形框）
│   ├── video1_00h15m43s.jpg
│   └── clips/                      ← 视频片段文件夹
│       ├── video1_clip_001_000452.mp4
│       ├── video1_clip_002_001523.mp4
│       └── video1_clip_003_002148.mp4
├── video2/
│   ├── video2_00h02m30s.jpg
│   └── clips/
│       └── video2_clip_001_000210.mp4
└── ...
```

**文件命名规则**:
- 截图: `{视频名}_{HH}h{MM}m{SS}s.jpg`
- 片段: `{视频名}_clip_{序号}_{HHMMSS}.mp4`

## ❓ 常见问题

### Q1: 为什么截图上只有绿色矩形框？
A: 根据用户需求简化标注，只保留最重要的边界框。这样画面更清晰，不会被太多标注遮挡内容。

### Q2: 如果视频中没有连续3秒的运动会怎样？
A: 不会生成任何视频片段（clips 文件夹为空），但截图仍会正常提取。

### Q3: 视频片段文件很大怎么办？
A: 可以缩短提取时长:
```bash
--clip-before 10 --clip-after 10  # 只提取前后各10秒
```

### Q4: 可以同时处理多个视频吗？
A: 可以，指定文件夹路径:
```bash
python3 main.py -i /path/to/videos/ --extract-clips
```

### Q5: 如何调整运动检测的敏感度？
A: 
- 检测到太多运动: 增加 `--sensitivity` (如 35)
- 检测到太少运动: 降低 `--sensitivity` (如 15)

## 🔗 相关模块

- `video_processor.py` - 截图提取和运动检测
- `video_clip_extractor.py` - 视频片段提取（独立模块）
- `main.py` - 命令行接口和批处理

## 📝 技术细节

### MotionEvent 数据结构
```python
@dataclass
class MotionEvent:
    start_time: float      # 运动开始时间（秒）
    end_time: float        # 运动结束时间（秒）
    duration: float        # 持续时间（秒）
    start_frame: int       # 开始帧号
    end_frame: int         # 结束帧号
```

### VideoClipExtractor 核心方法
```python
# 检测所有运动事件
events = extractor.detect_motion_events(video_path, fps=2)

# 提取单个事件的视频片段
extractor.extract_clip(video_path, event, output_path)

# 处理整个视频
clips = extractor.process_video(video_path, output_dir, fps=2)
```

---

**更新时间**: 2025-10-21
**版本**: v1.2.0
