---
name: code-review
description: 对代码变更进行全面 Review，覆盖设计规范、测试完备性、DRY 原则和封装合理性。当用户提交变更或请求代码审查时使用。
user-invocable: true
argument-hint: [file|branch|PR-url|--staged]
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Code Review — 全面代码审查

对代码变更进行系统性审查，输出结构化的审查报告。

输入：$ARGUMENTS

---

## 核心原则

1. **以项目规范为准绳** — 审查标准来自 [CLAUDE.md](../../../CLAUDE.md) 和项目现有代码模式，不套用外部通用规范
2. **指出问题而非重写** — 报告中说明"什么有问题、为什么、建议如何改"，不直接输出大段替换代码
3. **区分严重等级** — 阻塞发布的问题 vs 建议改进，不混为一谈

---

## 第一步：确定审查范围

### 1.1 解析输入

根据输入类型获取变更内容：

| 输入类型 | 操作 |
|---------|------|
| `--staged` 或无参数 | `git diff --cached` 获取暂存区变更；若为空则 `git diff` 获取工作区变更 |
| 文件路径 | 直接读取指定文件，结合 `git diff` 查看该文件的变更 |
| 分支名 | `git diff main...{branch}` 获取分支全部变更 |
| PR URL | `gh pr diff {number}` 获取 PR 完整变更 |

### 1.2 生成变更清单

列出所有变更文件，标注变更类型：

```
| 文件 | 变更类型 | 影响范围 |
|------|---------|---------|
| whosellm/models/families/xxx.py | 新增 | 模型配置 |
| tests/models/families/test_xxx.py | 新增 | 测试 |
| whosellm/models/registry.py | 修改 | 核心逻辑 |
```

---

## 第二步：设计规范审查

逐项检查变更是否符合项目设计规范。

### 2.1 核心概念一致性

对照 [CLAUDE.md](../../../CLAUDE.md) 中定义的 Family / Provider / Version / Variant 四个核心概念：

- **Family 划分**：新模型的 Family 归属是否正确？判断依据是命名模式，不是供应商营销定位
- **版本解析**：version 是否正确解析为 `(major, minor)` 元组？
- **变体分类**：variant 属于尺寸等级还是功能特化？`variant_priority` 是否合理？
- **比较边界**：同 Family 内可比较，跨 Family 应抛出 `ValueError`

### 2.2 配置驱动模式

检查变更是否遵循配置驱动的设计模式：

- 新模型是否通过 `ModelFamilyConfig` / `SpecificModelConfig` 定义，而非在代码中添加 if-else 分支？
- `patterns` 列表是否按优先级排序（更具体的在前）？
- `specific_models` 的键是否为小写模型名？
- 子 `patterns` 是否为父 `patterns` 的子集？

### 2.3 注册表模式

- 新增配置是否通过 `ModelFamilyConfig.__post_init__` 自动注册？
- 是否需要利用 Registry Merge 机制（同一 `(family, provider)` 的多个配置自动合并）？
- 如果新增了 `ModelFamily` 或 `Provider` 枚举值，是否通过 `add_member()` 扩展？

### 2.4 宽容设计

- 对未知输入是否返回 `UNKNOWN` 而非抛出异常？
- 新功能是否向后兼容，不破坏已有的公共 API？

### 2.5 代码风格

- Ruff 规则：行长 120、双引号、Python 3.11 目标
- MyPy 严格模式：类型注解完备、无隐式 Optional
- 运行 `uv run poe check` 和 `uv run poe typecheck` 验证

---

## 第三步：测试覆盖审查

### 3.1 功能性测试

对照 `tests/` 目录中已有模式，检查新增代码是否有对应测试：

**模型配置变更**必须覆盖：
- 模式匹配测试 — `match_model_pattern("model-name")` 返回正确的 family / version / variant
- `LLMeta` 端到端测试 — `LLMeta("model-name")` 的字段值正确
- 带日期后缀的模式匹配 — `model-name-YYYY-MM-DD` 格式正确解析
- 变体优先级排序 — 同版本不同变体间的比较关系正确

**能力字段变更**必须覆盖：
- 每个 `supports_*` 布尔字段的断言
- `max_tokens` 和 `context_window` 数值断言
- 特定模型覆盖父级默认值的场景

**核心逻辑变更**必须覆盖：
- 正向测试（正常输入 → 正确输出）
- 边界测试（空字符串、极长名称、特殊字符等）
- 异常测试（跨 Family 比较 → `ValueError`）

### 3.2 业务数据验证

检查测试中的断言值是否与配置一致：

```python
# 好 — 测试值与配置中的实际值匹配
assert m.capabilities.context_window == 200000  # 与 anthropic.py 中的配置一致

# 坏 — 测试值与配置不符，测试通过只是因为使用了错误的值
assert m.capabilities.context_window == 128000  # 配置中实际是 200000
```

### 3.3 参数化测试

对于同一家族的多个模型/变体，检查是否使用了 `@pytest.mark.parametrize` 减少重复：

```python
# 好 — 参数化覆盖多个模型
@pytest.mark.parametrize("model_name,expected_version,expected_variant", [...])
def test_family_version_variant(model_name, expected_version, expected_variant): ...

# 坏 — 每个模型一个独立函数，逻辑完全重复
def test_model_a_version(): ...
def test_model_b_version(): ...
def test_model_c_version(): ...
```

### 3.4 测试命名与标记

- 测试文件位于 `tests/models/families/test_{family}.py`
- 测试函数命名清晰描述测试意图
- 适当使用 `@pytest.mark.unit` / `@pytest.mark.integration` 标记

---

## 第四步：DRY 原则与封装合理性审查

### 4.1 重复代码检测

在变更文件和相关文件中查找以下模式：

- **同一能力配置重复声明** — 多个 `SpecificModelConfig` 定义了完全相同的 `ModelCapabilities`，应提取为共享变量或利用家族默认值
- **同一测试逻辑重复** — 多个测试函数的断言列表完全相同，应使用参数化测试或提取辅助函数
- **同一模式匹配逻辑重复** — 应复用 `parse_pattern` 而非自行实现匹配

### 4.2 未使用已有封装

检查变更是否绕过了项目已有的封装：

| 应该使用 | 而非 |
|---------|------|
| `ModelFamilyConfig` + `SpecificModelConfig` | 直接操作 `MODEL_REGISTRY` |
| `match_model_pattern()` | 自行编写正则匹配 |
| `infer_variant_priority()` | 手动硬编码优先级元组 |
| `parse_pattern()` | 直接调用 `parse.parse()` |
| `Provider.add_member()` / `ModelFamily.add_member()` | 修改枚举类定义 |

### 4.3 "半重复"封装

检查是否存在以下情况：

- **功能相似但接口不同的函数** — 例如两个函数都在做"从模型名解析版本"但实现路径不同
- **部分提取的抽象** — 例如提取了一个辅助函数但只用了一半参数，另一半仍在调用处硬编码
- **跨文件的逻辑耦合** — 例如两个文件各自维护一份相似的映射表

发现后建议：统一到一处实现，或说明为何需要两套。

---

## 第五步：输出审查报告

按以下格式输出结构化报告：

```markdown
## Code Review 报告

### 审查范围
{变更文件列表}

### 阻塞项（必须修复）

| # | 文件:行号 | 类别 | 问题描述 | 建议 |
|---|----------|------|---------|------|
| 1 | xxx.py:42 | 设计规范 | ... | ... |

### 建议项（推荐改进）

| # | 文件:行号 | 类别 | 问题描述 | 建议 |
|---|----------|------|---------|------|
| 1 | xxx.py:88 | DRY | ... | ... |

### 通过项
- 设计规范：{通过的检查项}
- 测试覆盖：{通过的检查项}
- DRY / 封装：{通过的检查项}
```

### 类别标签

| 标签 | 含义 |
|------|------|
| 设计规范 | 不符合 CLAUDE.md 定义的核心概念或设计模式 |
| 测试缺失 | 缺少必要的测试用例 |
| 测试数据 | 测试断言值与配置不一致 |
| DRY | 存在可消除的重复 |
| 封装 | 未使用已有封装或存在半重复封装 |
| 风格 | 不符合 Ruff / MyPy 规则 |
| 兼容性 | 可能破坏现有 API 或行为 |

---

## 第六步：验证（可选）

如果审查发现了风格或类型问题，可运行自动化工具确认：

```bash
uv run poe check      # Ruff 检查
uv run poe typecheck  # MyPy 类型检查
uv run poe test       # 运行测试
```

如果变更涉及特定模型家族，运行针对性测试：

```bash
uv run python -m pytest tests/models/families/test_{family}.py -v
```
