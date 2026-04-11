---
name: update-provider-model
description: 更新或新增 Provider-Model 配置的完整工作流，包括信息采集、代码变更、测试覆盖。仅指定 Provider 时自动发现新模型。
user-invocable: true
argument-hint: [provider] [model-name]
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# 更新/新增 Provider-Model 配置

本技能指导完成一个 Provider 下模型配置的新增或更新，覆盖：信息采集 → 代码变更 → 测试验证 全链路。

目标模型：$ARGUMENTS

---

## 第零步：判断运行模式

根据用户输入判断进入哪种工作模式：

| 输入形式 | 示例 | 运行模式 |
|---------|------|---------|
| `[provider] [model-name]` | `openai gpt-4o-mini` | **指定模型模式** — 直接跳到第一步 |
| `[provider]` | `openai` | **自动发现模式** — 进入下方发现流程 |

### 自动发现模式

仅指定 Provider 时，自动从官方文档发现本仓库尚未收录或配置过时的模型。

#### D1. 盘点仓库现有模型

读取该 Provider 对应的配置文件，提取所有已注册的模型 ID 列表：

```bash
# 定位配置文件
# 单文件供应商
whosellm/models/families/{provider}.py
# 多文件供应商（如 openai）
whosellm/models/families/{provider}/
```

使用代码提取已注册模型：

```python
uv run python -c "
from whosellm.models.registry import get_all_registered_models
from whosellm.provider import Provider

provider = Provider.{PROVIDER_UPPER}
registered = get_all_registered_models()
models = {name: info for name, info in registered.items() if info.provider == provider}
for name in sorted(models):
    print(name)
"
```

如果上述 API 不存在，改为直接读取配置文件中 `specific_models` 字典的所有 key，以及 `ModelFamilyConfig` 的 `patterns` 列表来推断覆盖范围。

#### D2. 采集官方最新模型列表

查阅 `${CLAUDE_SKILL_DIR}/providers/{provider}.md` 中的**采集策略**和**官方文档入口**，获取该 Provider 当前提供的完整模型列表。

采集目标：
- 所有可用的模型 ID（API 中的 model name）
- 每个模型的状态：GA / Preview / Deprecated / Experimental

**注意**：
- 优先采集 GA（正式版）和 Preview（预览版）模型，Experimental（实验版）可标记但不强制收录
- 已标记 Deprecated 的模型如仓库已有则保留，无需新增
- 遵守浏览器并发控制规则（见第一步"浏览器并发控制"章节）

#### D3. 差异比对

将官方模型列表与仓库已注册列表对比，生成发现报告：

```markdown
## 模型发现报告：{Provider}

### 采集时间：{date}
### 官方文档来源：{url}

### 🆕 新增模型（仓库未收录）

| 模型 ID | 状态 | 所属家族（推测） | 说明 |
|---------|------|----------------|------|
| gpt-4o-mini-2025-04-16 | GA | GPT_4O | 新 snapshot |
| o3-pro | GA | O3 | 新变体 |

### 🔄 可能需要更新（已收录但可能过时）

| 模型 ID | 可疑项 | 说明 |
|---------|--------|------|
| gpt-4o | context_window | 官方已从 128K 提升到 200K |

### ✅ 已覆盖（无需操作）

已收录 {N} 个模型，与官方一致。

### ⏭️ 跳过（不收录）

| 模型 ID | 原因 |
|---------|------|
| xxx-exp-0401 | Experimental，暂不收录 |
```

#### D4. 向用户展示报告并确认

**必须先展示发现报告，等用户确认要处理哪些模型后，再逐个执行更新。**

用户可能的回复：
- "全部更新" — 按顺序处理所有新增和需更新的模型
- "只更新 xxx 和 yyy" — 仅处理指定模型
- "先不更新" — 结束流程

对于用户确认要处理的每个模型，进入下方**第一步**开始正式的采集 → 代码变更 → 测试流程。

如果需要处理多个模型：
- **同一家族的多个 snapshot 变体**（如 `gpt-4o-2025-04-16`）：通常只需确认已有 patterns 能匹配，无需新增 `specific_models` 条目
- **新的变体**（如 `o3-pro`）：需要完整走一遍新增流程
- **能力字段更新**：直接修改对应 `specific_models` 中的 `capabilities`

---

## 第一步：采集官方模型信息

### 采集工具选择

每个供应商的指引文件（`${CLAUDE_SKILL_DIR}/providers/*.md`）中标注了**首选采集工具**：

- **WebFetch 优先**：文档为静态渲染，直接 fetch 即可获取完整信息（如 Anthropic、DeepSeek、Google Gemini）
- **Playwright 必需**：文档为 SPA/动态加载，或需要交互展开（如智谱、阿里巴巴、OpenAI）

**请先查阅对应供应商指引文件的 `采集策略` 章节，按标注的首选工具操作。**

### 浏览器并发控制（重要）

> **Playwright MCP 为单实例共享浏览器。多个 Agent 并发操作会产生页面竞争（导航覆盖、快照错乱），必须避免。**

**规则：任何时刻只允许一个 Agent 使用 Playwright。** 如果需要采集多个供应商的信息，采用以下策略：

1. **串行采集**：单个 Agent 依次访问各供应商文档，将采集结果保存到临时文件（如 `/tmp/collect-{provider}.md`）
2. **并行分析**：采集完成后，多个 Agent 可各自读取临时文件 + 代码配置，并行执行比对/修改/测试
3. **WebFetch 不受此限制**：标注为 WebFetch 优先的供应商可与 Playwright 采集并行进行

### 操作流程

1. **查阅 `${CLAUDE_SKILL_DIR}/providers/` 目录下对应供应商的指引文件**，获取官方文档 URL、首选采集工具和操作注意事项。
2. **根据首选工具执行采集**：
   - **WebFetch 路径**：直接使用 `WebFetch` 获取文档页面内容
   - **Playwright 路径**：
     1. 使用 `mcp__plugin_playwright_playwright__browser_navigate` 打开文档页面
     2. 使用 `mcp__plugin_playwright_playwright__browser_snapshot` 获取页面结构
     3. 使用 `mcp__plugin_playwright_playwright__browser_click` 展开折叠区域/切换标签
3. 如果首选工具获取不完整，回退使用另一工具补充。

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
