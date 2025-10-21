# TeslaClip 项目文档

本文件夹包含 TeslaClip 项目的所有技术文档、功能说明、Bug 修复记录和发布说明。

## 📚 文档索引

### 🚀 快速开始
- [QUICKSTART.md](QUICKSTART.md) - 快速入门指南

### 📖 功能文档
- [VIDEO_CLIP_FEATURE.md](VIDEO_CLIP_FEATURE.md) - 视频片段提取功能详细说明
- [CONTINUOUS_MOTION_TRACKING.md](CONTINUOUS_MOTION_TRACKING.md) - 全程运动追踪功能（最新）
- [FEATURE_VIDEO_OUTPUT.md](FEATURE_VIDEO_OUTPUT.md) - 视频输出功能文档
- [FEATURE_CORRECTION.md](FEATURE_CORRECTION.md) - 功能修正说明
- [FEATURE_IMPLEMENTATION_SUMMARY.md](FEATURE_IMPLEMENTATION_SUMMARY.md) - 功能实现总结

### 🐛 Bug 修复记录
- [BUGFIX_MOTION_ANNOTATION.md](BUGFIX_MOTION_ANNOTATION.md) - 运动标注准确性修复（最新）
- [BUGFIX_ATTRIBUTE_ERROR.md](BUGFIX_ATTRIBUTE_ERROR.md) - AttributeError 修复
- [BUGFIX_PROGRESS_ENHANCEMENT.md](BUGFIX_PROGRESS_ENHANCEMENT.md) - 进度条增强修复
- [BUGFIX_PROGRESS_BAR.md](BUGFIX_PROGRESS_BAR.md) - 进度条修复
- [BUGFIX_COMPLETE_SUMMARY.md](BUGFIX_COMPLETE_SUMMARY.md) - 完整修复总结
- [BUGFIX_SUMMARY.md](BUGFIX_SUMMARY.md) - Bug 修复摘要

### 📝 变更日志
- [CHANGELOG.md](CHANGELOG.md) - 完整的版本变更记录

### 🎯 总结文档
- [CORRECTION_SUMMARY.md](CORRECTION_SUMMARY.md) - 修正总结
- [RELEASE_SUMMARY.md](RELEASE_SUMMARY.md) - 发布总结

### 🚢 发布相关
- [HOW_TO_RELEASE.md](HOW_TO_RELEASE.md) - 发布流程指南
- [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md) - v1.0.0 版本发布说明
- [DEPLOYMENT.md](DEPLOYMENT.md) - 部署文档

## 📂 文档组织规则

1. **Bug 修复文档**：以 `BUGFIX_` 开头，描述问题、原因和解决方案
2. **功能文档**：以 `FEATURE_` 开头，详细说明功能实现和使用方法
3. **发布文档**：以 `RELEASE_` 开头，包含版本发布信息
4. **其他文档**：按照文档类型命名（CHANGELOG、QUICKSTART 等）

## 🔄 文档更新原则

- 所有新的技术文档、功能说明、Bug 修复记录都应放在此文件夹
- 保持文档命名规范和一致性
- 每次重大更新都应更新 CHANGELOG.md
- Bug 修复应创建独立的 BUGFIX_*.md 文档，详细记录问题和解决方案

## 📌 主文档位置

项目根目录保留以下核心文档：
- `README.md` / `README_CN.md` - 项目主说明文档
- `How_to_run.md` - 快速运行指南

所有其他技术文档均在本 `docs/` 文件夹中维护。
