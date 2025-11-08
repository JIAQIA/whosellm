# filename: alibaba.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
阿里巴巴模型家族配置 / Alibaba model family configurations
"""

from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.models.config import ModelFamilyConfig, SpecificModelConfig
from llmeta.provider import Provider

# ============================================================================
# Qwen 系列 / Qwen Series
# ============================================================================

QWEN = ModelFamilyConfig(
    family=ModelFamily.QWEN,
    provider=Provider.ALIBABA,
    version_default="1.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "qwen{version:d}-{variant:variant}",
        "qwen-{version:d}-{variant:variant}",
        "qwen-{variant:variant}",
        "qwen",
        "tongyi",  # 别名 / Alias
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=32000,
    ),
    specific_models={
        "qwen3-vl-plus": SpecificModelConfig(
            version="3",
            variant="vl-plus",
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                max_tokens=32000,
                context_window=256000,
            ),
            patterns=[
                "qwen3-vl-plus-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-plus",
            ],
        ),
    },
)
