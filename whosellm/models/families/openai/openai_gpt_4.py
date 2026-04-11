# filename: openai_gpt_4.py
# @Time    : 2025/11/8 13:31
# @Author  : JQQ
# @Email   : jiaqia@qknode.com
# @Software: PyCharm
from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-4 系列 / GPT-4 Series
# ============================================================================

GPT_4 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="4.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[],  # 父 patterns 由 gpt_5_4.py 通过 Registry Merge 提供
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=False,
        supports_json_outputs=True,
        max_tokens=8192,
        context_window=128000,
    ),
    specific_models={
        "gpt-4": SpecificModelConfig(
            version_default="4.0",
            variant_default="base",
            variant_priority=(1,),
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-4-{mmdd:4d}",
                "gpt-4-{year:4d}-{month:2d}-{day:2d}",
                "gpt-4",
            ],
        ),
    },
)
