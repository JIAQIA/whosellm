# filename: openai_gpt_3_5.py
# @Time    : 2025/11/8 13:32
# @Author  : JQQ
# @Email   : jiaqia@qknode.com
# @Software: PyCharm
from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.models.config import ModelFamilyConfig
from llmeta.provider import Provider

# ======================================================== ====================
# GPT-3.5 系列 / GPT-3.5 Series


GPT_3_5 = ModelFamilyConfig(
    family=ModelFamily.GPT_3_5,
    provider=Provider.OPENAI,
    version_default="3.5",
    variant_priority_default=(1,),  # base 的优先级 / base priority
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
