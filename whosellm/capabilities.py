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
from typing import Literal

# 无文档化上限哨兵：该媒体类型官方未给出数量上限，仅受上下文 token 预算约束
# Sentinel for "no documented limit": the provider documents no count cap,
# only the context-window token budget constrains the input.
UNLIMITED = math.inf

MediaCount = int | float  # 正整数 = 文档化上限；float 仅允许 UNLIMITED（math.inf）


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
