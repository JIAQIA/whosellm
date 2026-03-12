---
name: vidu
description: Vidu 视频生成模型信息采集指南
---

# Vidu 视频生成模型信息采集

## 官方文档入口

- **API 文档**：`https://api.vidu.com/docs`
- **官网**：`https://www.vidu.com`

## Playwright 操作指南

1. Vidu 文档可能需要登录才能查看完整 API 参考
2. 关注视频生成相关的参数：分辨率、时长限制、支持的输入格式

## 命名规则

- `vidu-q1-{variant}`（如 `vidu-q1`、`vidu-q1-turbo`）
- `vidu-2-{variant}`（如 `vidu-2`、`vidu-2-turbo`）

## 配置文件

单文件：`whosellm/models/families/vidu.py`

## 注意事项

- Vidu 是视频生成模型，能力参数与语言模型不同
- 主要关注 `max_video_duration_seconds`、`max_video_size_mb`、`supported_video_mime_type` 等视频相关限制
- 不支持 `function_calling`、`streaming`、`structured_outputs` 等语言模型能力
