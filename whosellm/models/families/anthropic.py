# filename: anthropic.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Anthropic 模型家族配置 / Anthropic model family configurations
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ==========================================================================
# Claude 系列 / Claude Series
# ==========================================================================

CLAUDE = ModelFamilyConfig(
    family=ModelFamily.CLAUDE,
    provider=Provider.ANTHROPIC,
    version_default="4.6",
    variant_default="sonnet",
    variant_priority_default=(3,),  # sonnet 的默认优先级 / default priority for sonnet
    patterns=[
        "claude-{variant:variant}-{major:d}-{minor:d}@{snapshot:snapshot}",
        "claude-{variant:variant}-{major:d}-{minor:d}-{snapshot:snapshot}",
        "claude-{variant:variant}-{major:d}-{minor:d}",
        "claude-{variant:variant}-{major:d}-{snapshot:snapshot}",
        "claude-{variant:variant}-{major:d}@{snapshot:snapshot}",
        "claude-{variant:variant}-{major:d}",
        "claude-{major:d}-{minor:d}-{variant:variant}-{snapshot:snapshot}",
        "claude-{major:d}-{minor:d}-{variant:variant}",
        "claude-{major:d}-{variant:variant}-{snapshot:snapshot}",
        "claude-{major:d}-{variant:variant}",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_thinking=True,
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=64000,
        context_window=200000,
    ),
    specific_models={
        # Mythos-class（2026-06-09 发布）：全新顶级层级，优先级高于 opus
        # Mythos-class (released 2026-06-09): new top tier, ranks above opus
        # Fable 5 为公开版，Mythos 5 为 Glasswing 受邀版（能力相同，去掉安全分类器）
        "claude-fable-5": SpecificModelConfig(
            version_default="5.0",
            variant_default="fable",
            variant_priority=(6,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=True,  # 自适应思考常开 / adaptive thinking always on
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
            ),
            patterns=[
                "claude-fable-5-{snapshot:snapshot}",
                "claude-fable-5",
                "claude-fable-5@{snapshot:snapshot}",
            ],
        ),
        "claude-mythos-5": SpecificModelConfig(
            version_default="5.0",
            variant_default="mythos",
            variant_priority=(7,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=True,  # 自适应思考常开 / adaptive thinking always on
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
            ),
            patterns=[
                "claude-mythos-5-{snapshot:snapshot}",
                "claude-mythos-5",
                "claude-mythos-5@{snapshot:snapshot}",
            ],
        ),
        "claude-opus-4-8": SpecificModelConfig(
            version_default="4.8",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
            ),
            patterns=[
                "claude-opus-4-8-{snapshot:snapshot}",
                "claude-opus-4-8",
                "claude-opus-4-8@{snapshot:snapshot}",
            ],
        ),
        "claude-opus-4-7": SpecificModelConfig(
            version_default="4.7",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
            ),
            patterns=[
                "claude-opus-4-7-{snapshot:snapshot}",
                "claude-opus-4-7",
                "claude-opus-4-7@{snapshot:snapshot}",
            ],
        ),
        "claude-opus-4-6": SpecificModelConfig(
            version_default="4.6",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
            ),
            patterns=[
                "claude-opus-4-6-{snapshot:snapshot}",
                "claude-opus-4-6",
                "claude-opus-4-6@{snapshot:snapshot}",
            ],
        ),
        "claude-sonnet-4-6": SpecificModelConfig(
            version_default="4.6",
            variant_default="sonnet",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=1000000,
            ),
            patterns=[
                "claude-sonnet-4-6-{snapshot:snapshot}",
                "claude-sonnet-4-6",
                "claude-sonnet-4-6@{snapshot:snapshot}",
            ],
        ),
        "claude-sonnet-4-5": SpecificModelConfig(
            version_default="4.5",
            variant_default="sonnet",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=200000,
            ),
            patterns=[
                "claude-sonnet-4-5-{snapshot:snapshot}",
                "claude-sonnet-4-5",
                "claude-sonnet-4-5@{snapshot:snapshot}",
            ],
        ),
        "claude-haiku-4-5": SpecificModelConfig(
            version_default="4.5",
            variant_default="haiku",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=200000,
            ),
            patterns=[
                "claude-haiku-4-5-{snapshot:snapshot}",
                "claude-haiku-4-5",
                "claude-haiku-4-5@{snapshot:snapshot}",
            ],
        ),
        "claude-opus-4-5": SpecificModelConfig(
            version_default="4.5",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=200000,
            ),
            patterns=[
                "claude-opus-4-5-{snapshot:snapshot}",
                "claude-opus-4-5",
                "claude-opus-4-5@{snapshot:snapshot}",
            ],
        ),
        "claude-opus-4-1": SpecificModelConfig(
            version_default="4.1",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_computer_use=True,
                max_tokens=32000,
                context_window=200000,
            ),
            patterns=["claude-opus-4-1-{snapshot:snapshot}", "claude-opus-4-1", "claude-opus-4-1@{snapshot:snapshot}"],
        ),
        "claude-sonnet-4-0": SpecificModelConfig(
            version_default="4.0",
            variant_default="sonnet",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=200000,
            ),
            patterns=[
                "claude-sonnet-4-{snapshot:snapshot}",
                "claude-sonnet-4-0",
                "claude-sonnet-4-0@{snapshot:snapshot}",
            ],
        ),
        "claude-3-7-sonnet": SpecificModelConfig(
            version_default="3.7",
            variant_default="sonnet",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=200000,
            ),
            patterns=["claude-3-7-sonnet-{snapshot:snapshot}", "claude-3-7-sonnet-latest", "claude-3-7-sonnet"],
        ),
        "claude-opus-4-0": SpecificModelConfig(
            version_default="4.0",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_computer_use=True,
                max_tokens=32000,
                context_window=200000,
            ),
            patterns=["claude-opus-4-{snapshot:snapshot}", "claude-opus-4-0", "claude-opus-4-0@{snapshot:snapshot}"],
        ),
        "claude-3-5-haiku": SpecificModelConfig(
            version_default="3.5",
            variant_default="haiku",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_thinking=False,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                max_tokens=8000,
                context_window=200000,
            ),
            patterns=["claude-3-5-haiku-{snapshot:snapshot}", "claude-3-5-haiku-latest", "claude-3-5-haiku"],
        ),
        "claude-3-haiku": SpecificModelConfig(
            version_default="3.0",
            variant_default="haiku",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=False,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                max_tokens=4096,
                context_window=200000,
            ),
            patterns=["claude-3-haiku-{snapshot:snapshot}"],
        ),
    },
)
