# 如何运行本项目

## 📋 步骤总览

1. ✅ 安装依赖
2. ✅ 准备视频文件
3. ✅ 运行程序
4. ✅ 查看结果

---

## 🚀 详细步骤

### 步骤 1️⃣ : 安装依赖

在终端中运行（二选一）：

**方式A：自动安装（推荐）**
```bash
cd /root/findAction
./install.sh
```

**方式B：手动安装**
```bash
pip3 install opencv-python numpy tqdm
```

---

### 步骤 2️⃣ : 准备视频文件

**选项1：使用您自己的特斯拉视频**
- 将视频文件复制到任意位置
- 记下视频的完整路径

**选项2：创建测试视频（如果没有真实视频）**
```bash
python3 create_test_video.py
```
这会在当前目录生成 `test_video.mp4`

---

### 步骤 3️⃣ : 运行程序

#### 🎬 基础命令

```bash
# 处理单个视频（最简单）
python3 main.py -i your_video.mp4

# 处理测试视频
python3 main.py -i test_video.mp4
```

#### 🎯 常用命令

```bash
# 处理视频并指定输出目录
python3 main.py -i video.mp4 -o ./my_output

# 处理整个文件夹的所有视频
python3 main.py -i /path/to/videos/ -o ./output

# 实时预览检测效果（按q退出）
python3 main.py -i video.mp4 --preview
```

#### ⚙️ 调整参数

```bash
# 哨兵模式（停车录像，更敏感）
python3 main.py -i sentry.mp4 -s 18 --min-interval 3.0

# 行车录像（过滤正常道路变化）
python3 main.py -i driving.mp4 -s 30 --min-interval 1.5
```

#### 📖 查看所有参数说明

```bash
python3 main.py --help
```

---

### 步骤 4️⃣ : 查看结果

截图会保存在输出目录（默认是 `extracted_frames/`）

```bash
# 查看提取的截图
ls -lh extracted_frames/

# 示例输出：
# video_00h02m15s.jpg  ← 视频在2分15秒的截图
# video_00h05m30s.jpg  ← 视频在5分30秒的截图
# video_00h08m45s.jpg  ← 视频在8分45秒的截图
```

文件名格式：`{视频名}_{时}h{分}m{秒}s.jpg`

---

## 💡 实际使用示例

### 示例1：处理特斯拉哨兵模式录像

```bash
# 假设您的哨兵录像在这个目录
python3 main.py \
  -i /media/TeslaCam/SentryClips \
  -o ./sentry_activity \
  -s 18 \
  --min-interval 3.0
```

### 示例2：处理保存的行车片段

```bash
python3 main.py \
  -i /media/TeslaCam/SavedClips \
  -o ./driving_events \
  -s 30 \
  --min-interval 1.5
```

### 示例3：调试和优化参数

```bash
# 使用预览模式查看实时检测效果
python3 main.py -i test.mp4 --preview -s 25

# 觉得截图太多？提高灵敏度值
python3 main.py -i test.mp4 --preview -s 35

# 觉得漏掉了一些？降低灵敏度值
python3 main.py -i test.mp4 --preview -s 15
```

---

## ⚠️ 常见问题

### Q: 提示"No module named 'cv2'"

**A:** 需要安装依赖包
```bash
pip3 install opencv-python numpy tqdm
```

### Q: 没有提取到任何截图

**A:** 可能是灵敏度设置太高，试试：
```bash
python3 main.py -i video.mp4 -s 15 --preview
```

### Q: 截图太多，很多都是重复的

**A:** 提高灵敏度和最小间隔：
```bash
python3 main.py -i video.mp4 -s 35 --min-interval 3.0
```

### Q: 程序运行很慢

**A:** 降低处理帧率：
```bash
python3 main.py -i video.mp4 --fps 1
```

### Q: 使用 python 还是 python3？

**A:** 在Linux系统上通常使用 `python3`，在某些系统上 `python` 也指向Python 3

---

## 📚 更多帮助

- **完整文档**: 查看 `README.md`
- **快速开始**: 查看 `QUICKSTART.md`
- **配置示例**: 查看 `config_example.py`
- **在线帮助**: `python3 main.py --help`

---

## 🎉 就这么简单！

现在您可以从海量特斯拉录像中快速提取关键时刻了！
