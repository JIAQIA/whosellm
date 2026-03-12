---
name: review-provider-model
description: 校验指定 Provider 或模型家族的配置是否与官方文档一致，输出差异报告并可选自动修复
user-invocable: true
argument-hint: [provider|family] [--fix]
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# Review Provider-Model 配置校验

对指定 Provider 或模型家族的现有配置进行二次校验，确保与官方文档保持一致。

校验目标：$ARGUMENTS

---

## 工作流概览

```
确定校验范围 → 读取现有配置 → 采集官方信息 → 逐项比对 → 输出差异报告 → 可选修复
```

---

## 第一步：确定校验范围

根据用户输入确定要校验的配置文件：

| 用户输入 | 校验范围 |
|---------|---------|
| Provider 名称（如 `openai`） | 该 Provider 下所有模型家族配置 |
| 模型家族名称（如 `gemini`） | 该家族的 `ModelFamilyConfig` 及其所有 `specific_models` |
| 具体模型名（如 `gemini-2.5-flash-lite`） | 仅校验该模型的 `SpecificModelConfig` |

### 定位配置文件

```bash
# 查找配置文件
whosellm/models/families/{provider}.py          # 单文件供应商
whosellm/models/families/{provider}/            # 多文件供应商（如 openai/）
```

---

## 第二步：读取现有配置

### 2.1 提取配置快照

读取目标配置文件，对每个 `ModelFamilyConfig` 和其 `specific_models` 提取以下信息：

- **家族级配置**：`family`、`provider`、`version_default`、`variant_default`、`patterns`、`capabilities`
- **特定模型配置**：每个 `specific_models` 条目的 `version`、`variant`、`variant_priority`、`capabilities`、`patterns`

### 2.2 生成配置摘要表

将现有配置整理为表格，方便后续比对：

```
| 模型 ID | thinking | vision | audio | video | pdf | function_calling | streaming | structured_outputs | json_outputs | web_search | max_tokens | context_window |
```

---

## 第三步：采集官方信息

### 推荐工具：Playwright MCP

与 `update-provider-model` 技能相同，**优先使用 Playwright MCP 浏览器工具**。

#### 操作流程

1. **查阅 `${CLAUDE_SKILL_DIR}/providers/` 目录下对应供应商的指引文件**，获取官方文档 URL。
2. **使用 `mcp__plugin_playwright_playwright__browser_navigate`** 打开供应商的模型文档页面。
3. **使用 `mcp__plugin_playwright_playwright__browser_snapshot`** 获取页面内容。
4. **使用 `mcp__plugin_playwright_playwright__browser_click`** 展开详情（如需要）。
5. 如页面无法渲染，回退使用 **WebSearch + WebFetch** 补充。

#### 重点采集的校验项

| 优先级 | 校验项 | 影响 |
|--------|--------|------|
| **P0** | `supports_thinking` | 直接影响 thinking_budget 校验逻辑 |
| **P0** | `supports_vision` / `supports_audio` / `supports_video` | 影响多模态输入路由 |
| **P0** | `context_window` / `max_tokens` | 影响 token 截断策略 |
| **P1** | `supports_function_calling` | 影响工具调用可用性 |
| **P1** | `supports_structured_outputs` / `supports_json_outputs` | 影响输出格式选择 |
| **P1** | `supports_streaming` | 影响流式响应路由 |
| **P2** | `supports_web_search` / `supports_code_interpreter` 等工具能力 | 影响扩展工具可用性 |
| **P2** | `supports_image_generation` / `supports_audio_generation` | 影响生成能力判断 |
| **P3** | `supports_fine_tuning` / `supports_distillation` | 影响训练相关功能 |

---

## 第四步：逐项比对并输出报告

### 4.1 比对规则

对每个模型 ID，将**代码中的配置值**与**官方文档值**进行比对：

- **布尔能力字段**：必须精确匹配（`True`/`False`）
- **数值字段**（`max_tokens`、`context_window`）：允许官方文档更新导致的增大，但缩小需标记
- **模式匹配**：验证 `patterns` 是否覆盖官方文档中列出的所有模型 ID 变体
- **新增模型**：检查官方文档中是否有新模型 ID 尚未在 `specific_models` 中注册

### 4.2 差异报告格式

输出结构化的差异报告：

```markdown
## 校验报告：{provider} / {family}

### 校验时间：{date}
### 官方文档来源：{url}

---

### ✅ 通过（{n} 项）

| 模型 ID | 校验项 | 配置值 | 官方值 |
|---------|--------|--------|--------|
| gemini-2.5-flash | supports_thinking | True | True |

### ❌ 不一致（{n} 项）

| 模型 ID | 校验项 | 当前配置值 | 官方文档值 | 优先级 | 建议 |
|---------|--------|-----------|-----------|--------|------|
| gemini-2.5-flash-lite | supports_thinking | False | True | P0 | 修改为 True |

### ⚠️ 待确认（{n} 项）

| 模型 ID | 问题描述 |
|---------|---------|
| xxx-preview | 官方文档未明确说明该能力，需人工确认 |

### 🆕 新增模型（{n} 项）

| 模型 ID | 说明 |
|---------|------|
| xxx-new-variant | 官方已发布但配置中未注册 |
```

---

## 第五步：修复（可选）

仅当用户传入 `--fix` 参数或明确要求修复时执行。

### 5.1 自动修复范围

- **仅修复 P0 和 P1 级别的布尔能力不一致**
- **数值字段更新**（`max_tokens`、`context_window` 增大）
- **不自动新增模型** — 新增模型应使用 `update-provider-model` 技能

### 5.2 修复流程

1. 使用 `Edit` 工具修改配置文件中的不一致字段
2. 运行 `uv run poe check` 确保代码检查通过
3. 运行相关测试确认无回归：
   ```bash
   uv run python -m pytest tests/models/families/test_{family}.py -v
   ```
4. 如果测试中有断言与修复冲突，同步更新测试代码

### 5.3 修复后验证

```bash
# 快速验证修复是否生效
uv run python -c "
from whosellm import LLMeta
m = LLMeta('{model_id}')
print(f'{field}: {getattr(m.capabilities, field)}')
"
```

---

## 快速参考

### 校验文件清单

| 文件 | 用途 |
|------|------|
| `whosellm/models/families/{provider}.py` | 模型配置源码 |
| `tests/models/families/test_{family}.py` | 对应测试（修复时需同步更新） |
| `${CLAUDE_SKILL_DIR}/providers/{provider}.md` | 供应商文档采集指南 |

### 常见错误模式

| 错误类型 | 示例 | 原因 |
|---------|------|------|
| 能力遗漏 | `supports_thinking=False` 但实际支持 | 模型发布时不支持，后续更新添加了该能力 |
| 数值过时 | `max_tokens=8192` 但官方已提升到 `65536` | 官方静默升级未同步 |
| 新变体未注册 | 官方新增 `-lite` 变体但无 `specific_models` 条目 | 需用 `update-provider-model` 新增 |
| 继承错误 | 子模型缺少独立能力配置，错误继承了家族默认值 | 应添加 `SpecificModelConfig` 覆盖 |
