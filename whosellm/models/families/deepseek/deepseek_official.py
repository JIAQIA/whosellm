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

from whosellm.capabilities import MediaCountLimit, ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# V4 系列保守基线 / Conservative baseline for the V4 series
# 仅用于按命名模式自动注册、且无 specific_models 覆盖的名字（如 deepseek-v3.2-exp 或未来代号）。
# 刻意不含视觉：家族内 deepseek-v4-pro 确认为纯文本（实探 2026-09-28 带图不报错、静默忽略并编造答案），
# 未知名字不应乐观标注多模态。
# Used only for pattern-registered names lacking a specific_models entry. Intentionally
# vision-less: v4-pro is text-only in this family (2026-09-28 probe: images silently
# ignored and hallucinated), so unknown names must not be optimistically multimodal.
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

# DeepSeek-V4.1-Flash 能力（deepseek-flash 与当前路由到它的旧名共用）
# Capabilities of DeepSeek-V4.1-Flash (shared by deepseek-flash and the routed legacy names)
_V4_1_FLASH_CAPABILITIES = ModelCapabilities(
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
                supports_thinking=False,
                supports_vision=True,  # 路由到 deepseek-flash，可读图 / routed to deepseek-flash, sees images
                supports_function_calling=True,
                supports_streaming=True,
                supports_json_outputs=True,
                supports_structured_outputs=False,
                max_tokens=384_000,
                context_window=1_000_000,
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
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
                supports_thinking=True,
                supports_vision=True,  # 路由到 deepseek-flash，可读图 / routed to deepseek-flash, sees images
                supports_function_calling=True,
                supports_streaming=True,
                supports_json_outputs=True,
                supports_structured_outputs=False,
                max_tokens=384_000,
                context_window=1_000_000,
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "deepseek-reasoner-{suffix}",
                "deepseek-reasoner",
            ],
        ),
    },
)
