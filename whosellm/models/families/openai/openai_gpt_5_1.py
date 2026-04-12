from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5.1 系列 / GPT-5.1 Series
# ============================================================================

GPT_5_1 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="5.1",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[],  # 父 patterns 由 gpt_5_4.py 通过 Registry Merge 提供
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_fine_tuning=False,
        supports_distillation=True,
        supports_web_search=True,
        supports_file_search=True,
        supports_image_generation=True,
        supports_code_interpreter=True,

        max_tokens=128_000,
        context_window=1_050_000,
    ),
    specific_models={
        "gpt-5.1": SpecificModelConfig(
            version_default="5.1",
            variant_default="base",
            variant_priority=(1,),
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.1-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1",
            ],
        ),
        "gpt-5.1-codex": SpecificModelConfig(
            version_default="5.1",
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
                "gpt-5.1-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1-codex",
            ],
        ),
        "gpt-5.1-codex-mini": SpecificModelConfig(
            version_default="5.1",
            variant_default="codex-mini",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5.1-codex-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1-codex-mini",
            ],
        ),
        "gpt-5.1-codex-max": SpecificModelConfig(
            version_default="5.1",
            variant_default="codex-max",
            variant_priority=(5,),
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
                "gpt-5.1-codex-max-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1-codex-max",
            ],
        ),
    },
)
