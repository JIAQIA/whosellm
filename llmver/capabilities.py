# filename: capabilities.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型能力定义 / Model capability definitions
"""

from pydantic import BaseModel, Field


class ModelCapabilities(BaseModel):
    """
    模型能力描述 / Model capability description
    """

    supports_thinking: bool = Field(
        default=False,
        description="是否支持思考（推理）模式 / Whether thinking (reasoning) mode is supported",
    )

    supports_vision: bool = Field(
        default=False,
        description="是否支持图片输入 / Whether image input is supported",
    )

    supports_audio: bool = Field(
        default=False,
        description="是否支持音频输入 / Whether audio input is supported",
    )

    supports_video: bool = Field(
        default=False,
        description="是否支持视频输入 / Whether video input is supported",
    )

    supports_pdf: bool = Field(
        default=False,
        description="是否支持PDF输入 / Whether PDF input is supported",
    )

    supports_function_calling: bool = Field(
        default=False,
        description="是否支持函数调用 / Whether function calling is supported",
    )

    supports_streaming: bool = Field(
        default=True,
        description="是否支持流式输出 / Whether streaming output is supported",
    )

    max_tokens: int | None = Field(
        default=None,
        description="最大token数 / Maximum number of tokens",
    )

    context_window: int | None = Field(
        default=None,
        description="上下文窗口大小 / Context window size",
    )

    # 图片相关限制 / Image-related limitations
    max_image_size_mb: float | None = Field(
        default=None,
        description="最大图片大小(MB) / Maximum image size in MB",
    )

    max_image_pixels: tuple[int, int] | None = Field(
        default=None,
        description="最大图片像素(宽, 高) / Maximum image pixels (width, height)",
    )

    supported_image_formats: list[str] = Field(
        default_factory=lambda: ["jpg", "jpeg", "png"],
        description="支持的图片格式 / Supported image formats",
    )

    supports_image_base64: bool = Field(
        default=True,
        description="是否支持base64编码的图片 / Whether base64-encoded images are supported",
    )

    # 视频相关限制 / Video-related limitations
    max_video_size_mb: float | None = Field(
        default=None,
        description="最大视频大小(MB) / Maximum video size in MB",
    )

    max_video_duration_seconds: int | None = Field(
        default=None,
        description="最大视频时长(秒) / Maximum video duration in seconds",
    )

    supported_video_formats: list[str] = Field(
        default_factory=lambda: ["mp4", "avi", "mov"],
        description="支持的视频格式 / Supported video formats",
    )

    # 音频相关限制 / Audio-related limitations
    max_audio_size_mb: float | None = Field(
        default=None,
        description="最大音频大小(MB) / Maximum audio size in MB",
    )

    max_audio_duration_seconds: int | None = Field(
        default=None,
        description="最大音频时长(秒) / Maximum audio duration in seconds",
    )

    supported_audio_formats: list[str] = Field(
        default_factory=lambda: ["mp3", "wav", "m4a"],
        description="支持的音频格式 / Supported audio formats",
    )

    class Config:
        """Pydantic 配置 / Pydantic configuration"""

        frozen = True  # 使实例不可变 / Make instances immutable
