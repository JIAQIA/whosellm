# filename: openai.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
OpenAI 模型定义 / OpenAI model definitions
"""

from llmver.capabilities import ModelCapabilities
from llmver.models.base import ModelFamily, ModelInfo, parse_version, register_model
from llmver.provider import Provider

# GPT-4 系列 / GPT-4 series
# variant_priority: (0,) < (1,) < (2,) 表示 base < turbo < omni
# variant_priority: (0,) < (1,) < (2,) means base < turbo < omni
register_model(
    "gpt-4",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.GPT_4,
        version="4.0",
        variant="base",
        capabilities=ModelCapabilities(
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=8192,
        ),
        version_tuple=parse_version("4.0"),
        variant_priority=(1,),  # base
    ),
)

register_model(
    "gpt-4-turbo",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.GPT_4,
        version="4.0",
        variant="turbo",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=4096,
            context_window=128000,
        ),
        version_tuple=parse_version("4.0"),
        variant_priority=(2,),  # turbo > base
    ),
)

register_model(
    "gpt-4o",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.GPT_4,
        version="4.0",
        variant="omni",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_audio=True,
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=16384,
            context_window=128000,
        ),
        version_tuple=parse_version("4.0"),
        variant_priority=(3,),  # omni > turbo
    ),
)

register_model(
    "gpt-4o-mini",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.GPT_4,
        version="4.0",
        variant="omni-mini",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=16384,
            context_window=128000,
        ),
        version_tuple=parse_version("4.0"),
        variant_priority=(0,),  # mini < base
    ),
)

# GPT-3.5 系列 / GPT-3.5 series
register_model(
    "gpt-3.5-turbo",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.GPT_3_5,
        version="3.5",
        variant="turbo",
        capabilities=ModelCapabilities(
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=4096,
            context_window=16385,
        ),
        version_tuple=parse_version("3.5"),
        variant_priority=(1,),
    ),
)

# O1 系列（推理模型） / O1 series (reasoning models)
register_model(
    "o1",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.O1,
        version="1.0",
        variant="base",
        capabilities=ModelCapabilities(
            supports_thinking=True,
            supports_streaming=False,
            max_tokens=100000,
            context_window=200000,
        ),
        version_tuple=parse_version("1.0"),
        variant_priority=(1,),
    ),
)

register_model(
    "o1-mini",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.O1,
        version="1.0",
        variant="mini",
        capabilities=ModelCapabilities(
            supports_thinking=True,
            supports_streaming=False,
            max_tokens=65536,
            context_window=128000,
        ),
        version_tuple=parse_version("1.0"),
        variant_priority=(0,),  # mini < base
    ),
)

register_model(
    "o1-preview",
    ModelInfo(
        provider=Provider.OPENAI,
        family=ModelFamily.O1,
        version="1.0",
        variant="preview",
        capabilities=ModelCapabilities(
            supports_thinking=True,
            supports_streaming=False,
            max_tokens=32768,
            context_window=128000,
        ),
        version_tuple=parse_version("1.0"),
        variant_priority=(0, 5),  # preview 介于 mini 和 base 之间 / preview is between mini and base
    ),
)
