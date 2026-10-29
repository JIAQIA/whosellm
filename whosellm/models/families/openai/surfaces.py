# filename: surfaces.py
# @Time    : 2026/10/29
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
OpenAI API surface 工具结果能力登记 / Tool-result capability data per OpenAI API surface

工具结果能力是 per-(provider × API-surface) 的，与具体模型无关：
- Chat Completions 的 tool 消息只允许 text content part，不能携带图片/文件；
- Responses 的 function_call_output.output 允许 input_text / input_image / input_file。

Tool-result capability is per-(provider × API surface), independent of the model:
- Chat Completions tool messages only allow text content parts;
- Responses function_call_output.output accepts input_text / input_image / input_file.

来源 / Sources（抓取日期 / fetched 2026-10-29）:
- Chat Completions tool message: only type `text` is supported
  https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
- Responses function_call_output: string or array of input_text / input_image / input_file
  https://developers.openai.com/api/reference/resources/responses/methods/create
- Image formats and request limits (up to 512 MB payload; 1,500 images/request)
  https://developers.openai.com/api/docs/guides/images-vision
- File inputs: PDF parsing on vision models; each file and the combined request under 50 MB
  https://developers.openai.com/api/docs/guides/file-inputs

数据性质 / Data status: 官方文档核实，未逐模型调用 API 实测（保守登记）。
OpenAI Responses 的 PDF 行为仅依据 OpenAI 官方文档，未使用 DeepSeek 探针结果外推。
Verified against official docs; not API-probed per model (conservative). OpenAI Responses
PDF behavior is based solely on OpenAI's own docs, not extrapolated from DeepSeek probes.
"""

from typing import Any

from whosellm.capabilities import LLMApiSurface, ToolResultSurfaceCapability

# Chat Completions：tool 消息明确不支持任何媒体（modalities 空元组 = 明确不支持）
# Chat Completions: tool messages explicitly support no media (empty tuple = explicit unsupported)
OPENAI_CHAT_ONLY_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.OPENAI_CHAT_COMPLETIONS: ToolResultSurfaceCapability(modalities=()),
}

# 具备视觉能力的模型：Chat Completions 仍为 text-only；Responses 可原生承载 image / document
# Vision-capable models: Chat Completions stays text-only; Responses natively carries image / document
OPENAI_MULTIMODAL_SURFACES: dict[LLMApiSurface, ToolResultSurfaceCapability] = {
    LLMApiSurface.OPENAI_CHAT_COMPLETIONS: ToolResultSurfaceCapability(modalities=()),
    LLMApiSurface.OPENAI_RESPONSES: ToolResultSurfaceCapability(
        modalities=("image", "document"),
        mime_types={
            "image": ["image/png", "image/jpeg", "image/webp", "image/gif"],
            # Responses 的 input_file 支持更多文档类型；这里只登记 PDF（内核当前唯一消费的文档类别）
            # input_file accepts more document types; only PDF is registered here (the only
            # document category currently consumed)
            "document": ["application/pdf"],
        },
    ),
}

# PDF / 内联媒体上限（model 级；Responses 与 Chat Completions 共用同一请求预算）
# PDF / inline-media limits (model level; shared request budget across both surfaces)
# - 每个文件及整个请求的文件总量均须低于 50 MB / each file and combined request under 50 MB
# - 图片请求总 payload 上限 512 MB / up to 512 MB total payload for image requests
OPENAI_PDF_KWARGS: dict[str, Any] = {
    "max_pdf_size_mb": 50.0,
    "supported_document_mime_type": ["application/pdf"],
    "max_document_size_mb": 50.0,
    "max_inline_media_bytes": 512_000_000,
}
