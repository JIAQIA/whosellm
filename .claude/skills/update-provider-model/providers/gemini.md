---
name: gemini
description: Google Gemini 模型信息采集指南
---

# Google Gemini 模型信息采集

## 官方文档入口

- **模型列表页**：`https://ai.google.dev/gemini-api/docs/models`
- **API 参考**：`https://ai.google.dev/api`
- **发布博客**：`https://blog.google/technology/google-deepmind/`
- **Google AI Studio**：`https://aistudio.google.com/`

## Playwright 操作指南

1. 导航到模型列表页后，使用 `browser_snapshot` 获取页面结构
2. Google 文档使用左侧导航 + 右侧内容面板，模型信息通常以表格形式展示
3. 每个模型有独立的详情卡片，包含输入/输出模态、context window、max output tokens 等
4. 注意区分 **GA 模型**（稳定版）、**Preview 模型**（预览版）和 **Experimental 模型**（实验版）

## 命名规则

- 基本格式：`gemini-{major}.{minor}-{variant}`（如 `gemini-2.5-flash`）
- 变体：`flash`（快速）、`flash-lite`（极速轻量）、`pro`（高级）
- 特殊后缀：
  - `-preview`：预览版
  - `-preview-{date}`：带日期的预览版（如 `gemini-2.5-flash-preview-09-2025`）
  - `-image`：图像生成变体（如 `gemini-2.5-flash-image`）
  - `-live`：实时音频变体
  - `-native-audio-preview-{date}`：原生音频预览
  - `-preview-tts`：文本转语音预览
  - `-exp`：实验版
  - `-001`：固定版本号后缀
- Gemini 3.x 系列使用 `gemini-3-{variant}` 格式（无小数点版本号）

## 配置文件

单文件：`whosellm/models/families/gemini.py`

所有 Gemini 模型属于同一个 `ModelFamily.GEMINI` 家族，Provider 为 `Provider.GOOGLE`，通过 `specific_models` 区分版本和变体。

## 变体优先级

- `flash-lite` / `flash-tts`：`(0,)`
- `flash`：`(1,)`
- `flash-image`：`(2,)`
- `pro-tts`：`(3,)`
- `pro-image`：`(4,)`
- `pro`：`(4,)` ~ `(5,)`

## 注意事项

- Image 系列模型（`-image` 后缀）虽然实际调试中可能产生思考内容，但接口不支持配置 thinking 行为，因此标记为 `supports_thinking=False`
- Image 系列模型的 `context_window` 和 `max_tokens` 通常远小于标准模型
- TTS 系列模型能力非常受限，仅支持 `supports_audio_generation` 和 `supports_streaming`
- `supports_file_search` 和 `supports_code_interpreter` 并非所有变体都支持，flash-lite 和 2.0 系列通常不支持 code_interpreter
- 大部分 Gemini 模型的 `context_window` 为 `1048576`（1M tokens），但特殊变体例外
- `supports_web_search` 在 2.0 flash 及以上版本可用，2.0 flash-lite 不支持
