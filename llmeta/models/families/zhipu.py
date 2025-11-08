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
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "glm-4v-{variant:variant}-{mmdd:4d}",  # glm-4v-plus-0111
        "glm-4v-{variant:variant}",  # glm-4v-plus, glm-4v-flash
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
            variant_priority=(3,),  # plus 的优先级 / plus priority
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
            variant_priority=(3,),  # plus 的优先级 / plus priority
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
            variant_priority=(0,),  # flash 的优先级 / flash priority
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
# GLM-4.5V 系列 / GLM-4.5V Series
# ============================================================================

GLM_45V = ModelFamilyConfig(
    family=ModelFamily.GLM_45V,
    provider=Provider.ZHIPU,
    version_default="4.5",
    variant_priority_default=(1,),
    patterns=[
        "glm-4.5v-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "glm-4.5v-{variant:variant}-{mmdd:4d}",
        "glm-4.5v-{variant:variant}",
        "glm-4.5v-{year:4d}-{month:2d}-{day:2d}",
        "glm-4.5v-{mmdd:4d}",
        "glm-4.5v",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_vision=True,
        supports_video=True,
        supports_pdf=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=64000,
    ),
)

# ============================================================================
# GLM-4.6 系列 / GLM-4.6 Series
# ============================================================================

GLM_46 = ModelFamilyConfig(
    family=ModelFamily.GLM_46,
    provider=Provider.ZHIPU,
    version_default="4.6",
    variant_priority_default=(1,),
    patterns=[
        "glm-4.6-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "glm-4.6-{variant:variant}-{mmdd:4d}",
        "glm-4.6-{variant:variant}",
        "glm-4.6-{year:4d}-{month:2d}-{day:2d}",
        "glm-4.6-{mmdd:4d}",
        "glm-4.6",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        max_tokens=128000,
        context_window=200000,
    ),
)

# ============================================================================
# GLM-4 系列 / GLM-4 Series
# ============================================================================

GLM_4 = ModelFamilyConfig(
    family=ModelFamily.GLM_4,
    provider=Provider.ZHIPU,
    version_default="4.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "glm-4-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "glm-4-{variant:variant}",
        "glm-4-{mmdd:4d}",
        "glm-4",
        "chatglm",  # 别名 / Alias
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
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        "glm-3-{variant:variant}",
        "glm-3",
    ],
    capabilities=ModelCapabilities(
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=32000,
    ),
)

# ============================================================================
# CogView-4 系列 / CogView-4 Series
# ============================================================================

COGVIEW_4 = ModelFamilyConfig(
    family=ModelFamily.COGVIEW_4,
    provider=Provider.ZHIPU,
    version_default="4.0",
    variant_priority_default=(1,),
    patterns=[
        "cogview-4-{yymmdd:6d}",
        "cogview-4-{mmdd:4d}",
        "cogview-4",
        "cogview",
    ],
    capabilities=ModelCapabilities(
        supports_streaming=False,
        supports_structured_outputs=False,
    ),
)

# ============================================================================
# CogVideoX-3 系列 / CogVideoX-3 Series
# ============================================================================

COGVIDEOX_3 = ModelFamilyConfig(
    family=ModelFamily.COGVIDEOX_3,
    provider=Provider.ZHIPU,
    version_default="3.0",
    variant_priority_default=(1,),
    patterns=[
        "cogvideox-3-{variant:variant}",
        "cogvideox-3",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_video=True,
        supports_streaming=False,
        supports_structured_outputs=False,
        max_video_duration_seconds=10,
    ),
)

# ============================================================================
# CogVideoX-2 系列 / CogVideoX-2 Series
# ============================================================================

COGVIDEOX_2 = ModelFamilyConfig(
    family=ModelFamily.COGVIDEOX_2,
    provider=Provider.ZHIPU,
    version_default="2.0",
    variant_priority_default=(1,),
    patterns=[
        "cogvideox-2-{variant:variant}",
        "cogvideox-2",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_video=True,
        supports_streaming=False,
        supports_structured_outputs=False,
    ),
)
