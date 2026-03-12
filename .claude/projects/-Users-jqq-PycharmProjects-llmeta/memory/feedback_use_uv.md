---
name: use-uv-run
description: Always use uv run for all Python/poe commands, never pip install or bare python
type: feedback
---

Always use `uv run` to execute Python commands in this project. Never use `pip install` or bare `python`/`poe` commands.

**Why:** The project uses uv for environment management. Using pip or bare python bypasses the managed environment and may fail with missing dependencies.

**How to apply:** Prefix all commands with `uv run`, e.g. `uv run poe test`, `uv run python -m pytest ...`, `uv run python -c "..."`.
