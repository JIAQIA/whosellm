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
from llmeta.models.config import ModelFamilyConfig, SpecificModelConfig
from llmeta.provider import Provider

# ============================================================================
# GPT-5 系列 / GPT-5 Series
# ============================================================================

GPT_5 = ModelFamilyConfig(
    family=ModelFamily.GPT_5,
    provider=Provider.OPENAI,
    version_default="5.0",
    patterns=[
        "gpt-5-{variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-5-mini-2025-08-07
        "gpt-5-{variant}",  # gpt-5-mini
        "gpt-5",  # gpt-5 (base)
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_fine_tuning=False,
        supports_distillation=True,
        max_tokens=16384,
        context_window=256000,
    ),
    specific_models={
        "gpt-5-mini": SpecificModelConfig(
            version="5.0",
            variant="mini",
            capabilities=ModelCapabilities(
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=8192,
                context_window=128000,
            ),
            patterns=[
                "gpt-5-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-mini",
            ],
        ),
        "gpt-5-nano": SpecificModelConfig(
            version="5.0",
            variant="nano",
            capabilities=ModelCapabilities(
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=4096,
                context_window=64000,
            ),
            patterns=[
                "gpt-5-nano-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-nano",
            ],
        ),
        "gpt-5-pro": SpecificModelConfig(
            version="5.0",
            variant="pro",
            capabilities=ModelCapabilities(
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=24576,  # Pro版本token限制更高
                context_window=256000,
            ),
            patterns=[
                "gpt-5-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-pro",
            ],
        ),
    },
)

# ============================================================================
# GPT-4o 系列 / GPT-4o Series
# ============================================================================

GPT_4O = ModelFamilyConfig(
    family=ModelFamily.GPT_4O,
    provider=Provider.OPENAI,
    version_default="4.0",
    variant_default="omni",
    patterns=[
        "gpt-4o-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "gpt-4o-{year:4d}-{month:2d}-{day:2d}",  # 日期模式优先
        "gpt-4o-{variant}",
        "gpt-4o",
    ],
    capabilities=ModelCapabilities(
        supports_streaming=True,
        supports_function_calling=True,
        supports_structured_outputs=True,
        supports_fine_tuning=True,
        supports_distillation=True,
        supports_predicted_outputs=True,
        max_tokens=16384,
        context_window=128000,
    ),
    specific_models={
        "gpt-4o-audio-preview": SpecificModelConfig(
            version="4.0",
            variant="audio-preview",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=False,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_predicted_outputs=False,
                max_tokens=16384,
                context_window=128000,
            ),
            patterns=[
                "gpt-4o-audio-preview-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4o-audio-preview",
            ],
        ),
        "gpt-4o-mini": SpecificModelConfig(
            version="4.0",
            variant="mini",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_fine_tuning=True,
                supports_predicted_outputs=True,
                max_tokens=16384,
                context_window=128000,
            ),
            patterns=[
                "gpt-4o-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4o-mini",
            ],
        ),
        "gpt-4o-mini-audio-preview": SpecificModelConfig(
            version="4.0",
            variant="mini-audio-preview",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=False,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_predicted_outputs=False,
                max_tokens=16384,
                context_window=128000,
            ),
            patterns=[
                "gpt-4o-mini-audio-preview-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4o-mini-audio-preview",
            ],
        ),
        "gpt-4o-mini-realtime-preview": SpecificModelConfig(
            version="4.0",
            variant="mini-realtime-preview",
            capabilities=ModelCapabilities(
                supports_streaming=False,
                supports_function_calling=True,
                supports_structured_outputs=False,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_predicted_outputs=False,
                max_tokens=4096,
                context_window=16000,
            ),
            patterns=[
                "gpt-4o-mini-realtime-preview-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4o-mini-realtime-preview",
            ],
        ),
    },
)

# ============================================================================
# O4 系列 / O4 Series
# ============================================================================

O4 = ModelFamilyConfig(
    family=ModelFamily.O4,
    provider=Provider.OPENAI,
    version_default="4.0",
    patterns=[
        "o4-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "o4-{variant}",
    ],
    capabilities=ModelCapabilities(
        supports_streaming=True,
        supports_function_calling=True,
        supports_structured_outputs=True,
        supports_fine_tuning=True,
    ),
    specific_models={
        "o4-mini": SpecificModelConfig(
            version="4.0",
            variant="mini",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_fine_tuning=True,
            ),
            patterns=[
                "o4-mini-{year:4d}-{month:2d}-{day:2d}",
                "o4-mini",
            ],
        ),
        "o4-mini-deep-research": SpecificModelConfig(
            version="4.0",
            variant="mini-deep-research",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=False,
                supports_structured_outputs=False,
                supports_fine_tuning=False,
            ),
            patterns=[
                "o4-mini-deep-research-{year:4d}-{month:2d}-{day:2d}",
                "o4-mini-deep-research",
            ],
        ),
    },
)

# ============================================================================
# GPT-4.1 系列 / GPT-4.1 Series
# ============================================================================

GPT_4_1 = ModelFamilyConfig(
    family=ModelFamily.GPT_4_1,
    provider=Provider.OPENAI,
    version_default="4.1",
    patterns=[
        "gpt-4.1-{year:4d}-{month:2d}-{day:2d}",
        "gpt-4.1-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "gpt-4.1-{variant}",
        "gpt-4.1-{year:4d}-{month:2d}-{day:2d}",
        "gpt-4.1",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_fine_tuning=True,
        supports_distillation=True,
    ),
    specific_models={
        "gpt-4.1-mini": SpecificModelConfig(
            version="4.1",
            variant="mini",
            capabilities=ModelCapabilities(
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=True,
                supports_predicted_outputs=True,
            ),
            patterns=[
                "gpt-4.1-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4.1-mini",
            ],
        ),
        "gpt-4.1-nano": SpecificModelConfig(
            version="4.1",
            variant="nano",
            capabilities=ModelCapabilities(
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=True,
                supports_predicted_outputs=True,
            ),
            patterns=[
                "gpt-4.1-nano-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4.1-nano",
            ],
        ),
    },
)

# ============================================================================
# GPT-4 系列 / GPT-4 Series
# ============================================================================

GPT_4 = ModelFamilyConfig(
    family=ModelFamily.GPT_4,
    provider=Provider.OPENAI,
    version_default="4.0",
    patterns=[
        "gpt-4-{mmdd:4d}",  # gpt-4-0613
        "gpt-4",  # gpt-4 (base)
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=128000,
    ),
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
        "o1-{year:4d}-{month:2d}-{day:2d}",
        "o1-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "o1-{variant}",
        "o1",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        max_tokens=100000,
        context_window=200000,
    ),
    specific_models={
        "o1-pro": SpecificModelConfig(
            version="1.0",
            variant="pro",
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=False,
                supports_structured_outputs=True,
                max_tokens=100000,
                context_window=200000,
            ),
            patterns=[
                "o1-pro-{year:4d}-{month:2d}-{day:2d}",
                "o1-pro",
            ],
        ),
    },
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
        "o3-{year:4d}-{month:2d}-{day:2d}",
        "o3",
    ],
    capabilities=ModelCapabilities(
        supports_streaming=True,
        supports_function_calling=True,
        supports_structured_outputs=True,
    ),
    specific_models={
        "o3": SpecificModelConfig(
            version="3.0",
            variant="base",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
            ),
            patterns=[
                "o3-{year:4d}-{month:2d}-{day:2d}",
                "o3",
            ],
        ),
        "o3-mini": SpecificModelConfig(
            version="3.0",
            variant="mini",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
            ),
            patterns=[
                "o3-mini-{year:4d}-{month:2d}-{day:2d}",
                "o3-mini",
            ],
        ),
        "o3-pro": SpecificModelConfig(
            version="3.0",
            variant="pro",
            capabilities=ModelCapabilities(
                supports_streaming=False,
                supports_function_calling=True,
                supports_structured_outputs=True,
            ),
            patterns=[
                "o3-pro-{year:4d}-{month:2d}-{day:2d}",
                "o3-pro",
            ],
        ),
        "o3-deep-research": SpecificModelConfig(
            version="3.0",
            variant="deep-research",
            capabilities=ModelCapabilities(
                supports_streaming=True,
                supports_function_calling=False,
                supports_structured_outputs=False,
            ),
            patterns=[
                "o3-deep-research-{year:4d}-{month:2d}-{day:2d}",
                "o3-deep-research",
            ],
        ),
    },
)
