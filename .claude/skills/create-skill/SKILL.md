---
name: create-skill
description: 创建符合项目规范的新 Claude Skill。当用户需要新增技能、为 Claude Code 添加自动化工作流时使用。
user-invocable: true
argument-hint: <skill-name> [description]
allowed-tools: Read, Write, Glob, Bash
---

# Create Skill — 创建新技能

根据用户描述创建符合本项目规范的 Claude Skill。

输入：$ARGUMENTS

---

## 核心原则

1. **代码胜于文档** — SKILL.md 中能引用现有文件的，直接用 Markdown 链接，不要摘录代码
2. **讲清为何，示例为何** — 先阐述模式与概念，再引用示例文件说明具体操作
3. **无实践不成技** — 如果项目中尚无该技能涉及的实际案例或代码，说明它未经验证，拒绝创建
4. **分步即模式** — SKILL 主体是分步执行流程，模式与最佳实践自然渗透在步骤中，而非堆砌独立章节

---

## 第一步：需求理解与可行性验证

### 1.1 解析用户意图

从 `$ARGUMENTS` 中提取：
- **技能名称**：小写字母 + 连字符（如 `update-provider-model`）
- **功能描述**：这个技能解决什么问题，什么场景触发

### 1.2 验证项目中有无实践基础

在项目中查找该技能涉及的实际文件、代码模式或已有工作流：

```bash
# 查找相关代码或文档
# 如果找不到任何相关实践，说明该技能尚未经项目验证
```

**关键判断**：如果项目中没有该技能所需的代码示例或实际操作案例，则**拒绝创建**，并向用户说明原因——未经实践验证的技能只会产生空洞的文档。

### 1.3 检查是否与现有技能重叠

现有技能清单：

```bash
ls .claude/skills/*/SKILL.md
```

如果新技能与已有技能功能重叠，建议扩展现有技能而非新建。

---

## 第二步：确定技能结构

### 2.1 选择参考模板

根据技能类型选择最接近的现有技能作为参考：

| 技能类型 | 参考 | 特点 |
|---------|------|------|
| 外部信息采集 + 代码变更 | [update-provider-model]({baseDir}/../update-provider-model/SKILL.md) | 多步骤、有子资源目录、委托 Agent |
| 配置校验 + 可选修复 | [review-provider-model]({baseDir}/../review-provider-model/SKILL.md) | 比对报告、分级处理 |
| 需求分析 + 方案评审 + 执行 | [evolve]({baseDir}/../evolve/SKILL.md) | 核心原则前置、必须用户确认 |
| CI/CD 操作流 | [release]({baseDir}/../release/SKILL.md) | 参数驱动、前置检查链、状态监控 |

### 2.2 确定目录布局

```
.claude/skills/{skill-name}/
├── SKILL.md              # 必需：技能入口
├── {resource}.md          # 可选：辅助资源（如 testing.md）
└── {subdir}/              # 可选：按类别组织的子资源（如 providers/）
```

子资源仅在技能确实需要外部参考材料时创建，不要预设空目录。

---

## 第三步：编写 SKILL.md

### 3.1 Frontmatter

```yaml
---
name: {skill-name}                    # 小写 + 连字符，不超过 64 字符
description: {中文描述，说明功能和触发场景}  # 不超过 1024 字符
user-invocable: true
argument-hint: {参数格式提示}
allowed-tools: {技能需要的工具列表}
---
```

**description 要点**：
- 使用中文（与本项目交互语言一致）
- 说清两件事：(1) 做什么 (2) 什么时候用
- 参考现有技能的 description 风格

### 3.2 正文结构

遵循本项目已有技能的统一风格——**分步编号工作流**：

```markdown
# 技能标题

一句话概括技能职责。

输入：$ARGUMENTS

---

## 核心原则（可选，仅当技能有重要的决策边界时）

## 第一步：{动作}
### 1.1 {子步骤}
### 1.2 {子步骤}

## 第二步：{动作}
...

## 快速参考（可选）
```

### 3.3 编写要领

**每一步应包含**：
1. 这一步的目标（做什么、为什么）
2. 具体操作（引用项目文件，或给出命令模板）
3. 输出判断（成功 / 失败的标准，下一步的分支条件）

**引用而非摘录**：

```markdown
# 好 — 链接到实际文件
详细的测试指南见 [testing.md](testing.md)。

# 坏 — 在 SKILL 中复制代码
\```python
# 从 testing.md 复制的 50 行测试代码...
\```
```

**在步骤中自然体现模式**：

```markdown
## 第四步：验证

运行全量 QA 确保无回归：

\```bash
uv run poe qa
\```

所有检查必须通过。如有失败，修复后重新运行。
```

而不是单独设置一个"最佳实践"章节罗列"应该跑 QA"。

---

## 第四步：创建文件

### 4.1 写入 SKILL.md

使用 Write 工具创建 `.claude/skills/{skill-name}/SKILL.md`。

### 4.2 创建子资源（如需要）

仅当技能确实需要辅助材料时才创建。

### 4.3 验证清单

创建完成后逐项检查：

- [ ] SKILL.md 位于 `.claude/skills/{skill-name}/` 目录
- [ ] Frontmatter 包含 name、description、user-invocable、argument-hint、allowed-tools
- [ ] name 使用小写字母和连字符
- [ ] description 使用中文，说清功能和触发场景
- [ ] 正文是分步编号工作流，与现有技能风格一致
- [ ] 引用了项目中实际存在的文件，而非摘录代码
- [ ] 没有空洞的"最佳实践"堆砌，模式融入步骤中

---

## 命名规范

```
update-provider-model    # 动词-名词，清晰的功能描述
review-provider-model    # 同上
create-skill             # 同上
release                  # 单词足够清晰时可省略

# 避免
SkillCreator             # 不要大写
skill_creator            # 不要下划线
my-awesome-skill         # 不要修饰词
```

---

## 常见错误

| 错误 | 原因 | 修正 |
|------|------|------|
| SKILL 内容空洞，全是抽象原则 | 没有结合项目实际操作 | 每一步引用具体文件和命令 |
| 大段代码摘录 | 复制了源文件内容 | 改为 Markdown 链接到源文件 |
| 与现有技能功能重叠 | 没有先检查已有技能 | 扩展现有技能，不要新建 |
| 创建了项目中无实践基础的技能 | 跳过了可行性验证 | 先有实践，再提炼技能 |
