# filename: openai_gpt_5.py
# @Time    : 2025/11/8 13:28
# @Author  : JQQ
# @Email   : jiaqia@qknode.com
# @Software: PyCharm
from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5 系列 / GPT-5 Series
# ============================================================================


GPT_5 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="5.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[],  # 父 patterns 由 gpt_5_4.py 通过 Registry Merge 提供
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_vision=True,
        supports_pdf=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_json_outputs=True,
        supports_fine_tuning=False,
        supports_distillation=True,
        supports_web_search=True,
        supports_file_search=True,
        supports_image_generation=True,
        supports_code_interpreter=True,
        supports_mcp=True,
        max_tokens=128_000,
        context_window=400_000,
    ),
    specific_models={
        "gpt-5": SpecificModelConfig(
            version_default="5.0",
            variant_default="base",
            variant_priority=(1,),
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5",
            ],
        ),
        "gpt-5-mini": SpecificModelConfig(
            version_default="5.0",
            variant_default="mini",
            variant_priority=(0,),  # mini 的优先级 / mini priority
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=False,
                supports_code_interpreter=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-mini",
            ],
        ),
        "gpt-5-nano": SpecificModelConfig(
            version_default="5.0",
            variant_default="nano",
            variant_priority=(0,),  # nano 的优先级 / nano priority
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=False,
                supports_code_interpreter=False,
                supports_mcp=True,
                max_tokens=16_384,
                context_window=128_000,
            ),
            patterns=[
                "gpt-5-nano-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-nano",
            ],
        ),
        "gpt-5-pro": SpecificModelConfig(
            version_default="5.0",
            variant_default="pro",
            variant_priority=(4,),  # pro 的优先级 / pro priority
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
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
                "gpt-5-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-pro",
            ],
        ),
        "gpt-5-codex": SpecificModelConfig(
            version_default="5.0",
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
                context_window=400_000,
            ),
            patterns=[
                "gpt-5-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-codex",
            ],
        ),
    },
)
