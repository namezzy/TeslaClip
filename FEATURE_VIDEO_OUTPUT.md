# 视频输出功能文档

## 功能概述

视频输出功能允许用户生成包含运动检测可视化的输出视频文件。该功能会在检测到运动的帧上绘制：
- **运动轮廓**（绿色）：检测到的运动区域边界
- **边界框**（红色）：包围运动区域的矩形框
- **面积标签**：显示每个运动区域的像素面积
- **时间戳**：当前帧在原视频中的时间位置
- **轮廓计数**：当前帧检测到的运动区域数量

## 使用方法

### 基本用法

```bash
python main.py -i video.mp4 --output-video
```

### 完整参数示例

```bash
python main.py -i video.mp4 \
  --output-video \
  -o ./output \
  -s 25 \
  --min-interval 1.0 \
  --fps 2
```

## 参数说明

### 核心参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--output-video` | 启用视频输出功能 | 关闭 |
| `-i, --input` | 输入视频文件路径 | 必需 |
| `-o, --output` | 输出目录 | `./extracted_frames` |

### 运动检测参数

| 参数 | 说明 | 默认值 | 推荐范围 |
|------|------|--------|----------|
| `-s, --sensitivity` | 运动检测灵敏度（0-100，值越小越敏感） | 25 | 哨兵模式: 15-20<br>行驶录像: 25-35 |
| `--min-interval` | 最小帧捕获间隔（秒） | 1.0 | 哨兵模式: 3-5<br>行驶录像: 1-2 |
| `--fps` | 处理帧率（每秒处理的帧数） | 2 | 1-5 |

## 输出文件

### 输出视频命名规则

输出视频文件名格式为：`{原视频名称}_motion_detected.mp4`

例如：
- 输入：`front_camera.mp4`
- 输出：`front_camera_motion_detected.mp4`

### 输出位置

输出视频保存在指定的输出目录中（`-o` 参数指定）。

## 可视化元素说明

### 1. 运动轮廓（绿色）
- **颜色**：BGR (0, 255, 0) 绿色
- **粗细**：2 像素
- **含义**：精确描绘检测到的运动区域边界

### 2. 边界框（红色）
- **颜色**：BGR (0, 0, 255) 红色
- **粗细**：2 像素
- **含义**：运动区域的最小外接矩形

### 3. 面积标签（黄色）
- **颜色**：BGR (0, 255, 255) 黄色
- **字体**：FONT_HERSHEY_SIMPLEX
- **比例**：0.5
- **格式**：`Area: {像素数量}px`
- **位置**：边界框左上角上方

### 4. 时间戳（白色）
- **颜色**：BGR (255, 255, 255) 白色
- **字体**：FONT_HERSHEY_SIMPLEX
- **比例**：0.7，粗细 2
- **格式**：`HH:MM:SS`
- **位置**：画面左上角

### 5. 轮廓计数（白色）
- **颜色**：BGR (255, 255, 255) 白色
- **字体**：FONT_HERSHEY_SIMPLEX
- **比例**：0.7，粗细 2
- **格式**：`Contours: {数量}`
- **位置**：时间戳下方

## 技术实现

### 视频编码参数

- **编解码器**：H.264 (MPEG-4 AVC)
- **FourCC**：`mp4v`
- **帧率**：与原视频相同
- **分辨率**：与原视频相同
- **色彩空间**：BGR

### 处理流程

1. **初始化视频写入器**
   ```python
   fourcc = cv2.VideoWriter_fourcc(*'mp4v')
   video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
   ```

2. **运动检测与轮廓提取**
   ```python
   has_motion, motion_mask, contours = detector.detect_motion(frame)
   ```

3. **绘制可视化元素**
   - 绘制运动轮廓（cv2.drawContours）
   - 绘制边界框（cv2.rectangle）
   - 添加面积标签（cv2.putText）
   - 添加时间戳和计数

4. **写入视频帧**
   ```python
   video_writer.write(frame_with_contours)
   ```

5. **释放资源**
   ```python
   video_writer.release()
   ```

## 使用场景

### 1. 哨兵模式分析
```bash
python main.py -i sentry_event.mp4 \
  --output-video \
  -s 15 \
  --min-interval 3.0
```
- 低灵敏度捕获明显运动
- 较长间隔避免重复捕获
- 适合分析停车场事件

### 2. 行驶录像分析
```bash
python main.py -i driving_front.mp4 \
  --output-video \
  -s 30 \
  --min-interval 1.0 \
  --fps 3
```
- 中等灵敏度过滤正常道路变化
- 较短间隔捕获快速事件
- 适合识别危险驾驶行为

### 3. 精细调试
```bash
python main.py -i test_video.mp4 \
  --output-video \
  --preview \
  -s 20 \
  --fps 5
```
- 启用实时预览窗口
- 高处理帧率获得更多细节
- 适合参数调优

## 性能考虑

### CPU 使用
- 视频编码是 CPU 密集型操作
- 降低 `--fps` 可减少处理负载
- 建议在多核 CPU 上运行

### 存储空间
- 输出视频大小取决于：
  - 原视频分辨率
  - 运动帧数量
  - 压缩率
- 估算：1小时 1080p 视频约 500MB - 2GB

### 处理速度
- 典型处理速度：2-5 FPS（实时的 0.1-0.2 倍）
- 影响因素：
  - 输入分辨率
  - `--fps` 参数
  - CPU 性能

## 故障排除

### 问题：输出视频无法播放
**原因**：编解码器不兼容
**解决方案**：
```bash
# 使用 ffmpeg 重新编码
ffmpeg -i output_video.mp4 -c:v libx264 output_video_h264.mp4
```

### 问题：轮廓过多导致画面混乱
**原因**：灵敏度过高
**解决方案**：
```bash
# 增加 sensitivity 值（降低敏感度）
python main.py -i video.mp4 --output-video -s 35
```

### 问题：处理速度过慢
**原因**：处理帧率过高
**解决方案**：
```bash
# 降低 fps 参数
python main.py -i video.mp4 --output-video --fps 1
```

### 问题：遗漏重要运动
**原因**：灵敏度过低或间隔过长
**解决方案**：
```bash
# 降低 sensitivity 值（提高敏感度），减少间隔
python main.py -i video.mp4 --output-video -s 15 --min-interval 0.5
```

## API 参考

### VideoProcessor.process_video()

```python
def process_video(
    self,
    video_path: str,
    callback: Optional[Callable] = None,
    output_video_path: Optional[str] = None
) -> List[FrameExtraction]:
    """
    处理视频并提取活动帧
    
    Args:
        video_path: 输入视频文件路径
        callback: 进度回调函数
        output_video_path: 输出视频路径（可选）
                          如果提供，将生成带有运动轮廓的视频
    
    Returns:
        提取的帧信息列表
    """
```

### MotionDetector.detect_motion()

```python
def detect_motion(self, frame: np.ndarray) -> Tuple[bool, np.ndarray, List]:
    """
    检测帧中的运动
    
    Args:
        frame: 输入帧（BGR 格式）
    
    Returns:
        Tuple[bool, np.ndarray, List]:
            - has_motion: 是否检测到运动
            - motion_mask: 运动掩码图像
            - contours: 检测到的轮廓列表
    """
```

## 版本历史

- **v1.1.0**（即将发布）：首次引入视频输出功能
  - 运动轮廓绘制
  - 边界框可视化
  - 面积和时间戳标注
  - 可配置的运动检测参数

## 相关文档

- [README.md](README.md) - 项目概述
- [README_CN.md](README_CN.md) - 中文文档
- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志

## 贡献与反馈

如有问题或建议，请在 GitHub Issues 中提交：
https://github.com/namezzy/TeslaClip/issues
