---
name: alibaba
description: 阿里巴巴通义千问模型信息采集指南
---

# 阿里巴巴 (Alibaba) 通义千问模型信息采集

## 官方文档入口

- **模型广场**：`https://help.aliyun.com/zh/model-studio/getting-started/models`
- **API 文档**：`https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api`
- **DashScope 文档**：`https://dashscope.aliyun.com`

## 采集策略

- **首选工具**：Playwright（中文 SPA，需要展开折叠面板和切换 Tab）
- **回退工具**：WebSearch（搜索阿里云帮助文档中的特定模型参数）
- **可并行**：否 — 使用 Playwright 时必须独占浏览器，不可与其他 Playwright Agent 并发

## Playwright 操作指南

1. 阿里云文档为中文 SPA，建议使用 Playwright 操作
2. 模型列表通常在"模型广场"页面，包含模型卡片和能力标签
3. 部分内容需要展开折叠面板或切换 Tab 才能看到完整参数
4. API 调用示例中通常包含准确的模型 ID

## 命名规则

- **Qwen 系列**：`qwen-{variant}`（如 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-long`）
- **带日期版本**：`qwen-{variant}-{year}-{month}-{day}`
- **版本号模型**：`qwen{major}.{minor}-{context}b-instruct`（如 `qwen2.5-72b-instruct`）

## 配置文件

单文件：`whosellm/models/families/alibaba.py`

## 注意事项

- Qwen 的 API 版本（qwen-turbo / qwen-plus / qwen-max）和开源版本（qwen2.5-72b-instruct）命名差异很大
- `qwen-long` 有特殊的超长上下文能力，`context_window` 与其他变体不同
- 变体优先级：`turbo < plus < max`
- 关注 `supports_function_calling`、`supports_web_search` 等参数，不同变体支持度不同
