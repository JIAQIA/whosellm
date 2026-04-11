from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5.3 系列 / GPT-5.3 Series
#
# 注意：GPT-5.3 没有通用 API 模型，仅有 Codex 变体
# Note: GPT-5.3 has no general-purpose API model, only Codex variant
# ============================================================================

GPT_5_3 = ModelFamilyConfig(
    family=ModelFamily.GPT_5_3,
    provider=Provider.OPENAI,
    version_default="5.3",
    variant_priority_default=(1,),
    patterns=[
        "gpt-5.3-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "gpt-5.3-{variant:variant}",
        "gpt-5.3-{year:4d}-{month:2d}-{day:2d}",
        "gpt-5.3",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_fine_tuning=False,
        supports_distillation=False,
        max_tokens=128_000,
        context_window=1_050_000,
    ),
    specific_models={
        "gpt-5.3-codex": SpecificModelConfig(
            version_default="5.3",
            variant_default="codex",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.3-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.3-codex",
            ],
        ),
    },
)
