# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指引。

## 项目概述

**whosellm** — 统一的 LLM 模型版本与能力管理库。标准化模型命名、聚合能力信息，并支持跨供应商（OpenAI、Anthropic、智谱、阿里巴巴等）的版本比较。

包名：`whosellm` | Python >=3.11 | 许可证：MIT

## 环境管理

**本项目使用 [uv](https://docs.astral.sh/uv/) 管理 Python 环境和依赖。所有命令必须通过 `uv run` 执行，禁止使用 `pip install` 或裸 `python` 命令。**

## 常用命令

所有任务命令通过 `uv run poe` 执行（[poethepoet](https://github.com/nat-n/poethepoet)）：

```bash
uv run poe dev          # 安装开发和测试依赖
uv run poe qa           # 完整流程：格式化 → 检查 → 类型检查 → 测试
uv run poe fmt          # 代码格式化（Ruff）
uv run poe lint         # 代码检查并自动修复（Ruff）
uv run poe check        # 仅检查，不修复
uv run poe typecheck    # 类型检查（MyPy，严格模式）
uv run poe test         # 运行单元测试 + 集成测试
uv run poe test-cov     # 带覆盖率的测试（不含端到端）
uv run poe test-e2e     # 仅运行端到端测试
uv run poe test-all     # 运行所有测试，详细输出
uv run poe clean        # 清理缓存和构建产物
```

运行单个测试文件或测试用例：
```bash
uv run python -m pytest tests/test_llmeta.py
uv run python -m pytest tests/test_llmeta.py::TestClassName::test_method -v
```

测试标记：`@pytest.mark.unit`、`@pytest.mark.integration`、`@pytest.mark.e2e`

版本升级：`uv run bump-my-version bump patch|minor|major`（PEP 440 格式）

## 架构

### 数据流

```
LLMeta("gpt-4o-mini")
  → __post_init__() → get_model_info()
    → MODEL_REGISTRY 精确匹配，或
    → auto_register_model() → match_model_pattern()
      → 使用 parse 库对 ModelFamilyConfig 中的模式进行匹配
      → parse_version()、infer_variant_priority()
      → register_model()（缓存结果）
  → 填充字段：provider、family、version、variant、capabilities、release_date
```

### 核心类型

- **`LLMeta`**（`model_version.py`）：主入口 dataclass。支持 `@total_ordering` 进行版本比较（版本元组 → 变体优先级 → 发布日期）。仅需模型名称字符串即可初始化。
- **`Provider`**（`provider.py`）：动态字符串枚举（OpenAI、Anthropic、Zhipu 等），运行时可通过 `add_member()` 扩展。
- **`ModelFamily`**（`models/base.py`）：动态字符串枚举，运行时可通过 `add_member()` 扩展。
- **`ModelCapabilities`**（`capabilities.py`）：冻结 dataclass，描述模型功能（thinking、vision、audio、video、function_calling 等）和限制（context_window、max_tokens 等）。
- **`ModelFamilyConfig`**（`models/config.py`）：配置 dataclass，定义模式、默认值和特定模型覆盖。创建时自动注册到全局注册表。
- **`SpecificModelConfig`**（`models/config.py`）：预注册的特定模型变体配置。

### 模块布局

- `whosellm/models/families/` — 按供应商组织的模型配置。每个文件使用 `parse` 库定义命名模式的 `ModelFamilyConfig` 实例。
- `whosellm/models/registry.py` — 全局模型族配置注册表和模式匹配逻辑。
- `whosellm/models/patterns.py` — 使用 `parse` 库自定义类型转换器的模式匹配。
- `whosellm/models/dynamic_enum.py` — `DynamicEnumMeta` 元类，支持运行时枚举扩展。

### 设计模式

- **配置驱动**：模型行为通过 `ModelFamilyConfig` 对象定义，而非代码分支。
- **注册表模式**：全局 `_FAMILY_CONFIGS` 和 `MODEL_REGISTRY` 用于模型查找，首次访问时惰性自动注册。
- **动态枚举**：`Provider` 和 `ModelFamily` 使用 `DynamicEnumMeta` 实现运行时可扩展性。
- 未知模型返回 `UNKNOWN` 族/供应商，而非抛出异常（宽容设计）。

## 代码风格

- Ruff：行长 120，双引号，Python 3.11 目标
- 允许中文标点（RUF001/002/003 已忽略）
- `__init__.py` 中忽略 `F401`（重导出）
- MyPy 严格模式（disallow_untyped_defs、no_implicit_optional）；测试文件放宽限制
- 核心依赖：`parse`（模式匹配）、`vrl-python`（参数验证）

## 添加新模型族

参见 `docs/add_new_model_family.md`。简要流程：在 `whosellm/models/families/` 中创建 `ModelFamilyConfig`，使用 `parse` 占位符（`{version}`、`{variant:variant}`、`{year:4d}` 等）定义模式，设置默认能力，并添加特定模型覆盖。配置在导入时自动注册。
