# Changelog

All notable changes to this project will be documented in this file.

## [0.2.2] - 2026-04-24

### Added
- DeepSeek V4 系列模型支持：`deepseek-v4-flash`、`deepseek-v4-pro`（1M 上下文，384K 最大输出，支持思考/非思考双模式）
- DeepSeek 官方 Provider 支持版本号命名模式（`deepseek-v{major}.{minor}-{variant}` 等），V4 起可通过版本号直接调用
- 腾讯云 DeepSeek-V3.2（GA 版，685B MoE，稀疏注意力）

### Changed
- `deepseek-chat` / `deepseek-reasoner` 能力基线升级为 V4-flash 非思考/思考模式别名（1M 上下文，384K 输出）

### Fixed
- 腾讯云 `deepseek-r1-0528` 的 `supports_function_calling` 修正为 `False`（官方文档明确列为不支持）

## [Unreleased]

### Added
- **模型家族（ModelFamily）概念** - 区分模型家族和提供商，同一模型家族可能由多个Provider提供
- **型号优先级比较系统** - 支持同一家族下不同型号的智能比较
  - GPT-4 系列: `gpt-4o-mini < gpt-4 < gpt-4-turbo < gpt-4o`
  - GLM-4 系列: `glm-4-flash < glm-4 < glm-4-plus`
  - GLM-4V 系列: `glm-4v-flash < glm-4v < glm-4v-plus < glm-4v-plus-0111`
  - O1 系列: `o1-mini < o1-preview < o1`
- **Provider指定语法** - 支持 `Provider::ModelName` 语法来显式指定Provider
- **variant_priority字段** - 在 `ModelInfo` 中添加型号优先级元组，用于同版本不同型号的比较
- **发布日期支持** - 支持从模型名称中自动解析发布日期
  - 支持 `YYYY-MM-DD` 格式（如 `gpt-4-turbo-2024-04-09`）
  - 支持 `MMDD` 格式（如 `gpt-4-0125-preview`）
  - 无日期的模型被认为是最新版本（指向 latest）
- **日期比较功能** - 在版本和型号相同时，通过日期进行精确比较
- **高级示例文件** - 添加 `examples/advanced_usage.py` 展示新功能的使用

### Changed
- **比较逻辑优化** - 模型比较从基于Provider改为基于ModelFamily，更符合实际使用场景
- **版本比较增强** - 比较顺序：版本 > 型号优先级 > 发布日期
- **错误提示改进** - 不同家族模型比较时的错误提示更加清晰
- **测试框架兼容** - 测试类现在同时兼容 pytest 和 unittest，方便 PyCharm 运行

### Updated
- 所有现有模型注册都添加了 `family` 和 `variant_priority` 字段
- OpenAI 模型定义（gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo, o1, o1-mini, o1-preview）
  - 新增带日期的模型：`gpt-4-turbo-2024-04-09`, `gpt-4-0125-preview`
- 智谱 AI 模型定义（glm-4, glm-4-plus, glm-4-flash, glm-4v, glm-4v-plus, glm-4v-plus-0111, glm-4v-flash, glm-3-turbo）
- 测试用例更新以验证新功能（新增3个日期相关测试）
- README 文档更新，添加新功能说明和使用示例

## [0.1.0] - 2025-11-07

### Added
- 初始版本发布
- 基础模型版本管理功能
- Provider 自动检测
- 模型能力描述系统
- 基础版本比较功能
