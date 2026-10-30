# filename: gemini.py
# @Time    : 2025/12/12 13:17
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Google Gemini 模型家族配置 / Google Gemini model family configurations
"""

from typing import Any

from whosellm.capabilities import (
    LLMApiSurface,
    MediaCountLimit,
    ModelCapabilities,
    ToolResultSurfaceCapability,
)
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ==========================================================================
# Gemini 系列 / Gemini Series
# 注意Image系列模型。当前虽然标记为不支持thinking，在实际调试中发现 image 系列也会有思考内容产生，但需要注意接口并不支持配置thinking行为，
# 因此权当不支持处理
# ==========================================================================

# --------------------------------------------------------------------------
# 工具结果能力 / Tool-result capability（按 API surface 登记）
#
# 官方：Gemini 3 系模型允许在 function response 中携带多模态内容。
# 2026-10-29 实测（owner 授权，共 10 次调用；实测模型 gemini-3-flash-preview）：
#   functionResponse.parts 用 inlineData 分别带 image/png、application/pdf、
#   audio/wav、video/mp4，四次请求均正常完成，模型回答分别为「红色」「红色」「有声音」「红色」。
#   实测报告：/Users/jqq/.turingfocus/reports/gemini-function-response-media-probe-20261029-230532.json
# 其他 3.x 型号（pro 等）未逐一实测；官方把多模态 function response 定义为 Gemini 3 系列能力，
# 因此按系列一致性登记，并在此保留实测覆盖范围。
# mime_types 只登记实测覆盖的格式；其他格式保持未声明，由调用方保守处理。
#
# Gemini 2.x：实测 gemini-2.5-flash 在 function response 带 image/png 时返回 HTTP 200、
# 请求正常完成，但模型回答「无法看到或分析图片内容」——属于静默忽略，不是 400。
# 因此 2.x 仍显式标为不支持（空元组）；supports_vision 保持 True（用户消息能力不受影响）。
#
# 注意：本登记以 legacy GenerateContent 的 functionResponse.parts 实测为准。
# Interactions API 的 FunctionResultStep.result 官方 schema 仍只列 ImageContent / TextContent；
# 若内核走 Interactions API 的 function_result，需要另行实测/裁决。
# This entry is based on the legacy GenerateContent functionResponse.parts probe. The
# Interactions API FunctionResultStep.result schema still lists only ImageContent/TextContent;
# a separate probe is needed if the kernel uses Interactions function_result.
#
# 来源 / Sources（抓取日期 / fetched 2026-10-29）:
# - Multimodal function responses (Gemini 3 series):
#   https://ai.google.dev/gemini-api/docs/function-calling
# - Probe report (2026-10-29, owner-approved, 10 calls):
#   /Users/jqq/.turingfocus/reports/gemini-function-response-media-probe-20261029-230532.json
# - PDF: up to 1,000 pages; inline 50 MB for PDFs, 100 MB per payload:
#   https://ai.google.dev/gemini-api/docs/document-processing
#   https://ai.google.dev/gemini-api/docs/generate-content/file-input-methods
# 数据性质 / Data status: Gemini 3 image/document/audio/video 为实测 + 官方文档；
# 其他 3.x 型号按系列文档登记、未逐一实测。2.x 静默忽略为实测。
# Gemini 3 modalities are probe-backed + official-doc-backed; other 3.x models are
# registered by series consistency, not individually probed. Gemini 2.x silent-drop is probed.
_GEMINI_3_TOOL_RESULT_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.GEMINI: ToolResultSurfaceCapability(
        modalities=("image", "document", "audio", "video"),
        mime_types={
            "image": [
                "image/png",
                "image/jpeg",
                "image/webp",
                "image/heic",
                "image/heif",
                "image/gif",
                "image/bmp",
                "image/tiff",
            ],
            "document": ["application/pdf"],
            # 仅登记实测覆盖的格式；其余格式未声明 / only probed formats are declared
            "audio": ["audio/wav"],
            "video": ["video/mp4"],
        },
    ),
}
_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    # 空元组 = 明确不支持。实测 2.x 请求 HTTP 200 但静默忽略媒体（2026-10-29, gemini-2.5-flash）。
    # Empty tuple = explicitly unsupported. Probe: 2.x returns HTTP 200 but silently ignores
    # media (2026-10-29, gemini-2.5-flash).
    LLMApiSurface.GEMINI: ToolResultSurfaceCapability(modalities=()),
}
_GEMINI_PDF_KWARGS: dict[str, Any] = {
    # 官方只公布“每请求 inline payload 100 MB（PDF 合计 50 MB）”，没有单文件大小上限；
    # 因此 max_pdf_size_mb 留 None（未知）。通用媒体上限登记到 max_inline_media_bytes，
    # PDF 合计上限登记到 max_inline_file_bytes。
    # The docs publish a per-request inline payload cap (100 MB; 50 MB combined for PDFs),
    # not a per-file cap, so max_pdf_size_mb stays None (unknown). The general media cap
    # goes to max_inline_media_bytes; the combined PDF cap goes to max_inline_file_bytes.
    "max_pdf_pages": 1000,  # 单请求最多 1000 页 / up to 1,000 pages per request
    "supported_document_mime_type": ["application/pdf"],
    "max_inline_file_bytes": 50_000_000,  # 请求内 PDF 合计 50 MB / combined PDFs per request
}
# 单请求内联媒体总预算（官方通用 inline payload 上限 100 MB）
# Per-request inline media budget (official general inline payload cap: 100 MB)
_GEMINI_MAX_INLINE_MEDIA_BYTES = 100_000_000

# Gemini 官方支持的音频输入 MIME 类型（2026-10-30 抓取）
# Officially supported audio input MIME types (fetched 2026-10-30)
# 来源 / Source: https://ai.google.dev/gemini-api/docs/audio#supported-audio-formats
_GEMINI_AUDIO_MIME_TYPES: list[str] = [
    "audio/wav",
    "audio/mp3",
    "audio/aiff",
    "audio/aac",
    "audio/ogg",
    "audio/flac",
    "audio/mpeg",
    "audio/m4a",
    "audio/l16",
    "audio/opus",
    "audio/alaw",
    "audio/mulaw",
    "audio/webm",
]

GEMINI = ModelFamilyConfig(
    family=ModelFamily.GEMINI,
    provider=Provider.GOOGLE,
    version_default="3.0",
    variant_default="flash",
    variant_priority_default=(1,),  # flash 的默认优先级 / default priority for flash
    patterns=[
        "gemini-{major:d}.{minor:d}-{variant}",
        "gemini-{major:d}.{minor:d}-{variant}-{suffix}",
        "gemini-{major:d}.{minor:d}-{variant}-preview-{date}",
        "gemini-{major:d}.{minor:d}-{variant}-preview",
        "gemini-{major:d}.{minor:d}-{variant}-image",
        "gemini-{major:d}.{minor:d}-{variant}-lite",
        "gemini-{major:d}.{minor:d}-{variant}-live",
        "gemini-{major:d}.{minor:d}-{variant}-native-audio-preview-{date}",
        "gemini-{major:d}.{minor:d}-preview-tts",
        "gemini-{major:d}.{minor:d}-preview-{date}",
        "gemini-{major:d}.{minor:d}-preview",
        "gemini-{major:d}.{minor:d}",
        "gemini-{variant}",
        "gemini-{variant}-preview",
        "gemini-{variant}-latest",
    ],
    capabilities=ModelCapabilities(
        supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
        supports_vision=True,
        supports_audio=True,
        supports_video=True,
        supports_pdf=True,
        supports_thinking=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_json_outputs=True,
        supports_web_search=True,
        supports_file_search=True,
        supports_code_interpreter=True,
        max_tokens=65536,
        context_window=1048576,
    ),
    specific_models={
        # Gemini 3 Pro 系列 - 最智能的多模态模型
        # ⚠️ gemini-3-pro / gemini-3-pro-preview 已于 2026-03-09 关停，请迁移至 gemini-3.1-pro-preview
        "gemini-3-pro": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3-pro"],
        ),
        "gemini-3-pro-preview": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3-pro-preview"],
        ),
        # ⚠️ gemini-3-pro-image-preview 已于 2026-06-25 关停，请迁移至 gemini-3-pro-image
        "gemini-3-pro-image-preview": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro-image",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                max_tokens=32768,
                context_window=65536,
            ),
            patterns=["gemini-3-pro-image-preview"],
        ),
        # Nano Banana Pro GA 版：2026-05-28 发布，替代已关停的 gemini-3-pro-image-preview
        # 官方规格：输入 Image/Text，输出 Image/Text；ctx 65536 / max 32768；
        # image_generation ✓、search grounding ✓、structured ✗、function calling ✗
        "gemini-3-pro-image": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro-image",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                supports_web_search=True,
                max_tokens=32768,
                context_window=65536,
            ),
            patterns=["gemini-3-pro-image"],
        ),
        # Gemini 2.5 Flash 系列 - 性价比最高的模型
        "gemini-2.5-flash": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash"],
        ),
        # ⚠️ gemini-2.5-flash-preview-09-2025 已于 2026-02-17 关停，官方建议迁移至 gemini-3.6-flash
        "gemini-2.5-flash-preview-09-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash-preview-09-2025"],
        ),
        # ⚠️ gemini-2.5-flash-image（Nano Banana）计划于 2026-10-02 关停，建议迁移至 gemini-3.1-flash-image（Nano Banana 2）
        "gemini-2.5-flash-image": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-image",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_pdf=False,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                max_tokens=32768,
                context_window=65536,
            ),
            patterns=["gemini-2.5-flash-image"],
        ),
        # ⚠️ gemini-2.5-flash-native-audio-preview-09-2025 已被 12-2025 版取代，
        # 官方当前 Live 旗舰为 gemini-2.5-flash-native-audio-preview-12-2025
        "gemini-2.5-flash-native-audio-preview-09-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-live",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_audio=True,
                supports_video=True,
                supports_pdf=False,
                supports_audio_generation=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_web_search=True,
                max_tokens=8192,
                context_window=131072,
            ),
            patterns=["gemini-2.5-flash-native-audio-preview-09-2025"],
        ),
        # 当前 Live API 旗舰（2.5 Flash Live 12-2025 版，官方规格卡 2026-08 采集）：
        # 输入 Audio/Video/Text，输出 Audio/Text；ctx 131072 / max 8192；
        # audio generation ✓、function calling ✓（支持异步）、search grounding ✓、thinking ✓
        "gemini-2.5-flash-native-audio-preview-12-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-live",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_audio=True,
                supports_video=True,
                supports_pdf=False,
                supports_audio_generation=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_web_search=True,
                max_tokens=8192,
                context_window=131072,
            ),
            patterns=["gemini-2.5-flash-native-audio-preview-12-2025"],
        ),
        "gemini-2.5-flash-preview-tts": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-tts",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_audio_generation=True,
                supports_pdf=False,
                supports_streaming=True,
                max_tokens=16384,
                context_window=8192,
            ),
            patterns=["gemini-2.5-flash-preview-tts"],
        ),
        # Gemini 2.5 Flash-Lite 系列 - 最快的模型
        "gemini-2.5-flash-lite": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash-lite"],
        ),
        # ⚠️ gemini-2.5-flash-lite-preview-09-2025 已于 2026-03-31 关停，官方建议迁移至 gemini-3.1-flash-lite
        "gemini-2.5-flash-lite-preview-09-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash-lite-preview-09-2025"],
        ),
        # Gemini 2.5 Pro 系列 - 高级思考模型
        "gemini-2.5-pro": SpecificModelConfig(
            version_default="2.5",
            variant_default="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-pro"],
        ),
        "gemini-2.5-pro-preview-tts": SpecificModelConfig(
            version_default="2.5",
            variant_default="pro-tts",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                supports_audio_generation=True,
                supports_streaming=True,
                max_tokens=16384,
                context_window=8192,
            ),
            patterns=["gemini-2.5-pro-preview-tts"],
        ),
        # gemini-3-flash-preview 是 gemini-3.5-flash 的 Preview 别名，官方建议迁移至 gemini-3.6-flash
        "gemini-3-flash-preview": SpecificModelConfig(
            version_default="3.0",
            variant_default="flash",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_streaming=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3-flash-preview"],
        ),
        # Gemini 3.5 / 3.6 / 3.7 Flash 系列（GA）- 2026 年 Flash 迭代主线
        # 官方规格（2026-08 采集）：输入 Text/Image/Video/Audio/PDF，输出 Text；
        # 1M 上下文 / 65536 输出；支持 thinking、结构化输出、代码执行、文件搜索、
        # 搜索接地、URL context（Computer use 为 Preview）
        "gemini-3.5-flash": SpecificModelConfig(
            version_default="3.5",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.5-flash"],
        ),
        # gemini-3.6-flash：2026-07-21 GA，擅长代码生成与智能体执行循环
        "gemini-3.6-flash": SpecificModelConfig(
            version_default="3.6",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.6-flash"],
        ),
        # gemini-3.7-flash：2026-08 GA；thinking 仅支持 low/medium/high（不支持 minimal）
        "gemini-3.7-flash": SpecificModelConfig(
            version_default="3.7",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
                # 官方文档：单请求最多 3600 张图片（https://ai.google.dev/gemini-api/docs/image-understanding）
                # Per docs: up to 3,600 image files per request
                media_count_limit=MediaCountLimit(per_type={"image": 3600}),
            ),
            patterns=["gemini-3.7-flash"],
        ),
        # gemini-3.8-flash：2026-09 GA，当前最新 Flash；thinking 仅 low/medium/high（不支持 minimal）
        # 文档标注 Computer use "Supported (Preview)"（与该系列 3.5-3.7 处理一致，未计入）
        "gemini-3.8-flash": SpecificModelConfig(
            version_default="3.8",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
                # 官方文档：单请求最多 3600 张图片（https://ai.google.dev/gemini-api/docs/image-understanding）
                # Per docs: up to 3,600 image files per request
                media_count_limit=MediaCountLimit(per_type={"image": 3600}),
            ),
            patterns=["gemini-3.8-flash"],
        ),
        # gemini-3.5-flash-lite：2026-07-21 GA，面向高吞吐子智能体与文档解析
        "gemini-3.5-flash-lite": SpecificModelConfig(
            version_default="3.5",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.5-flash-lite"],
        ),
        # Gemini 3.1 系列 / Gemini 3.1 Series
        # 注意：官方 API ID 使用点号格式 gemini-3.1-*（而非短横线 gemini-3-1-*）
        "gemini-3.1-pro-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_streaming=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            # gemini-3.1-pro-preview-customtools：面向 bash + 自定义工具的智能体端点
            patterns=["gemini-3.1-pro-preview", "gemini-3.1-pro-preview-customtools"],
        ),
        # ⚠️ gemini-3.1-flash-lite-preview 已于 2026-05-25 关停，GA 版为 gemini-3.1-flash-lite（计划 2027-05-07 关停）
        "gemini-3.1-flash-lite-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_streaming=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.1-flash-lite-preview"],
        ),
        # gemini-3.1-flash-lite：2026-05-07 GA（官方详情页未附规格卡，
        # 能力与 token 上限沿用其 preview 版官方公布值：1M ctx / 65536 out）
        "gemini-3.1-flash-lite": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.1-flash-lite"],
        ),
        # Nano Banana 2（GA）：2026-05-28 发布
        # 官方规格：输入 Text/Image/PDF，输出 Image/Text；ctx 131072 / max 32768；
        # image_generation ✓、search grounding ✓；caching/code execution/function calling/structured ✗
        "gemini-3.1-flash-image": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-image",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                **_GEMINI_PDF_KWARGS,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_pdf=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                supports_web_search=True,
                max_tokens=32768,
                context_window=131072,
            ),
            patterns=["gemini-3.1-flash-image"],
        ),
        # Nano Banana 2 Lite（GA）：仅 1K 分辨率、14 种宽高比
        # 官方规格：输入 Text/Image，输出 Image/Text；ctx 65536 / max 4096；
        # image_generation ✓、function calling ✓；search grounding/structured ✗
        "gemini-3.1-flash-lite-image": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-lite-image",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_tokens=4096,
                context_window=65536,
            ),
            patterns=["gemini-3.1-flash-lite-image"],
        ),
        # ==========================================================================
        # 实时/语音/视频特化模型（2026 新增）
        # ==========================================================================
        # Gemini 3.1 Flash Live：2026-03-11 发布的 A2A 实时对话模型
        # 官方详情页未附规格卡；ctx 取 Live API 官方约束（原生音频输出模型 128k），
        # max_tokens 参照官方指定的迁移源 gemini-2.5-flash-native-audio-preview-12-2025（8192）。
        # thinking 经 thinkingLevel 控制（minimal 默认）；function calling 仅同步（async 不支持）
        "gemini-3.1-flash-live-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-live",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_3_TOOL_RESULT_SURFACES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_audio=True,
                supports_video=True,
                supports_pdf=False,
                supports_audio_generation=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_web_search=True,
                max_tokens=8192,
                context_window=131072,
            ),
            patterns=["gemini-3.1-flash-live-preview"],
        ),
        # Gemini 3.1 Flash TTS：2026-04-13 发布，新增表现力音频标记
        # 官方规格：输入 Text，输出 Audio；ctx 8192 / max 16384；仅 audio generation
        "gemini-3.1-flash-tts-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-tts",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_audio_generation=True,
                supports_pdf=False,
                supports_thinking=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_tokens=16384,
                context_window=8192,
            ),
            patterns=["gemini-3.1-flash-tts-preview"],
        ),
        # Gemini 3.5 实时翻译：双向实时口语翻译，70+ 语言
        # 官方规格：输入 Audio(speech)，输出 Audio(翻译语音)+Text(转写)；
        # ctx 131072 / max 65536；仅 live API 与 audio generation
        "gemini-3.5-live-translate-preview": SpecificModelConfig(
            version_default="3.5",
            variant_default="live-translate",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_audio=True,
                supports_audio_generation=True,
                supports_thinking=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_tokens=65536,
                context_window=131072,
            ),
            patterns=["gemini-3.5-live-translate-preview"],
        ),
        # Gemini 3.5 Transcribe：2026-08 新发布的语音转写模型（85+ 语言，2026-09-04 采集）
        # 官方规格：输入 Audio（Unary ≤1h，启用 diarization/时间戳时 ≤30min；live ≤10min/次），
        # 输出 Text + Word annotations；官方无 token 上限说明，仅按音频时长限制；
        # thinking / function calling / structured outputs / caching / code execution 均不支持
        "gemini-3.5-transcribe": SpecificModelConfig(
            version_default="3.5",
            variant_default="transcribe",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_audio=True,
                supports_thinking=False,
                supports_function_calling=False,
                supports_streaming=True,  # gemini-3.5-transcribe-live 走 Live API / live endpoint
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_audio_duration_seconds=3600,  # Unary 上限 1 小时 / Unary up to 1 hour
            ),
            patterns=["gemini-3.5-transcribe-live", "gemini-3.5-transcribe"],
        ),
        # Gemini Omni Flash：对话式视频生成/编辑模型（走 Interactions API）
        # 官方规格：输入 Text/Image/Video（编辑/扩展 ≤10s），输出 Video（3-10s 360p/720p/1080p/4K 24FPS）；
        # ctx 1048576；输出为视频无 token 上限数据。
        # 官方版本说明（2026-09-04 采集）：Stable = gemini-omni-1.1-flash；Preview = gemini-omni-flash-preview；
        # gemini-omni-flash（总览页旧写法）也保留收录。注：官方未标注版本号，按家族默认 3.0 处理
        "gemini-omni-flash": SpecificModelConfig(
            version_default="3.0",
            variant_default="omni-flash",
            variant_priority=(6,),
            capabilities=ModelCapabilities(
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_video=True,
                supports_thinking=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                context_window=1048576,
            ),
            patterns=["gemini-omni-1.1-flash", "gemini-omni-flash", "gemini-omni-flash-preview"],
        ),
        # Gemini 2.0 Flash 系列 - 第二代主力模型
        # ⚠️ gemini-2.0-flash 已于 2026-06-01 关停，官方建议迁移至 gemini-3.6-flash
        "gemini-2.0-flash": SpecificModelConfig(
            version_default="2.0",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_code_interpreter=True,
                max_tokens=8192,
                context_window=1048576,
            ),
            patterns=["gemini-2.0-flash", "gemini-2.0-flash-001", "gemini-2.0-flash-exp"],
        ),
        "gemini-2.0-flash-preview-image-generation": SpecificModelConfig(
            version_default="2.0",
            variant_default="flash-image",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_thinking=False,
                supports_audio=False,
                supports_image_generation=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=True,
                max_tokens=8192,
                context_window=32768,
            ),
            patterns=["gemini-2.0-flash-preview-image-generation"],
        ),
        # Gemini 2.0 Flash-Lite 系列 - 第二代快速模型
        # ⚠️ gemini-2.0-flash-lite 已于 2026-06-01 关停，官方建议迁移至 gemini-3.1-flash-lite
        "gemini-2.0-flash-lite": SpecificModelConfig(
            version_default="2.0",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supported_audio_mime_type=_GEMINI_AUDIO_MIME_TYPES,
                tool_result_surfaces=_GEMINI_UNSUPPORTED_TOOL_RESULT_SURFACES,
                max_inline_media_bytes=_GEMINI_MAX_INLINE_MEDIA_BYTES,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                max_tokens=8192,
                context_window=1048576,
            ),
            patterns=["gemini-2.0-flash-lite", "gemini-2.0-flash-lite-001"],
        ),
    },
)
