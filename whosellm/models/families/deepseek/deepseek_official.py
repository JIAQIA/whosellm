# filename: deepseek_official.py
# @Time    : 2025/11/9 15:57
# @Author  : Cascade AI
"""
DeepSeek 官方模型家族配置 / DeepSeek official model family configuration

当前主力：deepseek-v4-flash / deepseek-v4-pro（1M 上下文，384K 最大输出，
支持思考与非思考双模式）。
Current primary models: deepseek-v4-flash / deepseek-v4-pro (1M context, 384K max output,
both thinking and non-thinking modes supported).

兼容别名：deepseek-chat / deepseek-reasoner（官方宣布未来将废弃，当前分别对应
deepseek-v4-flash 的非思考与思考模式）。
Legacy aliases: deepseek-chat / deepseek-reasoner (announced to be deprecated;
currently map to deepseek-v4-flash non-thinking and thinking modes respectively).
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# V4 系列共用能力基线 / Shared capability baseline for V4 series
_V4_CAPABILITIES = ModelCapabilities(
    supports_thinking=True,
    supports_function_calling=True,
    supports_streaming=True,
    supports_json_outputs=True,
    # DeepSeek 仅提供 response_format={type:"json_object"}，不支持 json_schema
    # DeepSeek only supports response_format={type:"json_object"}, not json_schema
    supports_structured_outputs=False,
    max_tokens=384_000,
    context_window=1_000_000,
)

DEEPSEEK = ModelFamilyConfig(
    family=ModelFamily.DEEPSEEK,
    provider=Provider.DEEPSEEK,
    version_default="4.0",
    variant_default="flash",
    variant_priority_default=(0,),
    patterns=[
        # 版本号命名（V4 起开放给 API 调用） / Version-numbered naming (open to API since V4)
        "deepseek-v{major:d}.{minor:d}-{variant:variant}",
        "deepseek-v{major:d}.{minor:d}",
        "deepseek-v{major:d}-{variant:variant}",
        "deepseek-v{major:d}",
        # 兼容别名 / Legacy aliases
        "deepseek-chat-{suffix}",
        "deepseek-chat",
        "deepseek-reasoner-{suffix}",
        "deepseek-reasoner",
    ],
    capabilities=_V4_CAPABILITIES,
    specific_models={
        # 当前旗舰：deepseek-v4-flash / Current flagship: deepseek-v4-flash
        "deepseek-v4-flash": SpecificModelConfig(
            version_default="4.0",
            variant_default="flash",
            variant_priority=(0,),
            capabilities=_V4_CAPABILITIES,
            patterns=[
                "deepseek-v4-flash",
            ],
        ),
        # 高阶版：deepseek-v4-pro / Professional tier: deepseek-v4-pro
        "deepseek-v4-pro": SpecificModelConfig(
            version_default="4.0",
            variant_default="pro",
            variant_priority=(4,),
            capabilities=_V4_CAPABILITIES,
            patterns=[
                "deepseek-v4-pro",
            ],
        ),
        # 兼容别名：deepseek-chat → v4-flash 非思考模式
        # Legacy alias: deepseek-chat → v4-flash non-thinking mode
        "deepseek-chat": SpecificModelConfig(
            version_default="4.0",
            variant_default="chat",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=False,
                supports_function_calling=True,
                supports_streaming=True,
                supports_json_outputs=True,
                supports_structured_outputs=False,
                max_tokens=384_000,
                context_window=1_000_000,
            ),
            patterns=[
                "deepseek-chat-{suffix}",
                "deepseek-chat",
            ],
        ),
        # 兼容别名：deepseek-reasoner → v4-flash 思考模式
        # Legacy alias: deepseek-reasoner → v4-flash thinking mode
        "deepseek-reasoner": SpecificModelConfig(
            version_default="4.0",
            variant_default="reasoner",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_json_outputs=True,
                supports_structured_outputs=False,
                max_tokens=384_000,
                context_window=1_000_000,
            ),
            patterns=[
                "deepseek-reasoner-{suffix}",
                "deepseek-reasoner",
            ],
        ),
    },
)
