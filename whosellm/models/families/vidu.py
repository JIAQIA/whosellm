# filename: vidu.py
# @Time    : 2025/11/8 23:53
# @Author  : Cascade
"""
Vidu Q1 模型家族配置 / Vidu Q1 model family configuration
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

VIDU_Q1 = ModelFamilyConfig(
    family=ModelFamily.VIDU_Q1,
    provider=Provider.VIDU,
    version_default="1.0",
    variant_priority_default=(1,),
    patterns=[
        "viduq1-{variant:variant}",
        "viduq1",
    ],
    capabilities=ModelCapabilities(
        supports_video=True,
        supports_streaming=False,
        supports_structured_outputs=False,
        max_video_duration_seconds=5,
    ),
    specific_models={
        "viduq1-image": SpecificModelConfig(
            version="1.0",
            variant="image",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,
                supports_streaming=False,
                supports_structured_outputs=False,
                max_video_duration_seconds=5,
            ),
            patterns=["viduq1-image"],
        ),
        "viduq1-start-end": SpecificModelConfig(
            version="1.0",
            variant="start-end",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,
                supports_streaming=False,
                supports_structured_outputs=False,
                max_video_duration_seconds=5,
            ),
            patterns=["viduq1-start-end"],
        ),
        "viduq1-text": SpecificModelConfig(
            version="1.0",
            variant="text",
            capabilities=ModelCapabilities(
                supports_video=True,
                supports_streaming=False,
                supports_structured_outputs=False,
                max_video_duration_seconds=5,
            ),
            patterns=["viduq1-text"],
        ),
    },
)


VIDU_2 = ModelFamilyConfig(
    family=ModelFamily.VIDU_2,
    provider=Provider.VIDU,
    version_default="2.0",
    variant_priority_default=(1,),
    patterns=[
        "vidu2-{variant:variant}",
        "vidu2",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_video=True,
        supports_audio=True,
        supports_streaming=False,
        supports_structured_outputs=False,
        max_video_duration_seconds=4,
    ),
    specific_models={
        "vidu2-image": SpecificModelConfig(
            version="2.0",
            variant="image",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,
                supports_audio=True,
                supports_streaming=False,
                supports_structured_outputs=False,
                max_video_duration_seconds=4,
            ),
            patterns=["vidu2-image"],
        ),
        "vidu2-start-end": SpecificModelConfig(
            version="2.0",
            variant="start-end",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,
                supports_audio=True,
                supports_streaming=False,
                supports_structured_outputs=False,
                max_video_duration_seconds=4,
            ),
            patterns=["vidu2-start-end"],
        ),
        "vidu2-reference": SpecificModelConfig(
            version="2.0",
            variant="reference",
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,
                supports_audio=True,
                supports_streaming=False,
                supports_structured_outputs=False,
                max_video_duration_seconds=4,
            ),
            patterns=["vidu2-reference"],
        ),
    },
)
