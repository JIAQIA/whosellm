# filename: zhipu.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
智谱 AI 模型家族配置 / Zhipu AI model family configurations
"""

from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.models.config import ModelFamilyConfig, SpecificModelConfig
from llmeta.provider import Provider

# ============================================================================
# GLM-4V 系列（视觉模型） / GLM-4V Series (Vision Model)
# ============================================================================

GLM_4V = ModelFamilyConfig(
    family=ModelFamily.GLM_4V,
    provider=Provider.ZHIPU,
    version_default="4.0",
    patterns=[
        "glm-4v-{variant}-{mmdd:4d}",  # glm-4v-plus-0111
        "glm-4v-{variant}",  # glm-4v-plus, glm-4v-flash
        "glm-4v",  # glm-4v (base)
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=128000,
        max_image_size_mb=10.0,
        max_image_pixels=(4096, 4096),
    ),
    # 特定模型的精确配置 / Precise configuration for specific models
    specific_models={
        "glm-4v-plus-0111": SpecificModelConfig(
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
                max_video_size_mb=200.0,  # 更大的视频限制
                max_video_duration_seconds=None,  # 无时长限制
            ),
            patterns=[
                "glm-4v-plus-0111",
            ],
        ),
        "glm-4v-plus": SpecificModelConfig(
            version="4.0",
            variant="vision-plus",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,  # plus 支持视频
                supports_streaming=True,
                max_tokens=8192,
                context_window=8192,
                max_image_size_mb=5.0,
                max_image_pixels=(6000, 6000),
                supports_image_base64=True,
                max_video_size_mb=20.0,
                max_video_duration_seconds=30,
            ),
            patterns=[
                "glm-4v-plus-{mmdd:4d}",
                "glm-4v-plus",
            ],
        ),
        "glm-4v-flash": SpecificModelConfig(
            version="4.0",
            variant="vision-flash",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_streaming=True,
                max_tokens=8192,
                context_window=8192,
                max_image_size_mb=5.0,
                max_image_pixels=(6000, 6000),
                supports_image_base64=False,  # flash 不支持 base64
            ),
        ),
    },
)

# ============================================================================
# GLM-4 系列 / GLM-4 Series
# ============================================================================

GLM_4 = ModelFamilyConfig(
    family=ModelFamily.GLM_4,
    provider=Provider.ZHIPU,
    version_default="4.0",
    patterns=[
        "glm-4-{variant}-{year:4d}-{month:2d}-{day:2d}",
        "glm-4-{variant}",
        "glm-4",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=128000,
    ),
)

# ============================================================================
# GLM-3 系列 / GLM-3 Series
# ============================================================================

GLM_3 = ModelFamilyConfig(
    family=ModelFamily.GLM_3,
    provider=Provider.ZHIPU,
    version_default="3.0",
    patterns=[
        "glm-3-{variant}",
        "glm-3",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=32000,
    ),
)
