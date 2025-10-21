# 快速入门指南

## 第一步：安装依赖

```bash
# 确保您在项目目录中
cd /root/findAction

# 安装Python依赖包
pip install opencv-python numpy tqdm
```

或者使用 requirements.txt：

```bash
pip install -r requirements.txt
```

## 第二步：准备测试视频

将您的特斯拉录像文件放到项目目录或任意位置，例如：
- `/path/to/tesla/TeslaCam/SavedClips/video.mp4`
- 或当前目录下的测试视频

## 第三步：运行程序

### 方式1：处理单个视频（最简单）

```bash
python main.py -i /path/to/your/video.mp4
```

这会在当前目录创建 `extracted_frames` 文件夹，保存提取的截图。

### 方式2：指定输出目录

```bash
python main.py -i /path/to/video.mp4 -o ./my_output
```

### 方式3：批量处理整个文件夹

```bash
python main.py -i /path/to/tesla/videos_folder -o ./output
```

程序会自动查找文件夹中所有视频文件（.mp4, .avi, .mov等）。

### 方式4：调整参数获得更好效果

```bash
# 哨兵模式（停车录像）- 更敏感
python main.py -i sentry_video.mp4 -s 18 --min-interval 3.0

# 行车录像 - 过滤正常道路变化
python main.py -i driving_video.mp4 -s 30 --min-interval 1.5

# 预览模式 - 实时查看检测效果（按q退出）
python main.py -i video.mp4 --preview
```

## 完整命令参数说明

```bash
python main.py \
  -i INPUT                # 输入视频文件或文件夹（必需）
  -o OUTPUT               # 输出目录（默认：./extracted_frames）
  -s SENSITIVITY          # 灵敏度 0-100（默认：25，越小越敏感）
  --min-interval SECONDS  # 最小截图间隔（默认：1.0秒）
  --fps FPS               # 处理帧率（默认：2帧/秒）
  --format jpg|png        # 输出格式（默认：jpg）
  --preview               # 显示实时预览窗口
```

## 查看帮助

```bash
python main.py --help
```

## 输出结果

提取的截图会保存为：
```
extracted_frames/
├── video1_00h05m30s.jpg  # 视频1在5分30秒的截图
├── video1_00h07m15s.jpg  # 视频1在7分15秒的截图
├── video2_00h00m45s.jpg  # 视频2在45秒的截图
└── ...
```

文件名中的时间戳对应视频的播放位置，方便您在原视频中找到该时刻。

## 常见使用场景

### 场景1：从哨兵模式录像中找到有人接近的时刻
```bash
python main.py -i /TeslaCam/SentryClips -o ./sentry_output -s 18 --min-interval 3.0
```

### 场景2：从行车记录中提取关键事件
```bash
python main.py -i /TeslaCam/SavedClips -o ./driving_output -s 30 --min-interval 1.5
```

### 场景3：调试参数找到最佳设置
```bash
python main.py -i test_video.mp4 --preview -s 25
# 实时查看效果，按需调整 -s 参数
```

## 故障排除

### 问题1：没有提取到任何截图
- 尝试降低灵敏度：`-s 15`
- 检查视频是否确实有运动画面

### 问题2：截图太多，很多重复的
- 提高灵敏度：`-s 35`
- 增加最小间隔：`--min-interval 3.0`

### 问题3：程序运行很慢
- 降低处理帧率：`--fps 1`
- 只处理需要的视频文件

### 问题4：缺少依赖包
```bash
pip install opencv-python numpy tqdm
```
