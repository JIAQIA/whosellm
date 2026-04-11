# ModelFamily 重新设计规范

> 状态：Draft | 日期：2026-04-11 | 作者：JQQ + Claude

## 1. 背景与问题

当前 `ModelFamily` 的语义不清晰，导致两个矛盾：

1. **拆分矛盾**：GPT-5.x 被拆为独立 Family（GPT_5、GPT_5_1、GPT_5_2、GPT_5_4），但 Claude 4.5/4.6 和 Gemini 2.5/3.0 却保持在单一 Family 中。标准不一致。
2. **比较失效**：拆分后 `LLMeta("gpt-5") < LLMeta("gpt-5.4")` 抛出 `ValueError`（跨 Family 不可比），但这个比较在业务上完全合理。

根本原因：**Family 同时承担了「代码组织」和「比较边界」两个职责**，而这两个职责的粒度需求不同。

## 2. 核心设计决策

### 2.1 Family = 产品线（Lineage）

**Family 的唯一语义是「产品线」，也是版本比较的边界。**

识别规则：**从命名风格推断产品线**，不依赖供应商的营销定位。

| 命名模式 | 产品线 | Family 名称 |
|---------|--------|-----------|
| `gpt-{version}` / `gpt-{version}-{variant}` | GPT 系列 | `GPT` |
| `gpt-4o` / `gpt-4o-{variant}` | GPT-4o 系列 | `GPT_4O` |
| `o{version}` / `o{version}-{variant}` | O 系列 | `O` |
| `claude-{variant}-{major}-{minor}` | Claude 系列 | `CLAUDE` |
| `gemini-{major}.{minor}-{variant}` | Gemini 系列 | `GEMINI` |
| `glm-{version}` / `glm-{version}v` | GLM 系列 | `GLM` |
| `cogview-{version}` | CogView 系列 | `COGVIEW` |
| `cogvideox-{version}` | CogVideoX 系列 | `COGVIDEOX` |

### 2.2 比较语义

| 场景 | 是否可比较 | 示例 |
|------|----------|------|
| 同 Family 同 version | YES | `gpt-5-mini < gpt-5-pro` |
| 同 Family 跨 version | YES | `gpt-4.1 < gpt-5.4` |
| 跨 Family 同 Provider | **NO** | `o3` vs `gpt-5` → ValueError |
| 跨 Provider | **NO** | `claude-sonnet-4-6` vs `gpt-5.4` → ValueError |

排序维度（优先级从高到低）：

1. **Version**：`(major, minor)` 元组，如 `(5, 4) > (5, 0) > (4, 1)`
2. **Variant Priority**：同 version 内，`nano(0) < mini(0) < base(1) < pro(4) < opus(5)`
3. **Release Date**：同 version 同 variant 时，按发布日期排序

### 2.3 Version 语义

Version 表示**产品线内的迭代代次**，是一个可解析的数字元组。

| 模型名 | version | 解析 |
|--------|---------|------|
| `gpt-3.5-turbo` | `"3.5"` | `(3, 5)` |
| `gpt-4` | `"4.0"` | `(4, 0)` |
| `gpt-4.1` | `"4.1"` | `(4, 1)` |
| `gpt-5` | `"5.0"` | `(5, 0)` |
| `gpt-5.4-mini` | `"5.4"` | `(5, 4)` |
| `claude-sonnet-4-6` | `"4.6"` | `(4, 6)` |
| `o3` | `"3.0"` | `(3, 0)` |
| `glm-4.6v` | `"4.6"` | `(4, 6)` |

### 2.4 Variant 语义

Variant 表示**同一 version 内的模型规格**，主要含义是尺寸/成本等级。

**两类 Variant：**

| 类型 | 示例 | 特点 |
|------|------|------|
| **尺寸等级** | nano, mini, base, flash, sonnet, pro, opus | 有线性排序关系，用 `variant_priority` 表示 |
| **功能特化** | codex, audio-preview, search-preview, deep-research, realtime-preview | 无线性排序关系，仍用 variant 字段存储 |

两类 Variant 共存于同一字段，通过 `variant_priority` 区分排序行为。功能特化变体可以有自己的 priority 值，但跨类型比较的语义由用户自行判断。

**标准 Priority 约定：**

```
nano=0, mini=0, flash=0, base=1, air=1, flashx=2,
sonnet=3, turbo=3, plus/pro=4, opus/ultra=5, omni=6
```

### 2.5 Provider 语义

Provider 不变——纯粹标识模型的供应商/来源（OpenAI、Anthropic、Google、Zhipu 等）。不参与比较逻辑。

## 3. Family 合并计划

### 3.1 OpenAI（8+ → 3）

| 当前 Family | 合并到 | 说明 |
|------------|--------|------|
| GPT_3_5 | **GPT** | version="3.5" |
| GPT_4 | **GPT** | version="4.0" |
| GPT_4_1 | **GPT** | version="4.1" |
| GPT_5 | **GPT** | version="5.0" |
| GPT_5_1 | **GPT** | version="5.1" |
| GPT_5_2 | **GPT** | version="5.2" |
| GPT_5_3 | **GPT** | version="5.3" |
| GPT_5_4 | **GPT** | version="5.4" |
| GPT_4O | **GPT_4O** | 独立命名模式，不合并 |
| O1 | **O** | version="1.0" |
| O3 | **O** | version="3.0" |
| O4 | **O** | version="4.0" |

### 3.2 Anthropic（不变）

| 当前 Family | 合并到 | 说明 |
|------------|--------|------|
| CLAUDE | **CLAUDE** | 保持不变 |

### 3.3 Google（不变）

| 当前 Family | 合并到 | 说明 |
|------------|--------|------|
| GEMINI | **GEMINI** | 保持不变 |

### 3.4 智谱（3 → 2 + 2）

| 当前 Family | 合并到 | 说明 |
|------------|--------|------|
| GLM_3 | **GLM** | version="3.0"，通过 Registry Merge 合并 |
| GLM_TEXT | **GLM** | version="4.0"~"5.0"，文本产品线 |
| GLM_VISION | **GLM_VISION** | 保持独立。命名模式 `glm-{version}v` 中 `v` 后缀是产品线标识（类似 GPT_4O 的 `o`），不是 variant |
| COGVIEW_4 | **COGVIEW** | 独立产品线，不合并 |
| COGVIDEOX_3 | **COGVIDEOX** | 独立产品线（可合并 2 和 3） |
| COGVIDEOX_2 | **COGVIDEOX** | 同上 |

### 3.5 其他 Provider

按相同原则处理：从命名风格识别产品线，同一产品线合并为一个 Family。

## 4. 架构变更：Registry Merge 模式

### 4.1 核心思路

允许多个 `ModelFamilyConfig` 声明相同的 `family`，注册时自动合并。

```
文件 A: ModelFamilyConfig(family=GPT, patterns=[...], specific_models={gpt-3.5: ...})
文件 B: ModelFamilyConfig(family=GPT, patterns=[...], specific_models={gpt-5.4: ...})
                          ↓ 注册时合并
_FAMILY_CONFIGS[GPT] = 合并后的 Config (patterns=A+B, specific_models=A∪B)
```

### 4.2 合并规则

| 字段 | 规则 |
|------|------|
| `family` | 相同，作为合并 key |
| `provider` | 必须一致，否则报错 |
| `version_default` | 取最后注册的值（最新版本的 Config 最后导入） |
| `variant_default` | 同上 |
| `variant_priority_default` | 同上 |
| `patterns` | **追加**，新 patterns 添加到列表前面（更具体的在前） |
| `capabilities` | 取最后注册的值（作为 family 级 fallback） |
| `specific_models` | **合并**字典，key 冲突时后注册的覆盖 |

### 4.3 文件组织

大 Family 使用子目录，每个子文件是一个独立的 `ModelFamilyConfig`：

```
whosellm/models/families/
├── openai/
│   ├── __init__.py          # 按版本顺序导入，触发注册
│   ├── gpt_3_5.py           # ModelFamilyConfig(family=GPT, ...)
│   ├── gpt_4.py             # ModelFamilyConfig(family=GPT, ...)
│   ├── gpt_4_1.py           # ModelFamilyConfig(family=GPT, ...)
│   ├── gpt_5.py             # ModelFamilyConfig(family=GPT, ...)
│   ├── gpt_5_4.py           # ModelFamilyConfig(family=GPT, ...)  ← 最后导入，其 defaults 生效
│   ├── gpt_4o.py            # ModelFamilyConfig(family=GPT_4O, ...)
│   ├── o1.py                # ModelFamilyConfig(family=O, ...)
│   ├── o3.py                # ModelFamilyConfig(family=O, ...)
│   └── o4.py                # ModelFamilyConfig(family=O, ...)
├── anthropic.py             # CLAUDE（单文件足够）
├── gemini.py                # GEMINI（单文件足够）
└── zhipu/
    ├── __init__.py
    ├── glm_3.py             # ModelFamilyConfig(family=GLM, ...)
    ├── glm_4.py             # ModelFamilyConfig(family=GLM, ...)
    ├── glm_4_5.py           # ModelFamilyConfig(family=GLM, ...)
    └── ...
```

### 4.4 需要修改的核心代码

1. **`models/config.py`** — `ModelFamilyConfig.__post_init__`：检测 family 是否已注册，是则合并
2. **`models/registry.py`** — `register_family_config()`：实现合并逻辑
3. **`models/base.py`** — `ModelFamily` 枚举：减少成员（GPT_3_5/GPT_4/... → GPT）
4. **`model_version.py`** — `__lt__` / `__eq__`：无需改动（Family 合并后自然可比）

## 5. 不在此次范围内

- 新增 Provider 或模型（先完成架构重构）
- 修改 `ModelCapabilities` 字段
- 修改 `variant_priority` 约定
- 跨 Family / 跨 Provider 的比较支持

## 6. 验证标准

重构完成后，以下断言必须全部通过：

```python
# 同 Family 跨 version 比较
assert LLMeta("gpt-3.5-turbo") < LLMeta("gpt-4")
assert LLMeta("gpt-4") < LLMeta("gpt-4.1")
assert LLMeta("gpt-4.1") < LLMeta("gpt-5")
assert LLMeta("gpt-5") < LLMeta("gpt-5.4")

# 同 version 内 variant 排序
assert LLMeta("gpt-5-mini") < LLMeta("gpt-5")
assert LLMeta("gpt-5") < LLMeta("gpt-5-pro")

# version 优先于 variant
assert LLMeta("gpt-4.1-pro") < LLMeta("gpt-5-mini")

# 跨 Family 比较应报错
with pytest.raises(ValueError):
    LLMeta("o3") < LLMeta("gpt-5")

with pytest.raises(ValueError):
    LLMeta("gpt-4o") < LLMeta("gpt-5")

# O 系列内可比
assert LLMeta("o1") < LLMeta("o3")
assert LLMeta("o3") < LLMeta("o4-mini")

# Family 正确归属
assert LLMeta("gpt-3.5-turbo").family == ModelFamily.GPT
assert LLMeta("gpt-5.4-mini").family == ModelFamily.GPT
assert LLMeta("gpt-4o").family == ModelFamily.GPT_4O
assert LLMeta("o3").family == ModelFamily.O
assert LLMeta("glm-4.6v").family == ModelFamily.GLM
assert LLMeta("glm-4.6").family == ModelFamily.GLM
```
