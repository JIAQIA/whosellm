---
name: openai
description: OpenAI 模型信息采集指南
---

# OpenAI 模型信息采集

## 官方文档入口

- **模型列表页**：`https://platform.openai.com/docs/models`
- **API 参考**：`https://platform.openai.com/docs/api-reference`
- **模型发布博客**：`https://openai.com/blog`

## Playwright 操作指南

1. 导航到模型列表页后，使用 `browser_snapshot` 获取页面结构
2. OpenAI 文档使用左侧导航 + 右侧内容面板，模型信息通常在表格或卡片中
3. 部分模型详情需要点击展开，使用 `browser_click` 操作
4. 注意区分 **GA 模型**（正式版）和 **Preview 模型**（预览版），两者的能力可能不同

## 命名规则

- GPT 系列：`gpt-{major}.{minor}` 或 `gpt-{major}{variant}`（如 `gpt-4o`）
- O 系列：`o{version}` 或 `o{version}-{variant}`（如 `o3-mini`、`o3-pro`）
- 日期后缀：`-YYYY-MM-DD`
- 变体后缀：`-mini`、`-nano`、`-pro`、`-audio-preview` 等

## 配置文件组织

OpenAI 按家族拆分为多个文件，位于 `whosellm/models/families/openai/` 下：

```
openai/
├── __init__.py              # 导入所有家族
├── openai_gpt_3_5.py
├── openai_gpt_4.py
├── openai_gpt_4_1.py
├── openai_gpt_4o.py
├── openai_gpt_5.py
├── openai_o1.py
├── openai_o3.py
└── openai_o4.py
```

新增家族时在此目录创建新文件，并在 `openai/__init__.py` 中添加导入。

## 注意事项

- OpenAI 模型的 `audio-preview`、`search-preview` 等特殊变体通常需要单独的 `specific_models` 条目，因为其能力与标准变体差异较大
- `predicted_outputs` 能力并非所有模型都支持，需逐一核实
- `fine_tuning` 和 `distillation` 在 mini/nano 变体上可能有差异
