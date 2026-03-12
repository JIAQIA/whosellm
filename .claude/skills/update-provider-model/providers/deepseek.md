---
name: deepseek
description: DeepSeek 模型信息采集指南
---

# DeepSeek 模型信息采集

## 官方文档入口

- **API 文档**：`https://api-docs.deepseek.com`
- **模型列表**：`https://api-docs.deepseek.com/quick_start/pricing`
- **官网**：`https://www.deepseek.com`

## 采集策略

- **首选工具**：WebFetch（文档结构清晰，静态渲染，fetch 即可获取）
- **回退工具**：Playwright（仅当 WebFetch 返回内容不完整时）
- **可并行**：是 — WebFetch 不受 Playwright 单实例限制

## Playwright 操作指南（回退时参考）

1. DeepSeek API 文档结构清晰，`browser_snapshot` 通常可直接获取
2. 模型定价页面包含所有可用模型的 ID 和上下文窗口信息
3. 能力详情需要在各 API 端点文档中查看支持的参数

## 命名规则

- **对话模型**：`deepseek-chat`
- **推理模型**：`deepseek-reasoner`
- 命名相对简单，变体较少

## 配置文件

在 `whosellm/models/families/others.py` 中的 `DEEPSEEK` 配置

## 注意事项

- DeepSeek 目前模型数量较少但迭代快，注意关注新模型发布
- `deepseek-reasoner` 支持 `supports_thinking`，与 `deepseek-chat` 能力不同
- 若未来模型增多，考虑从 `others.py` 中拆分为独立文件
