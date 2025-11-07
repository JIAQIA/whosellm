# filename: zhipu.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
智谱 AI 模型定义 / Zhipu AI model definitions
"""

from llmver.capabilities import ModelCapabilities
from llmver.models.base import ModelInfo, parse_version, register_model
from llmver.provider import Provider

# GLM-4 系列 / GLM-4 series
register_model(
    "glm-4",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="base",
        capabilities=ModelCapabilities(
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=128000,
        ),
        version_tuple=parse_version("4.0"),
    ),
)

register_model(
    "glm-4-plus",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="plus",
        capabilities=ModelCapabilities(
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=128000,
        ),
        version_tuple=parse_version("4.0.1"),
    ),
)

register_model(
    "glm-4-flash",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="flash",
        capabilities=ModelCapabilities(
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=128000,
        ),
        version_tuple=parse_version("4.0.0"),
    ),
)

# GLM-4V 系列（视觉模型） / GLM-4V series (vision models)
register_model(
    "glm-4v",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="vision",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=8192,
            max_image_size_mb=5.0,
            max_image_pixels=(6000, 6000),
            supports_image_base64=True,
        ),
        version_tuple=parse_version("4.0"),
    ),
)

register_model(
    "glm-4v-plus",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="vision-plus",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_video=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=8192,
            max_image_size_mb=5.0,
            max_image_pixels=(6000, 6000),
            supports_image_base64=True,
            max_video_size_mb=20.0,
            max_video_duration_seconds=30,
        ),
        version_tuple=parse_version("4.0.1"),
    ),
)

register_model(
    "glm-4v-plus-0111",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="vision-plus-0111",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_video=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=8192,
            max_image_size_mb=5.0,
            max_image_pixels=(6000, 6000),
            supports_image_base64=True,
            max_video_size_mb=200.0,  # 更大的视频限制 / Larger video limit
            max_video_duration_seconds=None,  # 无时长限制 / No duration limit
        ),
        version_tuple=parse_version("4.0.2"),
    ),
)

register_model(
    "glm-4v-flash",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="4.0",
        variant="vision-flash",
        capabilities=ModelCapabilities(
            supports_vision=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=8192,
            max_image_size_mb=5.0,
            max_image_pixels=(6000, 6000),
            supports_image_base64=False,  # 不支持 base64 / Does not support base64
        ),
        version_tuple=parse_version("4.0.0"),
    ),
)

# GLM-3 系列 / GLM-3 series
register_model(
    "glm-3-turbo",
    ModelInfo(
        provider=Provider.ZHIPU,
        version="3.0",
        variant="turbo",
        capabilities=ModelCapabilities(
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=128000,
        ),
        version_tuple=parse_version("3.0"),
    ),
)
