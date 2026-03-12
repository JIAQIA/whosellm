---
name: others
description: 其他供应商（百度、腾讯、Moonshot、MiniMax）模型信息采集指南
---

# 其他供应商模型信息采集

以下供应商当前配置在 `whosellm/models/families/others.py` 中。

## 百度 (Baidu) - 文心一言

- **文档**：`https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html`
- **命名**：`ernie-{variant}`（如 `ernie-4.0`、`ernie-speed`）
- Playwright 注意：百度云文档为中文 SPA，需动态加载

## 腾讯 (Tencent) - 混元

- **文档**：`https://cloud.tencent.com/document/product/1729`
- **命名**：`hunyuan-{variant}`（如 `hunyuan-pro`、`hunyuan-lite`）
- Playwright 注意：腾讯云文档结构较深，需多次导航

## Moonshot (月之暗面)

- **文档**：`https://platform.moonshot.cn/docs`
- **命名**：`moonshot-v1-{context}`（如 `moonshot-v1-8k`、`moonshot-v1-128k`）
- 上下文窗口是 Moonshot 的核心区分点

## MiniMax

- **文档**：`https://platform.minimaxi.com/document`
- **命名**：`abab{version}-{variant}`（如 `abab6.5s`、`abab5.5`）
- 命名格式较特殊，注意版本号紧跟在 `abab` 后面无分隔符

## 通用注意事项

- 如果某供应商的模型数量增长到 3 个以上家族，建议从 `others.py` 拆分为独立文件
- 拆分时需要更新 `families/__init__.py` 的导入
