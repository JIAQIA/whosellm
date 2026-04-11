from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5.4 系列 / GPT-5.4 Series (当前旗舰 / Current flagship)
# ============================================================================

GPT_5_4 = ModelFamilyConfig(
    family=ModelFamily.GPT_5_4,
    provider=Provider.OPENAI,
    version_default="5.4",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "gpt-5.4-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "gpt-5.4-{variant:variant}",
        "gpt-5.4-{year:4d}-{month:2d}-{day:2d}",
        "gpt-5.4",
    ],
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
        supports_mcp=True,
        max_tokens=128_000,
        context_window=1_050_000,
    ),
    specific_models={
        "gpt-5.4-pro": SpecificModelConfig(
            version_default="5.4",
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
                supports_mcp=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.4-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.4-pro",
            ],
        ),
        "gpt-5.4-mini": SpecificModelConfig(
            version_default="5.4",
            variant_default="mini",
            variant_priority=(0,),  # mini 的优先级 / mini priority
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
                supports_mcp=True,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5.4-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.4-mini",
            ],
        ),
        "gpt-5.4-nano": SpecificModelConfig(
            version_default="5.4",
            variant_default="nano",
            variant_priority=(0,),  # nano 的优先级 / nano priority
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
                supports_computer_use=False,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5.4-nano-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.4-nano",
            ],
        ),
    },
)
