---
name: zhipu
description: 智谱 AI 模型信息采集指南
---

# 智谱 AI (Zhipu) 模型信息采集

## 官方文档入口

- **开放平台文档**：`https://open.bigmodel.cn/dev/howuse/introduction`
- **模型列表**：`https://open.bigmodel.cn/dev/howuse/model`
- **API 文档**：`https://open.bigmodel.cn/dev/api/normal-model/glm-4`

## Playwright 操作指南

1. 智谱文档为中文 SPA 应用，**必须使用 Playwright**，WebSearch 效果很差
2. 导航到模型列表页后需要等待动态内容加载，建议 `browser_wait_for` 后再 `browser_snapshot`
3. 各模型详情页需要逐个点击左侧导航进入
4. 能力参数通常在 API 文档的"请求参数"部分，需要查看参数表格

## 命名规则

- **GLM 文本系列**：`glm-{major}` 或 `glm-{major}-{variant}`（如 `glm-4-plus`、`glm-4-long`）
- **GLM 视觉系列**：`glm-4v` 或 `glm-4v-{variant}`（如 `glm-4v-plus`、`glm-4v-flash`）
- **CogView 图像生成**：`cogview-{variant}`（如 `cogview-4`、`cogview-4-250304`）
- **CogVideoX 视频生成**：`cogvideox-{variant}`（如 `cogvideox-2`、`cogvideox-flash`）

## 配置文件

单文件：`whosellm/models/families/zhipu.py`

包含多个家族配置：`GLM_TEXT`、`GLM_VISION`、`GLM_3`、`COGVIEW_4`、`COGVIDEOX_3`、`COGVIDEOX_2`

## 注意事项

- 智谱的模型版本迭代较快，`glm-4` 系列有大量变体（air、airx、plus、long、flash、flashx 等）
- 视觉模型（glm-4v 系列）和文本模型（glm-4 系列）属于**不同的 ModelFamily**
- CogView 和 CogVideoX 是生成式模型，能力参数与语言模型完全不同（关注 `supports_image_generation` / `max_video_duration_seconds` 等）
- `ModelFamily.GLM_4` 和 `ModelFamily.GLM_4V` 是向后兼容别名，实际映射到 `GLM_TEXT` 和 `GLM_VISION`
- 部分模型有 MMDD 格式的日期后缀（如 `cogview-4-250304`），使用 `{mmdd:4d}` 或 `{snapshot:6d}` 模式
