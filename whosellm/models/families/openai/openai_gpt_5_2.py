from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5.2 系列 / GPT-5.2 Series
# ============================================================================

GPT_5_2 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="5.2",
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
        "gpt-5.2": SpecificModelConfig(
            version_default="5.2",
            variant_default="base",
            variant_priority=(1,),
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.2-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.2",
            ],
        ),
        "gpt-5.2-pro": SpecificModelConfig(
            version_default="5.2",
            variant_default="pro",
            variant_priority=(4,),
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
                supports_computer_use=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.2-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.2-pro",
            ],
        ),
        "gpt-5.2-codex": SpecificModelConfig(
            version_default="5.2",
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
                "gpt-5.2-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.2-codex",
            ],
        ),
    },
)
