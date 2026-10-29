# filename: alibaba.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
阿里巴巴模型家族配置 / Alibaba model family configurations
"""

from whosellm.capabilities import (
    LLMApiSurface,
    MediaCountLimit,
    ModelCapabilities,
    ToolResultSurfaceCapability,
)
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# 官方 API 参考将 tool 消息 content 定义为字符串，工具结果不能携带媒体。
# The official API reference defines tool-message content as a string, so tool
# results cannot carry media.
# 来源 / Source（抓取日期 / fetched 2026-10-29）:
# - Aliyun: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions
_DASHSCOPE_TOOL_RESULT_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.DASHSCOPE: ToolResultSurfaceCapability(modalities=()),
}

# ============================================================================
# Qwen 系列 / Qwen Series
# ============================================================================

QWEN = ModelFamilyConfig(
    family=ModelFamily.QWEN,
    provider=Provider.ALIBABA,
    version_default="1.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "qwen{version:d}-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "qwen{version:d}-{variant:variant}",
        "qwen-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "qwen-{variant:variant}",
        # Ollama 短格式 / Ollama short format (e.g. qwen2.5-coder, qwen2.5, qwen2, qwen3)
        "qwen{major:d}.{minor:d}-{variant:variant}",
        "qwen{major:d}.{minor:d}",
        "qwen{version:d}",
    ],
    capabilities=ModelCapabilities(
        tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
        supports_function_calling=True,
        supports_streaming=True,
        supports_vision=False,  # 默认关闭多模态能力 / Default multimodal capabilities disabled
        max_tokens=8192,
        context_window=32000,
    ),
    specific_models={
        "qwen3-max": SpecificModelConfig(
            version_default="3",
            variant_default="max",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=256000,
            ),
            patterns=[
                "qwen3-max-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-max",
            ],
        ),
        "qwen3-max-preview": SpecificModelConfig(
            version_default="3",
            variant_default="max-preview",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=64000,
                context_window=256000,
            ),
            patterns=[
                "qwen3-max-preview-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-max-preview",
            ],
        ),
        "qwen3-coder-plus": SpecificModelConfig(
            version_default="3",
            variant_default="coder-plus",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_fine_tuning=True,
                max_tokens=64000,
                context_window=1_000_000,
            ),
            patterns=[
                "qwen3-coder-plus-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-coder-plus",
            ],
        ),
        "qwen-image-plus": SpecificModelConfig(
            version_default="1.0",
            variant_default="image-plus",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_streaming=False,
                supports_structured_outputs=False,
                supports_function_calling=False,
                supports_vision=True,
                supports_image_base64=True,
                supported_image_mime_type=[
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                ],
                max_tokens=None,
                context_window=None,
            ),
            patterns=[
                "qwen-image-plus-{year:4d}-{month:2d}-{day:2d}",
                "qwen-image-plus",
            ],
        ),
        "qwen-image": SpecificModelConfig(
            version_default="1.0",
            variant_default="image",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_streaming=False,
                supports_structured_outputs=False,
                supports_function_calling=False,
                supports_vision=True,
                supports_image_base64=True,
                supported_image_mime_type=[
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                ],
                max_tokens=None,
                context_window=None,
            ),
            patterns=[
                "qwen-image-{year:4d}-{month:2d}-{day:2d}",
                "qwen-image",
            ],
        ),
        "qwen3-vl-plus": SpecificModelConfig(
            version_default="3",
            variant_default="vl-plus",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=256000,
                # 官方：公网 URL/本地路径最多 256 张；Base64 250 张（help.aliyun.com/zh/model-studio/vision）
                # Per docs: 256 images via URL/local path; 250 via base64
                media_count_limit=MediaCountLimit(per_type={"image": 256}),
            ),
            patterns=[
                "qwen3-vl-plus-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-plus",
            ],
        ),
        "qwen3-vl-235b-a22b-thinking": SpecificModelConfig(
            version_default="3",
            variant_default="vl-235b-a22b-thinking",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=128000,
            ),
            patterns=[
                "qwen3-vl-235b-a22b-thinking-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-235b-a22b-thinking",
            ],
        ),
        "qwen3-vl-32b-thinking": SpecificModelConfig(
            version_default="3",
            variant_default="vl-32b-thinking",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=128000,
            ),
            patterns=[
                "qwen3-vl-32b-thinking-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-32b-thinking",
            ],
        ),
        "qwen3-vl-32b-instruct": SpecificModelConfig(
            version_default="3",
            variant_default="vl-32b-instruct",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=128000,
            ),
            patterns=[
                "qwen3-vl-32b-instruct-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-32b-instruct",
            ],
        ),
        "qwen3-vl-flash": SpecificModelConfig(
            version_default="3",
            variant_default="vl-flash",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=256000,
                # 官方：公网 URL/本地路径最多 256 张；Base64 250 张（help.aliyun.com/zh/model-studio/vision）
                # Per docs: 256 images via URL/local path; 250 via base64
                media_count_limit=MediaCountLimit(per_type={"image": 256}),
            ),
            patterns=[
                "qwen3-vl-flash-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-flash",
            ],
        ),
        "qwen3-vl-30b-a3b-instruct": SpecificModelConfig(
            version_default="3",
            variant_default="vl-30b-a3b-instruct",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=128000,
            ),
            patterns=[
                "qwen3-vl-30b-a3b-instruct-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-30b-a3b-instruct",
            ],
        ),
        "qwen3-vl-8b-thinking": SpecificModelConfig(
            version_default="3",
            variant_default="vl-8b-thinking",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=128000,
            ),
            patterns=[
                "qwen3-vl-8b-thinking-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-8b-thinking",
            ],
        ),
        "qwen3-vl-8b-instruct": SpecificModelConfig(
            version_default="3",
            variant_default="vl-8b-instruct",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_vision=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                max_tokens=32000,
                context_window=128000,
            ),
            patterns=[
                "qwen3-vl-8b-instruct-{year:4d}-{month:2d}-{day:2d}",
                "qwen3-vl-8b-instruct",
            ],
        ),
        "qwen-plus": SpecificModelConfig(
            version_default="1.0",
            variant_default="plus",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_vision=False,  # 仅支持文本输入输出 / Text input/output only
                max_tokens=8192,
                context_window=32000,
            ),
            patterns=[
                "qwen-plus-{year:4d}-{month:2d}-{day:2d}",
                "qwen-plus",
            ],
        ),
        "qwen-flash": SpecificModelConfig(
            version_default="1.0",
            variant_default="flash",
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DASHSCOPE_TOOL_RESULT_SURFACES,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_vision=False,  # 仅支持文本输入输出 / Text input/output only
                max_tokens=8192,
                context_window=32000,
            ),
            patterns=[
                "qwen-flash-{year:4d}-{month:2d}-{day:2d}",
                "qwen-flash",
            ],
        ),
    },
)
