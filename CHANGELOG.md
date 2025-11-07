# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **模型家族（ModelFamily）概念** - 区分模型家族和提供商，同一模型家族可能由多个Provider提供
- **型号优先级比较系统** - 支持同一家族下不同型号的智能比较
  - GPT-4 系列: `gpt-4o-mini < gpt-4 < gpt-4-turbo < gpt-4o`
  - GLM-4 系列: `glm-4-flash < glm-4 < glm-4-plus`
  - GLM-4V 系列: `glm-4v-flash < glm-4v < glm-4v-plus < glm-4v-plus-0111`
  - O1 系列: `o1-mini < o1-preview < o1`
- **Provider指定语法** - 支持 `{{Provider::ModelName}}` 和 `Provider::ModelName` 语法来显式指定Provider
- **variant_priority字段** - 在 `ModelInfo` 中添加型号优先级元组，用于同版本不同型号的比较
- **高级示例文件** - 添加 `examples/advanced_usage.py` 展示新功能的使用

### Changed
- **比较逻辑优化** - 模型比较从基于Provider改为基于ModelFamily，更符合实际使用场景
- **版本比较增强** - 先比较版本号，版本相同时再比较型号优先级
- **错误提示改进** - 不同家族模型比较时的错误提示更加清晰

### Updated
- 所有现有模型注册都添加了 `family` 和 `variant_priority` 字段
- OpenAI 模型定义（gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo, o1, o1-mini, o1-preview）
- 智谱 AI 模型定义（glm-4, glm-4-plus, glm-4-flash, glm-4v, glm-4v-plus, glm-4v-plus-0111, glm-4v-flash, glm-3-turbo）
- 测试用例更新以验证新功能
- README 文档更新，添加新功能说明和使用示例

## [0.1.0] - 2025-11-07

### Added
- 初始版本发布
- 基础模型版本管理功能
- Provider 自动检测
- 模型能力描述系统
- 基础版本比较功能
