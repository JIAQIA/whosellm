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
from llmeta.models.config import ModelFamilyConfig
from llmeta.provider import Provider

# ============================================================================
# Qwen 系列 / Qwen Series
# ============================================================================

QWEN = ModelFamilyConfig(
    family=ModelFamily.QWEN,
    provider=Provider.ALIBABA,
    version_default="1.0",
    patterns=[
        "qwen-{version:d}-{variant}",
        "qwen-{variant}",
        "qwen",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=32000,
    ),
)
