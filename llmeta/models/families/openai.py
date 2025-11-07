# filename: openai.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
OpenAI 模型家族配置 / OpenAI model family configurations
"""

from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.models.config import ModelFamilyConfig
from llmeta.provider import Provider

# ============================================================================
# GPT-4 系列 / GPT-4 Series
# ============================================================================

GPT_4 = ModelFamilyConfig(
    family=ModelFamily.GPT_4,
    provider=Provider.OPENAI,
    version_default="4.0",
    patterns=[
        "gpt-4o-{variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-4o-mini-2024-07-18
        "gpt-4o-{variant}",  # gpt-4o-mini
        "gpt-4-{variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-4-turbo-2024-04-09
        "gpt-4-{variant}-{mmdd:4d}",  # gpt-4-0125-preview
        "gpt-4-{variant}",  # gpt-4-turbo, gpt-4-plus, gpt-4-custom
        "gpt-4o",  # gpt-4o (base)
        "gpt-4",  # gpt-4 (base)
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=128000,
    ),
    # 特定模型的精确配置 / Precise configuration for specific models
    specific_models={
        "gpt-4-turbo": (
            "4.0",
            "turbo",
            ModelCapabilities(
                supports_vision=True,  # turbo 支持视觉
                supports_function_calling=True,
                supports_streaming=True,
                max_tokens=4096,
                context_window=128000,
            ),
        ),
        "gpt-4o": (
            "4.0",
            "omni",
            ModelCapabilities(
                supports_vision=True,
                supports_audio=True,  # omni 支持音频
                supports_streaming=True,
                max_tokens=16384,
                context_window=128000,
            ),
        ),
        "gpt-4-0125-preview": (
            "4.0",
            "base",  # preview 版本是 base variant
            ModelCapabilities(
                supports_function_calling=True,
                supports_streaming=True,
                max_tokens=8192,
                context_window=128000,
            ),
        ),
    },
)

# ============================================================================
# GPT-3.5 系列 / GPT-3.5 Series

GPT_3_5 = ModelFamilyConfig(
    family=ModelFamily.GPT_3_5,
    provider=Provider.OPENAI,
    version_default="3.5",
    patterns=[
        "gpt-3.5-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "gpt-3.5-{variant}",
        "gpt-3.5",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=4096,
        context_window=16385,
    ),
)

# ============================================================================
# O1 系列 / O1 Series
# ============================================================================

O1 = ModelFamilyConfig(
    family=ModelFamily.O1,
    provider=Provider.OPENAI,
    version_default="1.0",
    patterns=[
        "o1-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "o1-{variant}",
        "o1",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,  # O1 支持推理 / O1 supports reasoning
        supports_function_calling=False,
        supports_streaming=False,
        max_tokens=100000,
        context_window=200000,
    ),
)

# ============================================================================
# O3 系列 / O3 Series
# ============================================================================

O3 = ModelFamilyConfig(
    family=ModelFamily.O3,
    provider=Provider.OPENAI,
    version_default="3.0",
    patterns=[
        "o3-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "o3-{variant}",
        "o3",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,  # O3 支持推理 / O3 supports reasoning
        supports_function_calling=False,
        supports_streaming=False,
        max_tokens=100000,
        context_window=200000,
    ),
)
