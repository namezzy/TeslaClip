# TeslaClip 🚗⚡

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

**特斯拉行车记录仪和哨兵模式视频智能活动帧提取器**

[English](./README.md) | [中文文档](#中文文档)

</div>

---

## 📖 中文文档

### 🎯 TeslaClip 是什么？

TeslaClip 是一个强大的计算机视觉工具，可以自动从特斯拉行车记录仪和哨兵模式录像中提取关键时刻。使用先进的运动检测算法，帮助您快速发现车辆周围发生的事件，无需观看数小时的录像。

### ✨ 核心功能

- 🎥 **智能运动检测** - 先进的帧差算法自动检测活动
- 📸 **自动截图提取** - 检测到运动时自动保存关键帧
- 🎬 **轮廓可视化视频输出** - 生成带有运动检测可视化的视频（新功能！）
- ⏰ **时间戳命名** - 文件名包含视频时间戳（如 `00h05m30s.jpg`）方便定位
- 📦 **批量处理** - 一次处理多个视频或整个文件夹
- ⚙️ **可配置参数** - 针对不同场景微调灵敏度、间隔和帧率
- 📊 **进度跟踪** - 实时进度条和统计信息
- 👁️ **预览模式** - 可视化调试以优化检测设置

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/namezzy/TeslaClip.git
cd TeslaClip

# 快速安装（推荐）
./install.sh

# 或手动安装
pip3 install opencv-python numpy tqdm
```

#### 基本使用

```bash
# 处理单个视频
python3 main.py -i your_video.mp4

# 处理整个文件夹
python3 main.py -i /path/to/tesla/videos -o ./output

# 生成带有运动轮廓的视频（新功能！）
python3 main.py -i video.mp4 --output-video

# 预览模式调试参数
python3 main.py -i video.mp4 --preview
```

#### 创建测试视频

```bash
# 生成包含运动的测试视频
python3 create_test_video.py

# 运行演示
./run_demo.sh
```

### 📋 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-i, --input` | 输入视频文件或目录 | 必需 |
| `-o, --output` | 截图输出目录 | `./extracted_frames` |
| `-s, --sensitivity` | 运动检测灵敏度（0-100，值越小越敏感） | `25` |
| `--min-interval` | 截图最小间隔（秒） | `1.0` |
| `--fps` | 处理帧率 | `2` |
| `--format` | 输出格式（jpg/png） | `jpg` |
| `--preview` | 启用实时预览窗口 | `false` |
| `--output-video` | 生成带有运动检测可视化的视频 | `false` |

### 🎨 使用示例

#### 哨兵模式（停车录像）
```bash
python3 main.py -i sentry_video.mp4 -s 18 --min-interval 3.0
```
*更敏感的设置适合静态摄像头，捕捉接近的人/车*

#### 行车模式
```bash
python3 main.py -i driving_video.mp4 -s 30 --min-interval 1.5
```
*过滤正常道路变化，只捕捉重要事件*

#### 高灵敏度
```bash
python3 main.py -i video.mp4 -s 15 --min-interval 0.5 --fps 4
```
*捕捉所有细微变化（会生成更多截图）*

### 📂 输出结构

```
extracted_frames/
├── video1/                          # 每个视频都有独立的文件夹
│   ├── video1_00h05m30s.jpg       # 带轮廓标注的截图，5分30秒
│   ├── video1_00h07m15s.jpg       # 带轮廓标注的截图，7分15秒
│   └── video1_motion_detected.mp4 # 只包含运动帧的视频
├── video2/
│   ├── video2_00h00m45s.jpg
│   └── video2_motion_detected.mp4
└── ...
```

**核心特性：**
- 📁 **独立文件夹** - 每个视频都有自己的子文件夹
- 🎨 **标注截图** - 所有截图都包含运动轮廓、边界框和标签
- 🎬 **纯运动视频** - 输出视频只包含检测到运动的帧（大小减少 70-90%）

文件名格式：`{视频名}_{时}h{分}m{秒}s.{格式}`

### 🎬 视频输出功能（新功能！）

生成带有运动检测实时标注的视频：

```bash
python3 main.py -i video.mp4 --output-video -s 25
```

**核心特性：**
- ⚡ **仅运动帧** - 输出视频只包含检测到运动的帧
- 📉 **文件更小** - 通常比原视频小 70-90%
- ⏱️ **省时高效** - 只看关键时刻，跳过所有静止内容

**可视化内容包括：**
- 🟢 **绿色轮廓** - 检测到的运动边界
- 🔴 **红色边界框** - 最小外接矩形
- 🔢 **面积标签** - 每个运动区域的像素大小
- ⏱️ **时间戳** - 当前视频时间（时:分:秒）
- 📊 **轮廓计数** - 检测到的运动区域数量

**输出文件：** `{视频名}_motion_detected.mp4`（保存在专属文件夹中）

**使用场景：**
- 快速回顾停车场事件（1小时 → 5分钟）
- 从行车录像创建精彩集锦
- 为保险理赔生成带标注的证据视频
- 可视化调试和优化灵敏度参数

详细文档请参阅 [FEATURE_CORRECTION.md](./FEATURE_CORRECTION.md)

### 🔧 工作原理

1. **帧差法** - 比较连续帧检测变化
2. **背景建模** - 适应渐变的光照变化
3. **噪声过滤** - 去除小范围运动伪影
4. **智能间隔** - 防止同一事件重复捕获

```
视频输入 → 运动检测 → 关键帧提取 → 时间戳命名 → 截图输出
```

### 🎯 使用场景

- 🚗 找到有人/车靠近停放特斯拉的时刻
- 📹 从行车录像中提取关键事件
- 🔍 回顾特定时间段发生了什么
- 📊 创建视频摘要或精彩集锦

### ⚙️ 配置预设

`config_example.py` 包含优化的预设：

| 预设 | 灵敏度 | 间隔 | FPS | 适用场景 |
|------|--------|------|-----|----------|
| `sentry` | 18 | 3.0秒 | 2 | 停车/哨兵模式 |
| `driving` | 30 | 1.5秒 | 3 | 行车录像 |
| `sensitive` | 15 | 0.5秒 | 4 | 捕捉所有变化 |
| `conservative` | 35 | 5.0秒 | 1 | 只捕捉重大事件 |

### 🛠️ 技术栈

- **Python 3.8+** - 核心语言
- **OpenCV** - 视频处理和运动检测
- **NumPy** - 数值计算
- **tqdm** - 进度条

### 📚 文档

- [快速入门指南](./QUICKSTART.md) - 详细设置说明（英文）
- [如何运行](./如何运行.md) - 中文教程
- [配置示例](./config_example.py) - 预设配置

### 🐛 故障排除

#### 没有提取到截图
- 降低灵敏度：`-s 15`
- 检查视频是否确实有运动画面

#### 截图太多且重复
- 提高灵敏度：`-s 35`
- 增加间隔：`--min-interval 3.0`

#### 程序运行缓慢
- 降低帧率：`--fps 1`
- 只处理需要的文件

### 🤝 贡献

欢迎贡献！您可以：
- 🐛 报告 bug
- 💡 提出新功能建议
- 🔧 提交 pull request

### 📝 开发路线图

- [ ] 深度学习对象检测（YOLO/MobileNet）
- [ ] 特斯拉 4 摄像头系统多摄像头同步
- [ ] 带时间轴可视化的 HTML 报告生成
- [ ] GPU 加速支持
- [ ] 智能分类（人、车辆、动物）
- [ ] 移动应用支持

### 🙏 致谢

灵感来自于高效回顾特斯拉大量行车记录的需求。

### 📄 许可证

MIT 许可证 - 随意使用和修改！

### 🔗 链接

- **GitHub**: https://github.com/namezzy/TeslaClip
- **问题反馈**: https://github.com/namezzy/TeslaClip/issues

---

<div align="center">

**为特斯拉车主用 ❤️ 制作**

如果觉得有用，请给个 ⭐ Star！

</div>
