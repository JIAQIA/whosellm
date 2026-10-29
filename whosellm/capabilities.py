# filename: capabilities.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型能力定义 / Model capability definitions
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

# 无文档化上限哨兵：该媒体类型官方未给出数量上限，仅受上下文 token 预算约束
# Sentinel for "no documented limit": the provider documents no count cap,
# only the context-window token budget constrains the input.
UNLIMITED = math.inf

MediaCount = int | float  # 正整数 = 文档化上限；float 仅允许 UNLIMITED（math.inf）


class LLMApiSurface(str, Enum):
    """
    LLM API surface 词表 / LLM API surface vocabulary

    工具结果的媒体承载能力是 per-(provider × API-surface) 的，而不是 per-model 的。
    本枚举由 whosellm 定义并导出，是能力数据的索引键；内核与其他实现只引用，不另建同义枚举。
    Tool-result media capability is per-(provider × API-surface), not per-model.
    This enum is owned by whosellm and is the index key for capability data; consumers
    reference it instead of defining parallel vocabularies.

    继承 str 使其可直接作为 dict 键并参与 JSON 序列化。
    Inherits str so instances work directly as dict keys and serialize to JSON.
    """

    CLAUDE_MESSAGES = "claude_messages"
    OPENAI_CHAT_COMPLETIONS = "openai_chat_completions"
    OPENAI_RESPONSES = "openai_responses"
    GEMINI = "gemini"
    DASHSCOPE = "dashscope"
    GLM = "glm"
    DEEPSEEK = "deepseek"
    # DeepSeek 的 Responses 端点（https://api.deepseek.com/responses）与 Chat Completions
    # 是两套 surface，能力不完全相同（例如 PDF input_file 静默不投递）。
    # DeepSeek's Responses endpoint is a distinct surface from Chat Completions; they do
    # not share identical capabilities (e.g. PDF input_file is silently dropped).
    DEEPSEEK_RESPONSES = "deepseek_responses"

    def __str__(self) -> str:
        """返回字符串值（而非 Enum 默认的成员名表示）/ Return the value instead of the enum repr"""
        return self.value


# 工具结果可原生承载的媒体类别（由 MIME 推出，字段中不重复 category）
# Media categories a tool result can natively carry (derived from MIME; no duplicate category field)
ToolResultModality = Literal["image", "audio", "video", "document"]


@dataclass(frozen=True)
class ToolResultSurfaceCapability:
    """
    单个 API surface 的工具结果能力 / Tool-result capability for one API surface

    modalities:
      该 surface 的工具结果可**原生**承载的媒体类别。
      空元组 = 明确不支持（内核走兄弟 user 消息或降级）；键缺失 = 该 surface 未声明。
    modalities:
      Media categories the surface can natively carry in tool results.
      Empty tuple = explicitly unsupported (callers fall back to a sibling user message
      or degrade); missing key = surface undeclared.

    max_inline_bytes:
      ［可选］该 surface 工具结果单条内联上限（字节）；None = 未声明。
    max_inline_bytes:
      [optional] Per-tool-result inline byte cap for this surface; None = undeclared.

    mime_types:
      ［可选］按媒体类别细分的允许 MIME；None = 未声明（调用方按类别级保守默认）。
    mime_types:
      [optional] Allowed MIME types per media category; None = undeclared (callers apply
      a conservative category-level default).
    """

    modalities: tuple[ToolResultModality, ...] = ()
    max_inline_bytes: int | None = None
    mime_types: dict[str, list[str]] | None = None

    def supports(self, modality: ToolResultModality) -> bool:
        """
        是否原生支持该媒体类别 / Whether the surface natively supports the modality
        """
        return modality in self.modalities


@dataclass(frozen=True)
class FileApiCapability:
    """
    文件 API 能力（预留，当前版本仅登记类型与空默认值）/ File API capability (reserved)

    本版本不参与任何消费逻辑，仅用于未来登记 provider 的文件上传能力。
    Not consumed in this version; reserved for future registration of provider file APIs.
    """

    supports_upload: bool = False  # 是否支持文件上传 / Whether file upload is supported
    max_file_size_mb: float | None = None  # 单文件大小上限(MB) / Max file size in MB
    supported_mime_types: list[str] = field(default_factory=list)  # 支持的文件MIME类型 / Supported file MIME types


@dataclass(frozen=True)
class MediaCountLimit:
    """
    单次请求媒体数量上限 / Per-request media count limits

    值域 / Value domain（键缺失 = 未实测，视同不支持）:
    - 0         确认不支持 / confirmed unsupported
    - 正整数    文档化上限，单位：个（张/段/...）/ documented cap (count)
    - UNLIMITED 无文档化上限，仅受上下文 token 预算约束 / no documented cap

    count_mode:
    - "per_type": 各类型独立计数（如 "image": 600 仅约束图片）/ per-type caps
    - "combined": 所有媒体共享一个总池（如 GLM 系列图片+视频合并计数）/ shared pool
    """

    per_type: dict[str, MediaCount] = field(default_factory=dict)
    count_mode: Literal["per_type", "combined"] = "per_type"
    # combined 模式的共享上限（per_type 模式下应为 None）
    # Shared pool cap for "combined" mode (None when count_mode == "per_type")
    combined: MediaCount | None = None

    def get(self, media_type: str) -> MediaCount:
        """
        返回该媒体类型的上限；键缺失（未实测）返回 0（视同不支持）
        Return the cap for a media type; missing keys (unmeasured) return 0 (treated as unsupported)
        """
        return self.per_type.get(media_type, 0)

    def is_supported(self, media_type: str) -> bool:
        """
        该媒体类型是否支持（0 > 0 为 False，正整数与 UNLIMITED 均为 True）
        Whether the media type is supported at all
        """
        return self.get(media_type) > 0


@dataclass(frozen=True)
class ModelCapabilities:
    """
    模型能力描述 / Model capability description

    使用 frozen=True 使其不可变，确保能力配置的稳定性
    Using frozen=True to make it immutable, ensuring stability of capability configuration
    """

    # 基础能力 / Basic capabilities
    supports_thinking: bool = False  # 是否支持思考（推理）模式 / Whether thinking (reasoning) mode is supported
    supports_vision: bool = False  # 是否支持图片输入 / Whether image input is supported
    supports_audio: bool = False  # 是否支持音频输入 / Whether audio input is supported
    supports_video: bool = False  # 是否支持视频输入 / Whether video input is supported
    supports_pdf: bool = False  # 是否支持PDF输入 / Whether PDF input is supported
    supports_function_calling: bool = False  # 是否支持函数调用 / Whether function calling is supported
    supports_structured_outputs: bool = True  # 是否支持结构化输出 / Whether structured outputs are supported
    supports_json_outputs: bool = True  # 是否支持Json输出，注意这个区别于结构化输出，结构化输出是指可以指定JSONSchema，而Json输出仅仅限制结果为Json形式
    supports_streaming: bool = True  # 是否支持流式输出 / Whether streaming output is supported
    supports_fine_tuning: bool = False  # 是否支持微调 / Whether fine-tuning is supported
    supports_distillation: bool = False  # 是否支持蒸馏 / Whether distillation is supported
    supports_predicted_outputs: bool = False  # 是否支持预测输出 / Whether predicted outputs are supported
    supports_web_search: bool = False  # 是否支持联网搜索工具 / Whether web search tool is supported
    supports_file_search: bool = False  # 是否支持文件检索 / Whether file search tool is supported
    supports_image_generation: bool = False  # 是否支持图像生成工具 / Whether image generation tool is supported
    supports_audio_generation: bool = False  # 是否支持音频生成工具 / Whether audio generation tool is supported
    supports_code_interpreter: bool = False  # 是否支持代码解释器 / Whether code interpreter tool is supported
    supports_computer_use: bool = False  # 是否支持电脑远程操作 / Whether computer use tool is supported

    # 通用限制 / General limitations
    max_tokens: int | None = None  # 最大输出token数 / Maximum number of tokens
    context_window: int | None = None  # 上下文窗口大小 / Context window size

    # 图片相关限制 / Image-related limitations
    max_image_size_mb: float | None = None  # 最大图片大小(MB) / Maximum image size in MB
    max_image_pixels: tuple[int, int] | None = None  # 最大图片像素(宽, 高) / Maximum image pixels (width, height)
    supported_image_mime_type: list[str] = field(
        default_factory=lambda: ["image/jpeg", "image/png"]
    )  # 支持的图片MIME类型 / Supported image MIME types
    supports_image_base64: bool = True  # 是否支持base64编码的图片 / Whether base64-encoded images are supported

    # 单次请求媒体（图片/视频/音频）数量限制 / Per-request media count limits
    media_count_limit: MediaCountLimit = field(default_factory=MediaCountLimit)

    # 单请求所有内联媒体字节总量上限（用户媒体 + 工具附件共享；不重复计数字段）。
    # 当官方只公布“整个请求 payload”上限时，该上限也登记在这里（媒体必然受其约束）。
    # Per-request total inline-media byte budget shared by user media and tool attachments.
    # When the provider only documents an entire-request payload cap, that cap is recorded
    # here too (media is necessarily bounded by it).
    max_inline_media_bytes: int | None = None

    # 文档相关限制 / Document-related limitations
    # None = 未声明（未知），不代表“不限”；调用方应套用自己的保守默认。
    # None = undeclared (unknown), NOT "unlimited"; callers apply their own conservative default.
    # max_pdf_size_mb 是单文件上限；max_pdf_pages 是单请求页数上限。
    # max_pdf_size_mb is a per-file cap; max_pdf_pages is a per-request page cap.
    max_pdf_size_mb: float | None = None  # 单个PDF大小上限(MB) / Max PDF size in MB
    max_pdf_pages: int | None = None  # 单请求PDF页数上限 / Max PDF pages per request
    max_document_size_mb: float | None = None  # 非PDF文档大小上限(MB，预留) / Max non-PDF document size in MB
    supported_document_mime_type: list[str] = field(
        default_factory=list
    )  # 支持的文档MIME类型 / Supported document MIME types

    # 视频相关限制 / Video-related limitations
    max_video_size_mb: float | None = None  # 最大视频大小(MB) / Maximum video size in MB
    max_video_duration_seconds: int | None = None  # 最大视频时长(秒) / Maximum video duration in seconds
    supported_video_mime_type: list[str] = field(
        default_factory=lambda: ["video/mp4", "video/x-msvideo", "video/quicktime"]
    )  # 支持的视频MIME类型 / Supported video MIME types

    # 音频相关限制 / Audio-related limitations
    max_audio_size_mb: float | None = None  # 最大音频大小(MB) / Maximum audio size in MB
    max_audio_duration_seconds: int | None = None  # 最大音频时长(秒) / Maximum audio duration in seconds
    supported_audio_mime_type: list[str] = field(
        default_factory=lambda: ["audio/mpeg", "audio/wav", "audio/mp4"]
    )  # 支持的音频MIME类型 / Supported audio MIME types

    # 工具结果（tool result / function response）按 API surface 登记的原生媒体能力
    # Native media capability of tool results keyed by API surface.
    # supports_vision / supports_audio / supports_video / supports_pdf 仍只表示用户消息能力；
    # 工具结果能力一律走本字段，二者不要混用。
    # The legacy supports_* flags describe USER messages only; tool-result capability
    # lives exclusively here.
    tool_result_surfaces: dict[LLMApiSurface, ToolResultSurfaceCapability] = field(default_factory=dict)

    # 文件 API 能力（预留，当前版本不消费）/ File API capability (reserved, not consumed yet)
    file_api: FileApiCapability | None = None
