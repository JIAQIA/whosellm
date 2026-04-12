"""ZhipuAI E2E 元数据测试。

来源: https://docs.z.ai/guides/llm/ | https://docs.z.ai/guides/vlm/
采集日期: 2026-04-12
"""

import pytest

from whosellm import ModelFamily, Provider

from .conftest import assert_model_metadata

# ============================================================================
# GLM Family — Version 5.0
# 来源: https://docs.z.ai/guides/llm/glm-5
# ============================================================================

GLM_50_MODELS = [
    (
        "glm-5",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM,
            "version": "5.0",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 200_000,
            "max_tokens": 128_000,
        },
    ),
]

# ============================================================================
# GLM Family — Version 4.7
# 来源: https://docs.z.ai/guides/llm/glm-4.7
# ============================================================================

GLM_47_MODELS = [
    (
        "glm-4.7",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM,
            "version": "4.7",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 200_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "glm-4.7-flash",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM,
            "version": "4.7",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 200_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "glm-4.7-flashx",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM,
            "version": "4.7",
            "variant": "flashx",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 200_000,
            "max_tokens": 128_000,
        },
    ),
]

# ============================================================================
# GLM Family — Version 4.6
# 来源: https://docs.z.ai/guides/llm/glm-4.6
# ============================================================================

GLM_46_MODELS = [
    (
        "glm-4.6",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM,
            "version": "4.6",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": False,
            "supports_web_search": True,
            "context_window": 200_000,
            "max_tokens": 128_000,
        },
    ),
]

# ============================================================================
# GLM Family — Version 4.5
# 来源: https://docs.z.ai/guides/llm/glm-4.5
# ============================================================================

GLM_45_MODELS = [
    (
        "glm-4.5",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM,
            "version": "4.5",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 128_000,
            "max_tokens": 96_000,
        },
    ),
]

# ============================================================================
# GLM-Vision Family — Version 4.6
# 来源: https://docs.z.ai/guides/vlm/glm-4.6v
# ============================================================================

GLM_VISION_46_MODELS = [
    (
        "glm-4.6v",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM_VISION,
            "version": "4.6",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 128_000,
            "max_tokens": 128_000,
        },
    ),
    (
        "glm-4.6v-flash",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM_VISION,
            "version": "4.6",
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": True,
            "supports_structured_outputs": True,
            "context_window": 128_000,
            "max_tokens": 128_000,
        },
    ),
]

# ============================================================================
# GLM-Vision Family — Version 4.5
# 来源: https://docs.z.ai/guides/vlm/glm-4.5v
# ============================================================================

GLM_VISION_45_MODELS = [
    (
        "glm-4.5v",
        {
            "provider": Provider.ZHIPU,
            "family": ModelFamily.GLM_VISION,
            "version": "4.5",
            "variant": "base",
            "supports_thinking": True,
            "supports_vision": True,
            "supports_video": True,
            "supports_streaming": True,
            "supports_function_calling": False,
            "context_window": 64_000,
            "max_tokens": 16_384,
        },
    ),
]

# ============================================================================
# 聚合 + 参数化
# ============================================================================

ALL_MODELS = GLM_50_MODELS + GLM_47_MODELS + GLM_46_MODELS + GLM_45_MODELS + GLM_VISION_46_MODELS + GLM_VISION_45_MODELS


@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name,expected",
    ALL_MODELS,
    ids=[m[0] for m in ALL_MODELS],
)
def test_model_metadata(model_name: str, expected: dict) -> None:  # type: ignore[type-arg]
    """验证 ZhipuAI 模型元数据与官方文档一致。"""
    assert_model_metadata(model_name, expected)
