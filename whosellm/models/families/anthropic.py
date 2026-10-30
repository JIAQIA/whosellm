# filename: anthropic.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Anthropic 模型家族配置 / Anthropic model family configurations
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
# Claude 系列 / Claude Series
# ==========================================================================

# Claude Messages 的工具结果能力（Claude 4.x / 5 系）
# Tool-result capability for the Claude Messages surface (Claude 4.x / 5)
#
# 来源 / Sources（抓取日期 / fetched 2026-10-29）:
# - tool_result content blocks may use text / image / document / search_result:
#   https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
# - PDF support (models, 128 MB request size, 600 pages / 100 pages under 1M ctx):
#   https://platform.claude.com/docs/en/build-with-claude/pdf-support
# - Image formats (JPEG / PNG / GIF / WebP):
#   https://platform.claude.com/docs/en/build-with-claude/vision
# 数据性质 / Data status: 官方文档核实，未逐模型调用 API 实测（保守登记）。
# Verified against official docs; not API-probed per model (conservative).
_CLAUDE_TOOL_RESULT_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.CLAUDE_MESSAGES: ToolResultSurfaceCapability(
        modalities=("image", "document"),
        mime_types={
            "image": ["image/jpeg", "image/png", "image/gif", "image/webp"],
            "document": ["application/pdf"],
        },
    ),
}

# 请求体上限核对（2026-10-30，官方 API overview#request-size-limits）：
#   第一方 Claude API 的 Messages / Token Counting = 128 MB；
#   Sessions / Agents / Environments = 32 MB；
#   Partner：Bedrock 20 MB、Google Cloud（Google managed）30 MB、
#   Claude Platform on AWS / Google Cloud（Anthropic managed）/ Microsoft Foundry 32 MB。
#   本库 Provider.ANTHROPIC 指第一方 API，因此 128 MB 正确；32 MB 不是 Messages API 的上限。
# Request-size verification (2026-10-30, official API overview#request-size-limits):
#   first-party Messages / Token Counting = 128 MB; Sessions/Agents/Environments = 32 MB;
#   partners: Bedrock 20 MB, Google Cloud (Google managed) 30 MB, AWS/Anthropic-managed
#   Google Cloud/Foundry 32 MB. Provider.ANTHROPIC is the first-party API, so 128 MB is
#   correct; 32 MB is NOT the Messages API limit.
#
# 单张图片：第一方文档未公布按字节的单图上限，只公布单图 8000×8000 px 与
# 100/600 张每请求；Bedrock / Google Cloud（Google managed）注明单图 5 MB（base64）。
# 因此 max_image_size_mb 保持 None（未声明）。
# Per-image bytes: first-party docs publish no byte cap, only 8000x8000 px and the
# 100/600 images-per-request limits; Bedrock / Google-managed Google Cloud note 5 MB
# per base64 image. max_image_size_mb therefore stays None (undeclared).
#
# PDF 上限（model 级）。官方只公布“整个请求 payload 128 MB”和“每请求 600/100 页”，
# 没有单文件大小上限；因此 max_pdf_size_mb 留 None（未知），128 MB 登记到请求级的
# max_inline_media_bytes。base64 膨胀由调用方按编码后大小自行计算。
# PDF limits (model level). The docs publish a 128 MB ENTIRE-request payload cap and a
# per-request page cap (600/100), but no per-file size cap. max_pdf_size_mb is therefore
# None (unknown); 128 MB goes to the request-level max_inline_media_bytes. Callers
# compute base64 expansion from the encoded size.
_CLAUDE_PDF_LIMITS_1M: dict[str, Any] = {
    "max_pdf_pages": 600,
    "supported_document_mime_type": ["application/pdf"],
    "max_inline_media_bytes": 128_000_000,
}
_CLAUDE_PDF_LIMITS_200K: dict[str, Any] = {
    "max_pdf_pages": 100,
    "supported_document_mime_type": ["application/pdf"],
    "max_inline_media_bytes": 128_000_000,
}

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
        # 200k 上下文模型：官方上限 100 张/请求；1M 模型为 600（见各 specific_models）
        # 200k-context models: 100 images/request per docs; 1M models: 600 (see specific_models)
        media_count_limit=MediaCountLimit(per_type={"image": 100}),
    ),
    specific_models={
        # Claude Opus 5.5（2026-09-22 发布，当前最新）：Fable 5.1 级性能，成本低约 40%
        # Claude Opus 5.5 (released 2026-09-22, latest): Fable 5.1-class work at ~40% lower cost
        # 规格：1M ctx（默认且最大）/ 128K out；adaptive thinking 常开且不可关闭，
        # effort 可配 low/medium/high/xhigh/max（默认 medium，低于 Opus 5 的 high）
        # Specs: 1M ctx (default & max) / 128K out; adaptive thinking always on and
        # cannot be disabled; effort low→max (default medium, down from Opus 5's high)
        # 来源 / Source: https://platform.claude.com/docs/en/release-notes/overview
        "claude-opus-5-5": SpecificModelConfig(
            version_default="5.5",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 思考默认开启且不可关闭 / thinking on by default, cannot be disabled
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "claude-opus-5-5-{snapshot:snapshot}",
                "claude-opus-5-5",
                "claude-opus-5-5@{snapshot:snapshot}",
            ],
        ),
        # Mythos-class（2026-06-09 发布）：全新顶级层级，优先级高于 opus
        # Mythos-class (released 2026-06-09): new top tier, ranks above opus
        # Fable 5 为公开版，Mythos 5 为 Glasswing 受邀版（能力相同，去掉安全分类器）
        "claude-fable-5": SpecificModelConfig(
            version_default="5.0",
            variant_default="fable",
            variant_priority=(6,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 自适应思考常开 / adaptive thinking always on
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 自适应思考常开 / adaptive thinking always on
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "claude-mythos-5-{snapshot:snapshot}",
                "claude-mythos-5",
                "claude-mythos-5@{snapshot:snapshot}",
            ],
        ),
        # Claude Fable 5.1（2026-09-01 发布，当前最新）：Fable 5 的扩展版，价格不变
        # Claude Fable 5.1 (released 2026-09-01, latest): extends Fable 5 at same prices
        # 规格同 Fable 5：1M ctx / 128K out，adaptive thinking 常开，default effort=high
        # 来源 / Source: https://platform.claude.com/docs/en/models/fable-5-1/overview
        "claude-fable-5-1": SpecificModelConfig(
            version_default="5.1",
            variant_default="fable",
            variant_priority=(6,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 自适应思考常开 / adaptive thinking always on
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "claude-fable-5-1-{snapshot:snapshot}",
                "claude-fable-5-1",
                "claude-fable-5-1@{snapshot:snapshot}",
            ],
        ),
        # Claude Mythos 5.1（2026-09-01 发布，Glasswing 受邀版）：与 Fable 5.1 同规格同价格
        # Claude Mythos 5.1 (released 2026-09-01, Glasswing invite-only): same specs & pricing as Fable 5.1
        "claude-mythos-5-1": SpecificModelConfig(
            version_default="5.1",
            variant_default="mythos",
            variant_priority=(7,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 自适应思考常开 / adaptive thinking always on
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "claude-mythos-5-1-{snapshot:snapshot}",
                "claude-mythos-5-1",
                "claude-mythos-5-1@{snapshot:snapshot}",
            ],
        ),
        # Claude 5 代（2026-06-30 Sonnet 5 / 2026-07-24 Opus 5 GA）：
        # adaptive thinking 默认开启，1M 上下文（默认且最大）/ 128K 最大输出
        # Claude 5 generation (Sonnet 5 GA 2026-06-30 / Opus 5 GA 2026-07-24):
        # adaptive thinking on by default, 1M context (default & max) / 128K max output
        "claude-opus-5": SpecificModelConfig(
            version_default="5.0",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 思考默认开启（adaptive）/ thinking on by default (adaptive)
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "claude-opus-5-{snapshot:snapshot}",
                "claude-opus-5",
                "claude-opus-5@{snapshot:snapshot}",
            ],
        ),
        "claude-sonnet-5": SpecificModelConfig(
            version_default="5.0",
            variant_default="sonnet",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,  # 自适应思考默认开启 / adaptive thinking on by default
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
            ),
            patterns=[
                "claude-sonnet-5-{snapshot:snapshot}",
                "claude-sonnet-5",
                "claude-sonnet-5@{snapshot:snapshot}",
            ],
        ),
        "claude-opus-4-8": SpecificModelConfig(
            version_default="4.8",
            variant_default="opus",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=128000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_1M,
                supports_pdf=True,
                supports_vision=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_computer_use=True,
                max_tokens=64000,
                context_window=1000000,
                # 官方上限：1M 上下文模型最多 600 张图片/请求（https://docs.anthropic.com/en/docs/build-with-claude/vision）
                # Per docs: up to 600 images per request for 1M-context models
                media_count_limit=MediaCountLimit(per_type={"image": 600}),
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_200K,
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_200K,
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_200K,
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_200K,
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_200K,
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
                tool_result_surfaces=_CLAUDE_TOOL_RESULT_SURFACES,
                **_CLAUDE_PDF_LIMITS_200K,
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
