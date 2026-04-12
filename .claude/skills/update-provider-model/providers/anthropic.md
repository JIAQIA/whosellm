---
name: anthropic
description: Anthropic Claude 模型信息采集指南
---

# Anthropic Claude 模型信息采集

## 官方文档入口

- **模型列表页**：`https://docs.anthropic.com/en/docs/about-claude/models`
- **API 参考**：`https://docs.anthropic.com/en/api`
- **发布公告**：`https://www.anthropic.com/news`

## 采集策略

- **首选工具**：WebFetch（文档为静态渲染，fetch 即可获取完整内容）
- **回退工具**：Playwright（仅当 WebFetch 返回内容不完整时）
- **可并行**：是 — WebFetch 不受 Playwright 单实例限制

## Playwright 操作指南（回退时参考）

1. Anthropic 文档为静态渲染，`browser_snapshot` 通常能直接获取完整信息
2. 模型列表页包含所有模型的能力矩阵表格，是最主要的信息来源
3. 注意页面可能有多个标签页（Overview / API / Pricing），需要切换查看

## 命名规则

Claude 有两种命名格式（新旧版本不同）：

- **新格式**（4.0+）：`claude-{variant}-{major}-{minor}`（如 `claude-sonnet-4-5`）
- **旧格式**（3.x）：`claude-{major}-{minor}-{variant}`（如 `claude-3-5-haiku`）
- **Snapshot 后缀**：`-YYYYMMDD` 或 `@YYYYMMDD`（如 `claude-sonnet-4-5-20250514`）

## 配置文件

单文件：`whosellm/models/families/anthropic.py`

所有 Claude 模型属于同一个 `ModelFamily.CLAUDE` 家族，通过 `specific_models` 区分版本和变体。

## 注意事项

- Claude 的 `max_tokens` 因版本不同差异较大（3-haiku: 4000, 3-5-haiku: 8000, opus: 32000, sonnet: 64000）
- 所有 Claude 模型的 `context_window` 目前统一为 200000
- `supports_thinking` 从 3.7-sonnet 开始支持，3.5 及更早版本不支持
- `supports_computer_use` 等能力需要逐模型确认
- 变体优先级：`haiku=0, sonnet=3, opus=5`
