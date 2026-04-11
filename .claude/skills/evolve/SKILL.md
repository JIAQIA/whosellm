---
name: evolve
description: 根据 GitHub Issue 或文字描述分析需求，评估对现有架构的影响，制定并执行变更方案
user-invocable: true
argument-hint: <github-issue-url | description>
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent, WebSearch, WebFetch
effort: high
---

# Evolve — 项目演进工作流

根据用户输入（GitHub Issue 链接或文字描述）分析需求，评估架构影响，制定变更方案并执行。

输入：$ARGUMENTS

---

## 核心原则

在整个工作流中，始终遵守以下原则：

1. **一切从实际出发** — 所有变更必须有真实的用户需求或市面现状作为依据，拒绝虚构需求与过度设计
2. **平衡三角** — 在性能、易用性、易维护性之间寻求最优平衡，不为某一维度牺牲其他两���
3. **不排斥重构，但需充分论证** — 重构需要具体的痛点和收益分析，而非"看起来更好"
4. **宽容设计** — 继承项目现有风格：未知模型返回 UNKNOWN 而非抛异常，新功能不应破坏已有行为

---

## 第一步：需求采集与理解

### 1.1 解析输入

根据输入类型执行不同的采集路径：

**GitHub Issue 链接**（匹配 `https://github.com/.*/issues/\d+`）：

```bash
# 获取 Issue 详情
gh issue view {issue_url} --json title,body,labels,comments,author
```

提取关键信息：
- Issue 标题与描述
- 标签分类（bug / feature / enhancement / question）
- 评论中的补充说明与讨论结论
- 提出者身份（外部用户 vs 维护者）

**文字描述**：

直接解析用户描述，识别其中的：
- 具体模型名称 / Provider 名称
- 期望的能力字段或行为
- 遇到的问题现象（如果是 bug）
- 期望的最终效果

### 1.2 需求分类

将需求归入以下类别之一：

| 类别 | 标识 | 示例 |
|------|------|------|
| **BUG** | 现有功能行为不符预期 | "LLMeta('xxx') 返回的 supports_vision 应该是 True" |
| **NEW_CAPABILITY** | 需要新增能力字段 | "希望知道模型是否支持 code_interpreter" |
| **NEW_PROVIDER** | 需要新增供应商 | "希望支持 Mistral 的模型" |
| **NEW_MODEL** | 已有 Provider 下新增模型 | "gpt-4o-audio 还没有收录" |
| **ARCHITECTURE** | 现有架构不满足组织需求 | "Provider::Model 两级不够用" |
| **ENHANCEMENT** | 改进现有功能 | "比较逻辑需要支持跨版本" |

---

## 第二步：现状评估

### 2.1 定位相关代码

根据需求类别，读取并理解相关文件：

```
whosellm/capabilities.py          — 能力字段定义
whosellm/model_version.py         — LLMeta 主入口
whosellm/provider.py              — Provider 枚举
whosellm/models/base.py           — ModelFamily 枚举
whosellm/models/config.py         — ModelFamilyConfig / SpecificModelConfig
whosellm/models/registry.py       — 注册表与模式匹配
whosellm/models/families/         — 各供应商配置
```

### 2.2 影响面分析

评估变更涉及的文件范围和影响面，输出影响矩阵：

```markdown
### 影响面分析

| 文件 | 变更类型 | 风险等级 | 说明 |
|------|---------|---------|------|
| capabilities.py | 新增字段 | 低 | 新增布尔字段，有默认值 |
| models/families/xxx.py | 修改配置 | 低 | 仅修改数据配置 |
| models/config.py | 修改逻辑 | 中 | 影响注册流程 |
| model_version.py | 修改核心逻辑 | 高 | 影响所有模型初始化 |
```

### 2.3 架构适配性判断

**关键判断点**：当前架构是否能满足此需求？

- **可以满足**：直接进入第三步制定方案
- **需要扩展**：评估最小化扩展方案（如新增字段、新增枚举值）
- **需要重构**：进入架构决策流程（见下方）

#### 架构决策流程（仅当需要重构时）

必须同时满足以下条件才可提议重构：

1. **有 2 个以上具体场景**证明当前架构无法支持（不是假设场景）
2. **重构收益明确可量化**（如：减少 N 个文件的重复代码、支持 M 个新 Provider 的接入模式）
3. **迁移路径清晰**：旧 API 到新 API 的迁移方式明确，不破坏已发布的公共接口

如果不满足，应选择**最小化扩展**方案。

---

## 第三步：方案设计

### 3.1 制定变更方案

输出结构化的变更方案，**必须在执行前向用户展示并获得确认**：

```markdown
## 变更方案

### 需求摘要
{一句话概括}

### 需求类别
{BUG / NEW_CAPABILITY / NEW_PROVIDER / NEW_MODEL / ARCHITECTURE / ENHANCEMENT}

### 变更清单

| 序号 | 文件 | 变更内容 | 必要性 |
|------|------|---------|--------|
| 1 | ... | ... | 必须 / 建议 |

### 不做的事情
{明确列出本次变更范围之外的内容，避免范围蔓延}

### 兼容性
{对现有 API / 行为的影响说明}

### 验证计划
{如何确认变更正确}
```

### 3.2 等待用户确认

**必须等待用户明确确认后才可进入执行阶段。** 如果用户有修改意见，回到 3.1 调整方案。

---

## 第四步：执行变更

### 按需求类别执行

#### BUG 修复

1. 先编写或修改测试用例，复现 bug
2. 修改代码修复问题
3. 运���测试验证修复：`uv run python -m pytest {test_file} -v`
4. 运行完整检查：`uv run poe qa`

#### NEW_CAPABILITY（新增能力字段）

1. 在 `whosellm/capabilities.py` 的 `ModelCapabilities` 中新增字段（必须有合理默认值）
2. 在相关供应商配置中为已知支持的模型设置该字段
3. 补充测试用例
4. 运行 `uv run poe qa`

#### NEW_PROVIDER / NEW_MODEL

**委托给已有技能**：

- 新增供应商或模型 → 使用 `/update-provider-model` 技能
- 校验现有配置 → 使用 `/review-provider-model` ���能

告知用户应使用的技能和参数，或在用户同意后直接调用。

#### ARCHITECTURE（架构变更）

1. 先创建设计文档草案，记录到 `docs/` 目录
2. 列出所有受影响的公共 API
3. 实现变更，保持向后兼容（至少一个版本的过渡期）
4. 迁移所有内部使用
5. 全量测试：`uv run poe qa`

#### ENHANCEMENT（功能增强）

1. 理解现有实现
2. 最小化修改，只改必须改的
3. 补充对应测试
4. `uv run poe qa`

---

## 第五步：验证与收尾

### 5.1 质量检查

```bash
uv run poe qa
```

所有检查必须通过。如有失败，修复后重新运行。

### 5.2 快速功能验证

```python
uv run python -c "
from whosellm import LLMeta
# 根据需求编写验证代码
m = LLMeta('{model_name}')
print(f'{field}: {getattr(m.capabilities, field)}')
"
```

### 5.3 输出变更报告

向用户展示最终结果：

```markdown
## 变更完成

### 修改文件
- `path/to/file.py` — {变更说明}

### 验证结果
- poe qa: 通过
- 功能验证: {结果}

### 后续建议
- {是否需要发版}
- {是否需要更新文档}
- {是否有关联的 Issue 需要关闭}
```

### 5.4 Issue 关联（如果输入是 GitHub Issue）

提示用户是否需要：
- 在 Issue 中评论变更结果
- 关闭 Issue

**不自动执行**，等待用户指示。

---

## 快速参考

### 需求类别 → 推荐路径

| 类别 | 推荐路径 |
|------|---------|
| BUG | 直接修复，测试先行 |
| NEW_CAPABILITY | 修改 capabilities.py + 供应商配置 |
| NEW_PROVIDER / NEW_MODEL | 委托 `/update-provider-model` |
| ARCHITECTURE | 设计文档先行，经确认后实施 |
| ENHANCEMENT | 最小化修改，不扩大范围 |

### 决策边界

| 场景 | 做 | 不做 |
|------|------|------|
| 用户要求的具体功能 | 实现它 | 顺带"改进"周边代码 |
| 明确的 bug | 修复它 | 重构整个模块 |
| 新增一个字段 | 加字段 + 设默认值 | 改造整个 capabilities 体系 |
| 需要新的组织层级 | 评估最小方案 | 一步到位设计"终极架构" |
