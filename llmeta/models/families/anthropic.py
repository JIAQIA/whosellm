# filename: anthropic.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Anthropic 模型家族配置 / Anthropic model family configurations
"""

from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.models.config import ModelFamilyConfig
from llmeta.provider import Provider

# ============================================================================
# Claude 系列 / Claude Series
# ============================================================================

CLAUDE = ModelFamilyConfig(
    family=ModelFamily.CLAUDE,
    provider=Provider.ANTHROPIC,
    version_default="3.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "claude-{version:d}-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "claude-{version:d}-{variant}",
        "claude-{variant}",
        "claude",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=4096,
        context_window=200000,
    ),
)
