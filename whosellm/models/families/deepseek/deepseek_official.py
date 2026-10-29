# filename: deepseek_official.py
# @Time    : 2025/11/9 15:57
# @Author  : Cascade AI
"""
DeepSeek 官方模型家族配置 / DeepSeek official model family configuration

当前线上（2026-09-28 实探 api.deepseek.com 确认）/ Currently serving:
  正式名 deepseek-flash  —— 模型版本 DeepSeek-V4.1-Flash，原生多模态视觉理解
  正式名 deepseek-v4-pro —— 模型版本 DeepSeek-V4-Pro-0813，纯文本（无图像输入）
  Canonical names: deepseek-flash (DeepSeek-V4.1-Flash, native multimodal) and
  deepseek-v4-pro (DeepSeek-V4-Pro-0813, text-only).

兼容路由（官方措辞为"暂时"）/ Compatibility routing (officially "temporary"):
  deepseek-v4-flash / deepseek-v4-flash-vision-exp / deepseek-chat / deepseek-reasoner
  的请求目前均由 deepseek-flash 承接（响应 model 字段回显 deepseek-flash，实探 2026-09-28）。
  这些旧名保留 4.0 的代次解析，但能力按当前实际服务模型标注：版本轴 = 名字血统，
  能力轴 = 端点现状。官方撤销路由后需回改，见 tests/models/families/test_deepseek.py::TestDeepSeekRouting。
  Requests under these legacy names are currently served by deepseek-flash (the response
  "model" field echoes deepseek-flash). Versions still parse from the name (4.0), while
  capabilities follow the actually serving model; the routing is temporary per the vendor.

来源 / Sources:
  https://api-docs.deepseek.com/zh-cn/updates/（2026-09-10 DeepSeek-V4.1-Flash 发布）
  https://api-docs.deepseek.com/zh-cn/quick_start/pricing
  https://api-docs.deepseek.com/zh-cn/guides/vision（单请求最多 600 张图）
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

# DeepSeek 有两个相关 surface：
# - DEEPSEEK（Chat Completions）：tool 消息 content 为字符串，不能携带媒体；
# - DEEPSEEK_RESPONSES（Responses）：官方明确 input_image 可出现在
#   function_call_output 的 output 中，deepseek-flash 会真正处理图片。
# DeepSeek has two relevant surfaces:
# - DEEPSEEK (Chat Completions): tool message content is a string, so no media;
# - DEEPSEEK_RESPONSES: input_image may appear in function_call_output output, and
#   deepseek-flash genuinely processes image blocks.
#
# 来源 / Sources（抓取日期 / fetched 2026-10-29）:
# - https://api-docs.deepseek.com/api/create-chat-completion
# - https://api-docs.deepseek.com/zh-cn/guides/responses_api
# - https://api-docs.deepseek.com/zh-cn/guides/vision
#
# DEEPSEEK_RESPONSES 的 image 登记为**文档依据**（官方 Responses 指南明确 input_image 可出现在
# function_call_output），未做 function_call_output 探针；2026-10-29 探针只覆盖 user 消息。
# The DEEPSEEK_RESPONSES image entry is DOCUMENTATION-BASED (the official Responses guide
# explicitly allows input_image in function_call_output); it was not probed via
# function_call_output -- the 2026-10-29 probe covered user messages only.
#
# PDF / document：明确不支持。实测 2026-10-29（TFROB-990 探针，owner 授权）：
#   Responses input_file 传 PDF（data URL）时请求被接受（无 4xx），但 PDF 内容未进入模型
#   （input_tokens=23，模型回复看不到 PDF）——静默不支持。内核应先转成图片再发送。
#   因此 supported_document_mime_type 保持空列表、max_pdf_* 保持 None，工具结果不登记 document。
# PDF / document: explicitly unsupported. 2026-10-29 probe (TFROB-990, owner-approved):
#   a Responses input_file PDF (data URL) was accepted without a 4xx, but the content never
#   reached the model (input_tokens=23; the model replied it could not see the PDF) -- a
#   silent drop. Convert PDFs to images before sending. supported_document_mime_type stays
#   empty, max_pdf_* stay None, and document is not registered for tool results.
# 可读图的 flash 系：Chat Completions 工具结果仍为 text-only，Responses 工具结果可原生承载 image
# Vision-capable flash line: Chat Completions tool results stay text-only; Responses tool
# results natively carry images
_DEEPSEEK_VISION_TOOL_RESULT_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.DEEPSEEK: ToolResultSurfaceCapability(modalities=()),
    LLMApiSurface.DEEPSEEK_RESPONSES: ToolResultSurfaceCapability(
        modalities=("image",),
        # 官方：内联单张图片最大 32 MiB（file_id 为 64 MiB）；这里取内联上限
        # Official: 32 MiB per inline image (64 MiB via file_id); the inline cap is used here
        max_inline_bytes=32 * 1024 * 1024,
        mime_types={"image": ["image/jpeg", "image/png", "image/gif", "image/webp"]},
    ),
}

# 纯文本模型 / 未知名字：两个 surface 都明确不支持媒体
# Text-only models / unknown names: both surfaces explicitly support no media
_DEEPSEEK_TEXT_ONLY_TOOL_RESULT_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.DEEPSEEK: ToolResultSurfaceCapability(modalities=()),
    LLMApiSurface.DEEPSEEK_RESPONSES: ToolResultSurfaceCapability(modalities=()),
}

# 单请求请求体上限 48 MiB（官方响应/图像理解文档；内联图片计入该预算）
# Per-request body cap: 48 MiB (official Responses/vision docs; inline images count toward it)
_DEEPSEEK_MAX_INLINE_MEDIA_BYTES = 48 * 1024 * 1024

# V4 系列保守基线 / Conservative baseline for the V4 series
# 仅用于按命名模式自动注册、且无 specific_models 覆盖的名字（如 deepseek-v3.2-exp 或未来代号）。
# 刻意不含视觉：家族内 deepseek-v4-pro 确认为纯文本（实探 2026-09-28 带图不报错、静默忽略并编造答案），
# 未知名字不应乐观标注多模态。
# Used only for pattern-registered names lacking a specific_models entry. Intentionally
# vision-less: v4-pro is text-only in this family (2026-09-28 probe: images silently
# ignored and hallucinated), so unknown names must not be optimistically multimodal.
_V4_CAPABILITIES = ModelCapabilities(
    tool_result_surfaces=_DEEPSEEK_TEXT_ONLY_TOOL_RESULT_SURFACES,
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

# DeepSeek-V4.1-Flash 能力（deepseek-flash 与当前路由到它的旧名共用）
# Capabilities of DeepSeek-V4.1-Flash (shared by deepseek-flash and the routed legacy names)
_V4_1_FLASH_CAPABILITIES = ModelCapabilities(
    tool_result_surfaces=_DEEPSEEK_VISION_TOOL_RESULT_SURFACES,
    supports_thinking=True,  # 默认开启（effort 默认 high）；thinking:{type:disabled} 可关闭
    supports_vision=True,  # 原生多模态视觉理解 / native multimodal vision
    supports_function_calling=True,
    supports_streaming=True,
    supports_json_outputs=True,
    supports_structured_outputs=False,
    max_tokens=384_000,
    context_window=1_000_000,
    # 官方文档：单请求最多 600 张图（api-docs.deepseek.com/zh-cn/guides/vision）
    # Per docs: up to 600 images per request
    media_count_limit=MediaCountLimit(per_type={"image": 600}),
    max_inline_media_bytes=_DEEPSEEK_MAX_INLINE_MEDIA_BYTES,
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
        # 无版本号的正式名 / Versionless canonical name
        "deepseek-flash",
        # 兼容别名 / Legacy aliases
        "deepseek-chat-{suffix}",
        "deepseek-chat",
        "deepseek-reasoner-{suffix}",
        "deepseek-reasoner",
    ],
    capabilities=_V4_CAPABILITIES,
    specific_models={
        # 官方当前正式名（2026-09-10 起）：不带版本号，模型版本 DeepSeek-V4.1-Flash
        # Canonical name since 2026-09-10: versionless, serves DeepSeek-V4.1-Flash
        # 旧 V4 Flash / V4 Flash Vision Exp 已下线，其模型名被路由到本模型
        # Legacy V4 Flash / V4 Flash Vision Exp are offline; their names route here
        "deepseek-flash": SpecificModelConfig(
            version_default="4.1",  # 名字无版本号，按官方模型版本标注 / versionless name tagged with official model version
            variant_default="flash",
            variant_priority=(0,),
            capabilities=_V4_1_FLASH_CAPABILITIES,
            patterns=[
                "deepseek-flash",
            ],
        ),
        # 兼容路由名：deepseek-v4-flash → 实际由 DeepSeek-V4.1-Flash 承接
        # Routed legacy name: served by DeepSeek-V4.1-Flash
        "deepseek-v4-flash": SpecificModelConfig(
            version_default="4.0",
            variant_default="flash",
            variant_priority=(0,),
            capabilities=_V4_1_FLASH_CAPABILITIES,
            patterns=[
                "deepseek-v4-flash",
            ],
        ),
        # 高阶版：deepseek-v4-pro，实探确认未被路由，仍是 DeepSeek-V4-Pro-0813
        # Professional tier: deepseek-v4-pro is NOT routed — still DeepSeek-V4-Pro-0813
        # 无图像输入：带图请求不报错但会静默忽略图片并编造答案（实探 2026-09-28），
        # 因此 supports_vision 必须为 False，由调用方阻止发图
        # No image input: image requests do not error out — the image is silently ignored
        # and the answer is hallucinated (2026-09-28 probe); supports_vision must stay False
        # 来源 / Source: https://api-docs.deepseek.com/zh-cn/quick_start/pricing（图像理解 不支持）
        "deepseek-v4-pro": SpecificModelConfig(
            version_default="4.0",
            variant_default="pro",
            variant_priority=(4,),
            capabilities=_V4_CAPABILITIES,
            patterns=[
                "deepseek-v4-pro",
            ],
        ),
        # 兼容路由名：deepseek-v4-flash-vision-exp → 实际由 DeepSeek-V4.1-Flash 承接
        # Routed legacy name: served by DeepSeek-V4.1-Flash
        # 官方原文："旧版本模型 V4 Flash 与 V4 Flash Vision Exp 现已下线……将被暂时路由到 V4.1 Flash"
        "deepseek-v4-flash-vision-exp": SpecificModelConfig(
            version_default="4.0",
            variant_default="flash-vision-exp",
            variant_priority=(0,),
            capabilities=_V4_1_FLASH_CAPABILITIES,
            patterns=[
                "deepseek-v4-flash-vision-exp",
            ],
        ),
        # 兼容别名：deepseek-chat → 当前路由到 deepseek-flash 的非思考模式
        # Legacy alias: deepseek-chat → non-thinking mode of the currently served flash
        # 实探 2026-09-28：默认非思考，但传 thinking:{type:enabled} 仍可思考；
        # 这里沿用"别名=模式"的既有建模，按默认模式标注 supports_thinking=False
        # Probe: non-thinking by default, yet thinking can be enabled on request; the
        # existing "alias = mode" modeling is kept, so supports_thinking follows the default
        "deepseek-chat": SpecificModelConfig(
            version_default="4.0",
            variant_default="chat",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DEEPSEEK_VISION_TOOL_RESULT_SURFACES,
                supports_thinking=False,
                supports_vision=True,  # 路由到 deepseek-flash，可读图 / routed to deepseek-flash, sees images
                supports_function_calling=True,
                supports_streaming=True,
                supports_json_outputs=True,
                supports_structured_outputs=False,
                max_tokens=384_000,
                context_window=1_000_000,
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
                max_inline_media_bytes=_DEEPSEEK_MAX_INLINE_MEDIA_BYTES,
            ),
            patterns=[
                "deepseek-chat-{suffix}",
                "deepseek-chat",
            ],
        ),
        # 兼容别名：deepseek-reasoner → 当前路由到 deepseek-flash 的思考模式
        # Legacy alias: deepseek-reasoner → thinking mode of the currently served flash
        "deepseek-reasoner": SpecificModelConfig(
            version_default="4.0",
            variant_default="reasoner",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_DEEPSEEK_VISION_TOOL_RESULT_SURFACES,
                supports_thinking=True,
                supports_vision=True,  # 路由到 deepseek-flash，可读图 / routed to deepseek-flash, sees images
                supports_function_calling=True,
                supports_streaming=True,
                supports_json_outputs=True,
                supports_structured_outputs=False,
                max_tokens=384_000,
                context_window=1_000_000,
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
                max_inline_media_bytes=_DEEPSEEK_MAX_INLINE_MEDIA_BYTES,
            ),
            patterns=[
                "deepseek-reasoner-{suffix}",
                "deepseek-reasoner",
            ],
        ),
    },
)
