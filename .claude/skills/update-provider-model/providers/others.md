---
name: others
description: 其他供应商（百度、腾讯、Moonshot、MiniMax）模型信息采集指南
---

# 其他供应商模型信息采集

以下供应商当前配置在 `whosellm/models/families/others.py` 中。

## 采集策略（通用）

以下供应商均为中文 SPA 或需要交互操作的文档：

- **首选工具**：Playwright（百度、腾讯、MiniMax 均为中文 SPA）
- **例外**：Moonshot 文档结构较简单，可尝试 WebFetch
- **可并行**：Playwright 供应商之间不可并行；Moonshot 若用 WebFetch 则可并行
- **重要**：使用 Playwright 时必须独占浏览器，不可与其他 Playwright Agent 并发

## 百度 (Baidu) - 文心一言

- **文档**：`https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html`
- **命名**：`ernie-{variant}`（如 `ernie-4.0`、`ernie-speed`）
- **采集工具**：Playwright（百度云文档为中文 SPA，需动态加载）

## 腾讯 (Tencent) - 混元

- **文档**：`https://cloud.tencent.com/document/product/1729`
- **命名**：`hunyuan-{variant}`（如 `hunyuan-pro`、`hunyuan-lite`）
- **采集工具**：Playwright（腾讯云文档结构较深，需多次导航）

## Moonshot (月之暗面)

- **文档**：`https://platform.moonshot.cn/docs`
- **命名**：`moonshot-v1-{context}`（如 `moonshot-v1-8k`、`moonshot-v1-128k`）
- **采集工具**：WebFetch 优先（文档结构简单），Playwright 回退
- 上下文窗口是 Moonshot 的核心区分点

## MiniMax

- **文档**：`https://platform.minimaxi.com/document`
- **命名**：`abab{version}-{variant}`（如 `abab6.5s`、`abab5.5`）
- **采集工具**：Playwright（需要交互操作）
- 命名格式较特殊，注意版本号紧跟在 `abab` 后面无分隔符

## 通用注意事项

- 如果某供应商的模型数量增长到 3 个以上家族，建议从 `others.py` 拆分为独立文件
- 拆分时需要更新 `families/__init__.py` 的导入
