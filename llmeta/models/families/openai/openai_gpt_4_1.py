# filename: openai_gpt_4_1.py
# @Time    : 2025/11/8 13:29
# @Author  : JQQ
# @Email   : jiaqia@qknode.com
# @Software: PyCharm
from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.models.config import ModelFamilyConfig, SpecificModelConfig
from llmeta.provider import Provider

# ============================================================================
# GPT-4.1 系列 / GPT-4.1 Series
# ============================================================================

GPT_4_1 = ModelFamilyConfig(
    family=ModelFamily.GPT_4_1,
    provider=Provider.OPENAI,
    version_default="4.1",
    variant_priority_default=(1,),  # base 的优先级 / base priority
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
            variant_priority=(0,),  # mini 的优先级 / mini priority
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
            variant_priority=(0,),  # nano 的优先级 (< mini) / nano priority (< mini)
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
