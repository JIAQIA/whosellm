---
name: update-provider-model
description: 更新或新增 Provider-Model 配置的完整工作流，包括信息采集、代码变更、测试覆盖
user-invocable: true
argument-hint: [provider] [model-name]
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# 更新/新增 Provider-Model 配置

本技能指导完成一个 Provider 下模型配置的新增或更新，覆盖：信息采集 → 代码变更 → 测试验证 全链路。

目标模型：$ARGUMENTS

---

## 第一步：采集官方模型信息

### 推荐工具：Playwright MCP

很多 LLM 供应商的官方文档对搜索引擎不友好（SPA、动态加载、需要交互操作），因此**优先使用 Playwright MCP 浏览器工具**访问供应商官方网站。

#### 操作流程

1. **查阅 `${CLAUDE_SKILL_DIR}/providers/` 目录下对应供应商的指引文件**，获取该供应商的官方文档 URL 和操作注意事项。
2. **使用 `mcp__plugin_playwright_playwright__browser_navigate`** 打开供应商的模型文档页面。
3. **使用 `mcp__plugin_playwright_playwright__browser_snapshot`** 获取页面结构，定位模型列表或模型详情区域。
4. **使用 `mcp__plugin_playwright_playwright__browser_click`** 展开折叠区域、切换标签页，获取完整信息。
5. 如果页面无法正常渲染，回退使用 **WebSearch + WebFetch** 作为补充。

#### 需要采集的信息

| 字段 | 说明 | 示例 |
|------|------|------|
| 模型名称 | 官方 API 中使用的 model ID | `gpt-4o-mini-2025-04-16` |
| 模型家族 | 所属系列 | GPT-4o / Claude / GLM-4 |
| 版本号 | 主版本.次版本 | `4.0`、`3.7` |
| 变体名称 | mini / pro / plus / turbo 等 | `mini` |
| 能力参数 | vision / thinking / function_calling / streaming 等 | `supports_vision=True` |
| 上下文窗口 | context_window | `128000` |
| 最大输出 | max_tokens | `16384` |
| 命名模式 | 名称中包含的日期/snapshot 格式 | `{year:4d}-{month:2d}-{day:2d}` |
| 发布日期 | 模型发布时间 | `2025-04-16` |

---

## 第二步：代码变更链条

按以下顺序修改文件，每一步都有前置依赖：

### 2.1 新增 Provider（仅当供应商不存在时）

**文件：** `whosellm/provider.py`

- 在 `Provider` 枚举中添加新成员（放在 `UNKNOWN` 之前）

```python
MY_PROVIDER = "my-provider"  # 中文名
```

### 2.2 新增 ModelFamily（仅当模型族不存在时）

**文件：** `whosellm/models/base.py`

- 在 `ModelFamily` 枚举中添加新成员

```python
MY_MODEL = "my-model"
```

### 2.3 创建或更新模型家族配置

**文件：** `whosellm/models/families/{provider}.py` 或 `whosellm/models/families/{provider}/{provider}_{family}.py`

- 单文件供应商（如 anthropic、zhipu）直接修改现有文件
- OpenAI 等多文件供应商在子目录中按家族拆分

配置模板：

```python
from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

MY_FAMILY = ModelFamilyConfig(
    family=ModelFamily.MY_MODEL,
    provider=Provider.MY_PROVIDER,
    version_default="1.0",
    variant_default="base",
    variant_priority_default=(1,),
    patterns=[
        # 模式顺序：最具体 → 最通用
        "my-model-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "my-model-{variant:variant}",
        "my-model-{year:4d}-{month:2d}-{day:2d}",
        "my-model",
    ],
    capabilities=ModelCapabilities(
        # 从官方文档采集的默认能力
        supports_streaming=True,
        supports_function_calling=True,
    ),
    specific_models={
        "my-model-pro": SpecificModelConfig(
            version="1.0",
            variant="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                # 此变体的特定能力覆盖
            ),
            patterns=[
                "my-model-pro-{year:4d}-{month:2d}-{day:2d}",
                "my-model-pro",
            ],
        ),
    },
)
```

#### 关键规则

- **模式顺序**：从最具体到最通用排列，确保带日期的模式在前
- **specific_models 的子模式必须是父模式的子集**，否则 `__post_init__` 校验会报错
- **variant_priority 取值约定**：`mini=0, base=1, flash=2, sonnet=3, turbo=3, plus/pro=4, opus/ultra=5, omni=6`
- **capabilities 要准确反映官方文档**，不要猜测或默认为 True

### 2.4 注册导入

**文件：** `whosellm/models/families/__init__.py`（或对应子目录的 `__init__.py`）

- 确保新模块被导入，触发 `ModelFamilyConfig.__post_init__` 自动注册

### 2.5 变更检查清单

- [ ] Provider 枚举已添加（如需要）
- [ ] ModelFamily 枚举已添加（如需要）
- [ ] ModelFamilyConfig 已创建，patterns 顺序正确
- [ ] specific_models 中每个变体的 capabilities 均来自官方文档
- [ ] `families/__init__.py` 已导入新模块
- [ ] 代码通过 `poe check` 和 `poe typecheck`

---

## 第三步：测试最佳实践

详细的测试指南见 [testing.md](testing.md)。

### 运行测试

```bash
# 运行单个家族测试
python -m pytest tests/models/families/test_{family}.py -v

# 运行全部测试确保无回归
poe test

# 完整质量检查（格式化 + 检查 + 类型检查 + 测试）
poe qa
```

---

## 快速参考：完整变更文件清单

| 步骤 | 文件 | 操作 |
|------|------|------|
| Provider 枚举 | `whosellm/provider.py` | 新增成员 |
| Family 枚举 | `whosellm/models/base.py` | 新增成员 |
| 家族配置 | `whosellm/models/families/{provider}.py` | 创建/更新 ModelFamilyConfig |
| 注册导入 | `whosellm/models/families/__init__.py` | 添加 import |
| 家族测试 | `tests/models/families/test_{family}.py` | 新建测试文件 |
| 集成测试 | `tests/test_llmeta.py` | 添加端到端用例（可选） |
| 变体优先级 | `tests/test_variant_priority_config.py` | 添加参数化用例（可选） |
