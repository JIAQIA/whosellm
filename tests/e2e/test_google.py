"""Google E2E 元数据测试。

来源: https://ai.google.dev/gemini-api/docs/models
采集日期: 2026-04-12（2026-08-20 增补 3.5/3.6/3.7 Flash、Nano Banana 2 系列、Live/TTS 等新模型）
"""

import pytest

from whosellm import ModelFamily, Provider

from .conftest import assert_model_metadata

# ============================================================================
# Gemini Family — Version 3.x (Preview)
# 来源: https://ai.google.dev/gemini-api/docs/gemini-3
# ============================================================================

GEMINI_3X_MODELS = [
    (
        "gemini-3.1-pro-preview",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "pro",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-3-flash-preview",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.0",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-3.1-flash-lite-preview",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "flash-lite",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        # NOTE: 官方文档标注 thinking=Supported，但实测 image-preview 模型开启
        # thinking 存在问题，因此保持 False。
        "gemini-3-pro-image-preview",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.0",
            "variant": "pro-image",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": False,
            "supports_video": False,
            "supports_streaming": True,
            "supports_function_calling": False,
            "supports_structured_outputs": True,
            "supports_image_generation": True,
            "context_window": 65_536,
            "max_tokens": 32_768,
        },
    ),
]

# ============================================================================
# Gemini Family — 2026-08 新增（GA Flash 主线 / Nano Banana 2 / Live / TTS）
# 来源: https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash 等（2026-08-20 采集）
# ============================================================================

GEMINI_2026_NEW_MODELS = [
    (
        "gemini-3.7-flash",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.7",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-3.6-flash",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.6",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-3.5-flash",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.5",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-3.5-flash-lite",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.5",
            "variant": "flash-lite",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-3.1-flash-lite",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "flash-lite",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        # Nano Banana 2：官方卡片 thinking=Supported，但接口不支持配置 thinking 行为，按家族惯例置 False
        "gemini-3.1-flash-image",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "flash-image",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": False,
            "supports_streaming": True,
            "supports_function_calling": False,
            "supports_structured_outputs": False,
            "supports_image_generation": True,
            "context_window": 131_072,
            "max_tokens": 32_768,
        },
    ),
    (
        "gemini-3.1-flash-lite-image",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "flash-lite-image",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_image_generation": True,
            "context_window": 65_536,
            "max_tokens": 4_096,
        },
    ),
    (
        # Nano Banana Pro（GA）
        "gemini-3-pro-image",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.0",
            "variant": "pro-image",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": False,
            "supports_streaming": True,
            "supports_function_calling": False,
            "supports_structured_outputs": False,
            "supports_image_generation": True,
            "context_window": 65_536,
            "max_tokens": 32_768,
        },
    ),
    (
        # 官方详情页未附规格卡：ctx 取 Live API 原生音频模型约束 128k，max 参照迁移源 12-2025
        "gemini-3.1-flash-live-preview",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "flash-live",
            "supports_thinking": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_audio_generation": True,
            "context_window": 131_072,
            "max_tokens": 8_192,
        },
    ),
    (
        "gemini-3.1-flash-tts-preview",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "3.1",
            "variant": "flash-tts",
            "supports_thinking": False,
            "supports_vision": False,
            "supports_audio": False,
            "supports_streaming": True,
            "supports_structured_outputs": False,
            "supports_audio_generation": True,
            "context_window": 8_192,
            "max_tokens": 16_384,
        },
    ),
]

# ============================================================================
# Gemini Family — Version 2.5 (Stable)
# 来源: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash
#        https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro
#        https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite
# ============================================================================

GEMINI_25_MODELS = [
    (
        "gemini-2.5-pro",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "2.5",
            "variant": "pro",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-2.5-flash",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "2.5",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
    (
        "gemini-2.5-flash-lite",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "2.5",
            "variant": "flash-lite",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 65_536,
        },
    ),
]

# ============================================================================
# Gemini Family — Version 2.0 (Deprecated)
# 来源: https://ai.google.dev/gemini-api/docs/models/gemini-2.0-flash
#        https://ai.google.dev/gemini-api/docs/models/gemini-2.0-flash-lite
# ============================================================================

GEMINI_20_MODELS = [
    (
        "gemini-2.0-flash",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "2.0",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 8_192,
        },
    ),
    (
        "gemini-2.0-flash-lite",
        {
            "provider": Provider.GOOGLE,
            "family": ModelFamily.GEMINI,
            "version": "2.0",
            "variant": "flash-lite",
            "supports_thinking": False,
            "supports_vision": True,
            "supports_audio": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 1_048_576,
            "max_tokens": 8_192,
        },
    ),
]

# ============================================================================
# 聚合 + 参数化
# ============================================================================

ALL_MODELS = GEMINI_3X_MODELS + GEMINI_2026_NEW_MODELS + GEMINI_25_MODELS + GEMINI_20_MODELS


@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name,expected",
    ALL_MODELS,
    ids=[m[0] for m in ALL_MODELS],
)
def test_model_metadata(model_name: str, expected: dict) -> None:  # type: ignore[type-arg]
    """验证 Google 模型元数据与官方文档一致。"""
    assert_model_metadata(model_name, expected)
