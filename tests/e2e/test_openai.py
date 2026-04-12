"""OpenAI E2E 元数据测试。

来源: https://developers.openai.com/api/docs/models
采集日期: 2026-04-12
"""

import pytest

from whosellm import ModelFamily, Provider

from .conftest import assert_model_metadata

# ============================================================================
# GPT Family (latest: 5.4)
# 来源: https://developers.openai.com/api/docs/models/gpt-5.4
# ============================================================================

GPT_MODELS = [
    (
        "gpt-5.4",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT,
            "version": "5.4",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": True,
            "context_window": 1_050_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "gpt-5.4-mini",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT,
            "version": "5.4",
            "variant": "mini",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": True,
            "context_window": 400_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "gpt-5.4-nano",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT,
            "version": "5.4",
            "variant": "nano",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "supports_computer_use": False,
            "context_window": 400_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "gpt-5.4-pro",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT,
            "version": "5.4",
            "variant": "pro",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_code_interpreter": False,
            "supports_computer_use": True,
            "context_window": 1_050_000,
            "max_tokens": 128_000,
        },
    ),
]

# ============================================================================
# GPT-4o Family (latest: 4.0)
# 来源: https://developers.openai.com/api/docs/models/gpt-4o
# ============================================================================

GPT4O_MODELS = [
    (
        "gpt-4o",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT_4O,
            "version": "4.0",
            "variant": "omni",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 128_000,
            "max_tokens": 16_384,
        },
    ),
    (
        "gpt-4o-mini",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT_4O,
            "version": "4.0",
            "variant": "mini",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 128_000,
            "max_tokens": 16_384,
        },
    ),
    (
        "gpt-4o-audio-preview",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT_4O,
            "version": "4.0",
            "variant": "audio-preview",
            "supports_thinking": False,
            "supports_vision": False,
            "supports_audio": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "context_window": 128_000,
            "max_tokens": 16_384,
        },
    ),
    (
        "gpt-4o-mini-audio-preview",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT_4O,
            "version": "4.0",
            "variant": "mini-audio-preview",
            "supports_thinking": False,
            "supports_vision": False,
            "supports_audio": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "context_window": 128_000,
            "max_tokens": 16_384,
        },
    ),
    (
        "gpt-4o-mini-realtime-preview",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.GPT_4O,
            "version": "4.0",
            "variant": "mini-realtime-preview",
            "supports_thinking": False,
            "supports_vision": False,
            "supports_audio": True,
            "supports_streaming": False,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "context_window": 16_000,
            "max_tokens": 4_096,
        },
    ),
]

# ============================================================================
# O Family (latest: 4.0)
# 来源: https://developers.openai.com/api/docs/models/o4-mini
# ============================================================================

O_MODELS = [
    (
        "o4-mini",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.O,
            "version": "4.0",
            "variant": "mini",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 200_000,
            "max_tokens": 100_000,
        },
    ),
    (
        "o4-mini-deep-research",
        {
            "provider": Provider.OPENAI,
            "family": ModelFamily.O,
            "version": "4.0",
            "variant": "mini-deep-research",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_streaming": True,
            "supports_function_calling": False,
            "supports_structured_outputs": False,
            "context_window": 200_000,
            "max_tokens": 100_000,
        },
    ),
]

# ============================================================================
# 聚合 + 参数化
# ============================================================================

ALL_MODELS = GPT_MODELS + GPT4O_MODELS + O_MODELS


@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name,expected",
    ALL_MODELS,
    ids=[m[0] for m in ALL_MODELS],
)
def test_model_metadata(model_name: str, expected: dict) -> None:  # type: ignore[type-arg]
    """验证 OpenAI 模型元数据与官方文档一致。"""
    assert_model_metadata(model_name, expected)
