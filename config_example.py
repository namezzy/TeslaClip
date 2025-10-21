#!/usr/bin/env python3
"""
配置示例文件
可以复制此文件为 config.py 并根据需要修改参数
"""

# 运动检测配置
MOTION_DETECTION = {
    # 灵敏度 (0-100)，值越小越敏感
    'sensitivity': 25,
    
    # 最小运动区域面积（像素）
    'min_area': 500,
    
    # 最小截图间隔（秒）
    'min_interval': 1.0,
    
    # 处理帧率（每秒处理的帧数）
    'process_fps': 2,
}

# 输出配置
OUTPUT = {
    # 默认输出目录
    'default_dir': './extracted_frames',
    
    # 图像格式 ('jpg' 或 'png')
    'format': 'jpg',
    
    # JPEG质量 (0-100)
    'jpeg_quality': 95,
}

# 视频文件配置
VIDEO = {
    # 支持的视频格式
    'supported_formats': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v'],
    
    # 是否递归搜索子目录
    'recursive_search': True,
}

# 针对不同场景的预设配置
PRESETS = {
    'sentry': {  # 哨兵模式（停车录像）
        'sensitivity': 18,
        'min_interval': 3.0,
        'process_fps': 2,
        'description': '适用于停车场景，捕捉人或车靠近'
    },
    'driving': {  # 行车模式
        'sensitivity': 30,
        'min_interval': 1.5,
        'process_fps': 3,
        'description': '适用于行车录像，过滤正常道路场景'
    },
    'sensitive': {  # 高灵敏度
        'sensitivity': 15,
        'min_interval': 0.5,
        'process_fps': 4,
        'description': '捕捉所有细微变化，可能产生较多截图'
    },
    'conservative': {  # 保守模式
        'sensitivity': 35,
        'min_interval': 5.0,
        'process_fps': 1,
        'description': '只捕捉明显活动，减少截图数量'
    },
}
