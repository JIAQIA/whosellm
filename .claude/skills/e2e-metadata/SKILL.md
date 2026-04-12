---
name: e2e-metadata
description: 从官方文档采集真实元数据，生成 E2E 测试验证 LLMeta 解析准确性。发现不一致时排查并修复代码库。可指定 Provider/模型名称，或自动发现未覆盖模型。
user-invocable: true
argument-hint: "[provider] [model-name]"
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent, WebSearch, WebFetch, AskUserQuestion
---

# E2E 元数据测试 — 官方文档驱动

从真实世界的官方文档采集模型元数据，作为唯一的期望值来源，验证 `LLMeta` 解析结果的准确性。

目标模型：$ARGUMENTS

---

## 核心原则

**期望值的唯一来源是官方文档，不是代码库。**

代码库是被测对象，不是参照物。工作流：

```
采集官方文档（WebSearch + Playwright）
        ↓
  整理为期望数据
        ↓
  对比 LLMeta 解析结果
        ↓
   一致 → 写入测试文件
   不一致 → 排查并修复代码库 → 再写入测试文件
```

这确保了测试是对代码库的"外部审计"——如果代码库错了，测试会失败而不是跟着错。

---

## 第零步：判断运行模式

| 输入形式 | 示例 | 运行模式 |
|---------|------|---------|
| `[provider] [model-name]` | `openai gpt-5.4-mini` | **指定模型模式** — 跳到第一步 |
| `[provider]` | `openai` | **自动发现模式** — 进入下方发现流程 |
| 无参数 | `/e2e-metadata` | **全量扫描模式** — 扫描所有 Provider |

### 自动发现流程

**只关注每个 Family 的最新版本**——不逐版本全量覆盖。老版本需要时通过 `[provider] [model-name]` 手动指定。

#### D1. 盘点已有 E2E 测试覆盖

读取 `tests/test_e2e_metadata.py`，提取所有已覆盖的 model_name 列表。

#### D2. 提取每个 Family 的最新版本模型

从注册表中按 Family 分组，取 `version_default` 最高的那组 config 对应的 `specific_models`：

```bash
uv run python -c "
from whosellm.models.registry import _FAMILY_CONFIGS
from whosellm.provider import Provider

target = Provider.OPENAI  # 替换为目标 Provider

# 按 family 分组，取最新版本（version_default 最大的 config）
family_latest: dict[str, tuple[str, list[str]]] = {}
for (family, provider), config in _FAMILY_CONFIGS.items():
    if provider != target:
        continue
    fkey = family.value
    ver = config.version_default
    if fkey not in family_latest or ver > family_latest[fkey][0]:
        family_latest[fkey] = (ver, sorted(config.specific_models.keys()))

for fkey, (ver, models) in sorted(family_latest.items()):
    for m in models:
        print(f'{fkey}\t{ver}\t{m}')
"
```

例如 OpenAI 的结果：
- GPT family → version 5.4 → `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.4-pro`
- GPT_4O family → version 4.0 → `gpt-4o-mini`, `gpt-4o-audio-preview`, ...
- O family → version 4.0 → `o4-mini`, `o4-mini-deep-research`

#### D3. 差异比对 + 展示报告

对比最新版本模型与已有 E2E 用例，向用户展示未覆盖列表：

```markdown
## E2E 覆盖报告（仅最新版本）

### 未覆盖模型（{n} 个）

| Family | 最新版本 | 模型 ID |
|--------|---------|---------|
| gpt    | 5.4     | gpt-5.4-pro |

### 已覆盖（{n} 个）

已有 E2E 用例覆盖 {n} 个最新版本模型。
```

确认后进入第一步。

---

## 第一步：从官方文档采集元数据

**禁止从代码库 `whosellm/models/families/` 读取配置作为期望值。**

### 1.1 确定采集策略

查阅 `${CLAUDE_SKILL_DIR}/../update-provider-model/providers/{provider}.md`，获取：

- 官方文档 URL
- 首选采集工具（WebFetch 或 Playwright）
- 操作注意事项

各 Provider 采集策略速查：

| Provider | 首选工具 | 官方文档入口 | 可并行 |
|----------|---------|------------|--------|
| OpenAI | Playwright | `https://platform.openai.com/docs/models` | 否 |
| Anthropic | WebFetch | `https://docs.anthropic.com/en/docs/about-claude/models` | 是 |
| Google | WebFetch | `https://ai.google.dev/gemini-api/docs/models` | 是 |
| 智谱 | Playwright | `https://open.bigmodel.cn/dev/howuse/model` | 否 |

### 1.2 执行采集

#### WebSearch 路径（适合快速定位特定模型信息）

```
WebSearch: "{model_name} context window max tokens site:{provider_docs_domain}"
```

典型搜索示例：
- `gpt-5.4-mini context window max output tokens site:platform.openai.com`
- `claude-sonnet-4-6 model capabilities site:docs.anthropic.com`
- `gemini-2.5-flash context window site:ai.google.dev`

WebSearch 适合：
- 快速确认单个模型的特定字段值
- 查找模型发布公告中的能力说明
- 交叉验证 Playwright 采集的数据

#### WebFetch 路径（Anthropic、Google 等静态文档）

直接 fetch 模型列表页，解析表格中的能力矩阵：

```
WebFetch: "https://docs.anthropic.com/en/docs/about-claude/models"
WebFetch: "https://ai.google.dev/gemini-api/docs/models"
```

#### Playwright 路径（OpenAI、智谱等动态 SPA）

1. `browser_navigate` → 模型文档页
2. `browser_snapshot` → 获取页面结构
3. `browser_click` → 展开折叠区域/切换标签
4. 重复 snapshot + click 直到获取所有模型信息

**Playwright 并发控制**：任何时刻只允许一个 Agent 使用 Playwright。如需多 Provider 采集：
- 串行使用 Playwright 采集各 Provider，将结果保存到临时文件
- WebFetch 类 Provider 可与 Playwright 并行

### 1.3 必须采集的字段

按优先级排列：

| 优先级 | 字段 | 采集来源 | 说明 |
|--------|------|---------|------|
| **P0** | `context_window` | 模型卡片/表格 | Token 截断策略，必须精确 |
| **P0** | `max_tokens`（最大输出） | 模型卡片/表格 | 输出截断策略，必须精确 |
| **P0** | `supports_thinking` | 功能描述/API 参数 | 是否支持 reasoning/thinking 模式 |
| **P0** | `supports_vision` | 输入模态说明 | 是否支持图像输入 |
| **P1** | `supports_audio` | 输入模态说明 | 是否支持音频输入 |
| **P1** | `supports_function_calling` | API 功能说明 | 是否支持 tool use / function calling |
| **P1** | `supports_streaming` | API 功能说明 | 是否支持流式响应 |
| **P1** | `supports_structured_outputs` | API 功能说明 | 是否支持 JSON Schema 约束的结构化输出 |
| **P2** | `supports_video` | 输入模态说明 | 是否支持视频输入 |
| **P2** | `supports_web_search` | 工具能力说明 | 是否支持联网搜索 |
| **P2** | `supports_computer_use` | 工具能力说明 | 是否支持计算机操作 |

**数值字段的识别技巧**：
- `context_window`：官方文档中通常标注为 "context window"、"input tokens"、"max input"
- `max_tokens`：通常标注为 "max output tokens"、"max completion tokens"
- 注意单位，部分文档用 K（千）表示，如 "128K" = 128,000

### 1.4 整理采集结果

将采集到的原始数据整理为结构化记录（临时用于比对，不写入代码）：

```
模型: gpt-5.4-mini
来源: https://platform.openai.com/docs/models/gpt-5.4-mini
采集时间: 2026-04-12
---
context_window: 400,000
max_tokens: 128,000
supports_thinking: true (reasoning model)
supports_vision: true (image input supported)
supports_audio: false
supports_streaming: true
supports_function_calling: true
supports_structured_outputs: true
```

---

## 第二步：对比 LLMeta 解析结果

### 2.1 获取 LLMeta 当前输出

```bash
uv run python -c "
from whosellm import LLMeta
m = LLMeta('{model_name}')
c = m.capabilities
print(f'provider: {m.provider.value}')
print(f'family: {m.family.value}')
print(f'version: {m.version}')
print(f'variant: {m.variant}')
print(f'supports_thinking: {c.supports_thinking}')
print(f'supports_vision: {c.supports_vision}')
print(f'supports_audio: {c.supports_audio}')
print(f'supports_streaming: {c.supports_streaming}')
print(f'supports_function_calling: {c.supports_function_calling}')
print(f'supports_structured_outputs: {c.supports_structured_outputs}')
print(f'context_window: {c.context_window}')
print(f'max_tokens: {c.max_tokens}')
"
```

### 2.2 逐字段比对

对比官方采集值与 LLMeta 输出：

| 字段 | 官方文档值 | LLMeta 输出 | 状态 |
|------|-----------|------------|------|
| context_window | 400,000 | 400000 | OK |
| supports_thinking | true | True | OK |
| supports_vision | true | False | **MISMATCH** |

### 2.3 处理不一致

发现不一致时，**不要直接修改代码**。必须先输出完整报告，由用户逐条确认后再修改。

#### 2.3.1 输出不一致报告

将所有不一致项汇总为一份报告，**每条必须注明参考链接**：

```markdown
## 元数据不一致报告

### 1. {model_name} — `{field_name}`

| | 值 |
|---|---|
| 官方文档 | True |
| LLMeta 当前值 | False |
| 配置来源 | 继承自 GPT-5.3 family default（`openai_gpt_5_3.py`） |
| 参考链接 | https://developers.openai.com/api/docs/models/gpt-5.3 |

**建议修复**：在 `specific_models["gpt-5.3"]` 中添加独立 capabilities，设置 `supports_vision=True`。

---

### 2. {model_name} — `{field_name}`

...（同上格式）
```

#### 2.3.2 逐条确认

**使用 `AskUserQuestion` 工具逐条向用户确认**，每条不一致项单独询问：

```
不一致 #1: o4-mini 的 supports_thinking
- 官方文档：True（https://developers.openai.com/api/docs/models/o4-mini）
- LLMeta 当前值：False
- 建议：添加 supports_thinking=True

是否按照官方文档修复？(y/n/跳过)
```

用户可能的回复：
- **确认修复**（"y"、"是"、"修"）→ 记录为待修复
- **拒绝修复**（"n"、"否"、"不改"）→ 跳过，以 LLMeta 当前值写入测试
- **存疑需要进一步验证**（"不确定"、"再查一下"）→ 暂不处理该字段，不写入测试

**全部确认完毕后**，才开始修改代码。

#### 2.3.3 执行用户确认的修复

仅修改用户明确确认的项：

1. **定位配置文件**：`whosellm/models/families/{provider}/*.py`
2. **修改 capabilities 中对应字段值**
3. **如果是继承问题**（模型无独立 capabilities，错误继承了 family default）：
   - 为该模型添加独立的 `capabilities=ModelCapabilities(...)` 覆盖
4. **运行现有测试确认修复无回归**：`uv run python -m pytest tests/ -v`

---

## 第三步：写入测试文件

仅当第二步的所有不一致项都经过用户逐条确认（并完成修复或明确跳过）后，才写入测试。

测试期望值的来源：
- **用户确认修复的字段** → 以官方文档值（修复后的 LLMeta 输出）写入
- **用户拒绝修复的字段** → 以 LLMeta 当前值写入（代表用户认为官方文档不准确或有特殊原因）
- **用户存疑的字段** → 不写入该字段的断言（留待下次确认）

### 3.1 目录结构

```
tests/e2e/
├── __init__.py
├── conftest.py              # 共享断言函数 assert_model_metadata()
├── test_openai.py           # OpenAI: GPT, GPT_4O, O
├── test_anthropic.py        # Anthropic: CLAUDE
├── test_google.py           # Google: GEMINI
├── test_zhipu.py            # Zhipu: GLM, GLM_VISION
└── test_{provider}.py       # 新增 Provider 时添加对应文件
```

**设计原则**：

| 原则 | 说明 |
|------|------|
| **一 Provider 一文件** | 按 Provider 拆分文件，便于定位和独立运行（`pytest tests/e2e/test_openai.py`） |
| **断言逻辑集中** | `conftest.py` 中的 `assert_model_metadata()` 是唯一的断言入口，所有 test 文件共用 |
| **数据即文档** | 每个数据列表上方标注官方来源 URL 和采集日期，方便追溯和复查 |
| **最新版本优先** | 自动发现模式只覆盖每个 Family 的最新版本；老版本按需手动添加 |

### 3.2 conftest.py — 共享断言

```python
# tests/e2e/conftest.py
from whosellm import LLMeta

def assert_model_metadata(model_name: str, expected: dict) -> None:
    model = LLMeta(model_name)
    assert model.provider == expected["provider"], f"{model_name}: provider"
    assert model.family == expected["family"], f"{model_name}: family"
    assert model.version == expected["version"], f"{model_name}: version"
    assert model.variant == expected["variant"], f"{model_name}: variant"
    for key, value in expected.items():
        if key in ("provider", "family", "version", "variant"):
            continue
        if key in ("context_window", "max_tokens"):
            assert getattr(model.capabilities, key) == value, f"{model_name}: {key}"
        elif key.startswith("supports_"):
            assert getattr(model.capabilities, key) is value, f"{model_name}: {key}"
```

修改断言逻辑时只改这一个文件，所有 Provider 的测试同步生效。

### 3.3 test_{provider}.py — 文件模板

每个 Provider 测试文件遵循相同结构：

```python
"""{Provider} E2E 元数据测试。

来源: {官方文档 URL}
采集日期: {YYYY-MM-DD}
"""
import pytest
from whosellm import ModelFamily, Provider
from .conftest import assert_model_metadata

# ============================================================================
# {Family} Family (latest: {version})
# 来源: {具体模型页 URL}
# ============================================================================

{FAMILY}_MODELS = [
    (
        "{model-name}",
        {
            "provider": Provider.XXX,
            "family": ModelFamily.XXX,
            "version": "X.Y",
            "variant": "xxx",
            # P0 字段（必须）
            "supports_thinking": bool,
            "supports_vision": bool,
            "context_window": int,
            "max_tokens": int,
            # P1 字段（推荐）
            "supports_function_calling": bool,
            "supports_streaming": bool,
            "supports_structured_outputs": bool,
            # 区分性特征（该模型与同系列其他模型的差异点）
        },
    ),
]

ALL_MODELS = {FAMILY}_MODELS  # 多个 Family 用 + 拼接

@pytest.mark.e2e
@pytest.mark.parametrize("model_name,expected", ALL_MODELS, ids=[m[0] for m in ALL_MODELS])
def test_model_metadata(model_name: str, expected: dict) -> None:
    """验证 {Provider} 模型元数据与官方文档一致。"""
    assert_model_metadata(model_name, expected)
```

### 3.4 数据条目规范

**必须字段**（每条用例都要有）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `provider` | `Provider.XXX` | 身份标识 |
| `family` | `ModelFamily.XXX` | 身份标识 |
| `version` | `str` | 身份标识 |
| `variant` | `str` | 身份标识 |
| `supports_thinking` | `bool` | P0 — 是否支持推理模式 |
| `supports_vision` | `bool` | P0 — 是否支持图像输入 |
| `context_window` | `int` | P0 — 上下文窗口（官方有明确值时） |
| `max_tokens` | `int` | P0 — 最大输出（官方有明确值时） |

**推荐字段**（尽量覆盖）：

| 字段 | 说明 |
|------|------|
| `supports_function_calling` | 工具调用 |
| `supports_streaming` | 流式响应 |
| `supports_structured_outputs` | JSON Schema 结构化输出 |

**区分性字段**（按需添加）：

当某字段值与同系列其他模型**不同**时，必须显式写入以捕获回归。例如：
- `gpt-5.4-nano` 的 `supports_computer_use=False`（其他 5.4 变体为 True）
- `gpt-4o-audio-preview` 的 `supports_audio=True`（其他 4o 变体为 False）

**数值格式**：大数字使用下划线分隔（`1_050_000` 而非 `1050000`）。

**来源注释**：每个 `{FAMILY}_MODELS` 列表上方必须标注采集来源 URL。

### 3.5 数据排序约定

文件内按 Family → Version（降序，最新在前） → Variant（按 priority 升序）排列。

### 3.6 新增 Provider 检查清单

- [ ] 创建 `tests/e2e/test_{provider}.py`，遵循文件模板
- [ ] 模块 docstring 标注官方文档 URL 和采集日期
- [ ] 每个 Family 数据列表上方标注具体来源 URL
- [ ] 所有条目包含 8 个必须字段
- [ ] 区分性字段已显式写入
- [ ] `pytest tests/e2e/test_{provider}.py -v` 全部通过

---

## 第四步：运行测试

```bash
# 运行单个 Provider 的 E2E 测试
uv run python -m pytest tests/e2e/test_openai.py -v

# 运行全部 E2E 测试
uv run python -m pytest tests/e2e/ -v

# 完整 QA 确保无回归
uv run poe qa
```

所有测试必须通过。

---

## 快速参考

### 采集工具决策树

```
需要特定模型的某个字段值？
  → WebSearch（最快，适合点查）

需要某 Provider 全部模型的完整信息？
  → 该 Provider 文档是否为静态渲染？
      是 → WebFetch（Anthropic、Google）
      否 → Playwright（OpenAI、智谱）
```

### 文件清单

| 文件 | 角色 |
|------|------|
| `tests/e2e/conftest.py` | 共享断言逻辑（修改断言规则只改这里） |
| `tests/e2e/test_{provider}.py` | 各 Provider 的 E2E 测试数据 + 参数化 |
| `${CLAUDE_SKILL_DIR}/../update-provider-model/providers/*.md` | 各 Provider 采集指南 |
| `whosellm/models/families/**/*.py` | 被测代码（发现不一致时修复） |

### 批量采集效率建议

当需要覆盖一个 Provider 的所有最新版本模型时：

1. **一次性采集**：用 Playwright/WebFetch 获取模型列表页的完整能力矩阵
2. **批量比对**：用脚本一次性输出所有模型的 LLMeta 元数据
3. **差异报告**：只对有差异的模型展开详细排查（使用 AskUserQuestion 逐条确认）
4. **批量写入**：确认无误后一次性写入对应的 `test_{provider}.py`

```bash
# 批量输出某 Provider 最新版本模型的 LLMeta 元数据
uv run python -c "
from whosellm import LLMeta
from whosellm.models.registry import _FAMILY_CONFIGS
from whosellm.provider import Provider

target = Provider.OPENAI  # 替换为目标 Provider

# 按 family 取最新版本的 specific_models
family_latest: dict[str, tuple[str, list[str]]] = {}
for (family, provider), config in _FAMILY_CONFIGS.items():
    if provider != target:
        continue
    fkey = family.value
    ver = config.version_default
    if fkey not in family_latest or ver > family_latest[fkey][0]:
        family_latest[fkey] = (ver, sorted(config.specific_models.keys()))

for fkey, (ver, models) in sorted(family_latest.items()):
    for name in models:
        m = LLMeta(name)
        c = m.capabilities
        print(f'{name}|{m.version}|{m.variant}|thinking={c.supports_thinking}|vision={c.supports_vision}|ctx={c.context_window}|max={c.max_tokens}')
"
```
