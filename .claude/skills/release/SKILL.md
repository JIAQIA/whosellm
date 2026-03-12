---
name: release
description: 通过 GitHub Release 触发 CI 流水线发布包到 PyPI 或 TestPyPI
user-invocable: true
argument-hint: <pypi|testpypi> [version]
allowed-tools: Bash, Read, Glob
---

# Release 发布工作流

通过创建 GitHub Release 触发 CI 流水线，将包发布到指定目标。

参数：$ARGUMENTS

---

## 参数解析

从 `$ARGUMENTS` 中解析：

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| 发布目标 | `pypi` 或 `testpypi` | 是 | — |
| 版本号 | 如 `0.1.1a5` | 否 | 最新 git tag 对应的版本 |

如果用户未提供发布目标，**必须询问用户**，不可假设。

---

## 工作流

```
解析参数 → 确定版本 → 前置检查 → 创建 GitHub Release → 监控流水线 → 报告结果
```

---

## 第一步：确定版本

如果用户指定了版本号，使用指定版本。否则获取最新 tag：

```bash
git describe --tags --abbrev=0
```

版本号格式为 `v{version}`（如 `v0.1.1a5`），提取纯版本号时去掉 `v` 前缀。

---

## 第二步：前置检查

依次执行以下检查，任一失败则中止并告知用户：

### 2.1 确认 tag 存在

```bash
git tag -l "v{version}"
```

如果 tag 不存在，提示用户先执行版本 bump：
```bash
uv run bump-my-version bump patch|minor|major
```

### 2.2 确认 pyproject.toml 版本一致

```bash
uv run bump-my-version show current_version
```

版本必须与目标 tag 一致，否则中止。

### 2.3 确认 tag 已推送到远程

```bash
git ls-remote --tags origin "refs/tags/v{version}"
```

如果远程没有该 tag，提示用户推送。

### 2.4 确认无同名 Release 已存在

```bash
gh release view "v{version}" 2>&1
```

如果已存在：
- 询问用户是否删除后重建
- 用户确认后执行 `gh release delete "v{version}" --yes`

---

## 第三步：创建 GitHub Release

根据发布目标决定是否添加 `--prerelease` 标签：

| 发布目标 | `--prerelease` | CI 触发的 Job |
|---------|----------------|--------------|
| `testpypi` | **添加** | `publish-testpypi`（条件：`prerelease == true`） |
| `pypi` | **不添加** | `publish-pypi`（条件：`prerelease == false && target_commitish == 'main'`） |

### 创建命令

**发布到 TestPyPI：**
```bash
gh release create "v{version}" --title "v{version}" --prerelease --generate-notes
```

**发布到 PyPI：**
```bash
gh release create "v{version}" --title "v{version}" --generate-notes
```

> **关键经验：** 创建 Release 时的 `prerelease` 属性会写入 GitHub event payload，后续通过 `gh release edit` 修改该属性**不会**改变已触发 workflow 的 event payload。因此必须在创建时就设置正确，如果设错了需要**删除 Release 后重新创建**。

---

## 第四步：监控流水线

### 4.1 获取触发的 workflow run

```bash
gh run list --workflow=publish.yml --limit 1
```

### 4.2 等待并检查结果

```bash
gh run watch {run_id}
```

或轮询检查状态：

```bash
gh run view {run_id} --json status,conclusion,jobs --jq '{status, conclusion, jobs: [.jobs[] | {name, status, conclusion}]}'
```

### 4.3 结果报告

根据流水线结果向用户报告：

**成功：**
```
✅ v{version} 已成功发布到 {PyPI|TestPyPI}
📦 https://{pypi.org|test.pypi.org}/project/whosellm/{version}/
🔗 https://github.com/JIAQIA/whosellm/releases/tag/v{version}
```

**失败：**
- 运行 `gh run view {run_id} --log-failed` 获取失败日志
- 向用户展示失败原因和建议修复方式

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| TestPyPI job 报 "environment protection rules" | tag 不在 testpypi 环境的允许列表中 | 检查 GitHub repo Settings → Environments → testpypi 的 deployment protection rules |
| PyPI job 被跳过 | Release 创建时带了 `--prerelease`，或 target_commitish 不是 main | 删除 Release 重新创建，不带 `--prerelease` |
| Version mismatch | pyproject.toml 版本与 tag 不一致 | 先执行 `uv run bump-my-version bump` 再创建 Release |
| Release 已存在 | 之前创建过同名 Release | 删除旧 Release 后重新创建 |
