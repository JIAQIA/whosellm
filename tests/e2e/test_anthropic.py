"""Anthropic E2E 元数据测试。

来源: https://platform.claude.com/docs/en/docs/about-claude/models
采集日期: 2026-04-12
"""

import pytest

from whosellm import ModelFamily, Provider

from .conftest import assert_model_metadata

# ============================================================================
# Claude Family — Latest (version 4.6)
# 来源: https://platform.claude.com/docs/en/docs/about-claude/models/overview
# ============================================================================

CLAUDE_LATEST_MODELS = [
    (
        "claude-opus-4-6",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.6",
            "variant": "opus",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": True,
            "context_window": 1_000_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "claude-sonnet-4-6",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.6",
            "variant": "sonnet",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": True,
            "context_window": 1_000_000,
            "max_tokens": 64_000,
        },
    ),
]

# ============================================================================
# Claude Family — Version 4.5
# 来源: https://platform.claude.com/docs/en/docs/about-claude/models/overview (Legacy)
# ============================================================================

CLAUDE_45_MODELS = [
    (
        "claude-haiku-4-5",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.5",
            "variant": "haiku",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": True,
            "context_window": 200_000,
            "max_tokens": 64_000,
        },
    ),
    (
        "claude-sonnet-4-5",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.5",
            "variant": "sonnet",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": True,
            "context_window": 200_000,
            "max_tokens": 64_000,
        },
    ),
]

# ============================================================================
# Claude Family — Version 4.1
# 来源: https://platform.claude.com/docs/en/docs/about-claude/models/overview (Legacy)
# ============================================================================

CLAUDE_41_MODELS = [
    (
        "claude-opus-4-1",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.1",
            "variant": "opus",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_computer_use": True,
            "context_window": 200_000,
            "max_tokens": 32_000,
        },
    ),
]

# ============================================================================
# Claude Family — Version 4.0
# 来源: https://platform.claude.com/docs/en/docs/about-claude/models/overview (Legacy)
# ============================================================================

CLAUDE_40_MODELS = [
    (
        "claude-sonnet-4-0",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.0",
            "variant": "sonnet",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_computer_use": True,
            "context_window": 200_000,
            "max_tokens": 64_000,
        },
    ),
    (
        "claude-opus-4-0",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "4.0",
            "variant": "opus",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_computer_use": True,
            "context_window": 200_000,
            "max_tokens": 32_000,
        },
    ),
]

# ============================================================================
# Claude Family — Version 3.0 (deprecated)
# 来源: https://platform.claude.com/docs/en/docs/about-claude/models/overview (Legacy)
# ============================================================================

CLAUDE_30_MODELS = [
    (
        "claude-3-haiku",
        {
            "provider": Provider.ANTHROPIC,
            "family": ModelFamily.CLAUDE,
            "version": "3.0",
            "variant": "haiku",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_computer_use": False,
            "context_window": 200_000,
            "max_tokens": 4_096,
        },
    ),
]

# ============================================================================
# 聚合 + 参数化
# ============================================================================

ALL_MODELS = CLAUDE_LATEST_MODELS + CLAUDE_45_MODELS + CLAUDE_41_MODELS + CLAUDE_40_MODELS + CLAUDE_30_MODELS


@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name,expected",
    ALL_MODELS,
    ids=[m[0] for m in ALL_MODELS],
)
def test_model_metadata(model_name: str, expected: dict) -> None:  # type: ignore[type-arg]
    """验证 Anthropic 模型元数据与官方文档一致。"""
    assert_model_metadata(model_name, expected)
