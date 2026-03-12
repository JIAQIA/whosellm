"""
Google 模型家族配置 / Google model family configurations
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ==========================================================================
# Gemini 系列 / Gemini Series
# ==========================================================================

GEMINI = ModelFamilyConfig(
    family=ModelFamily.GEMINI,
    provider=Provider.GOOGLE,
    version_default="2.5",
    variant_default="pro",
    variant_priority_default=(4,),  # pro 的默认优先级 / default priority for pro
    patterns=[
        # 连字符版本模式（3-1 风格）/ Hyphen-version patterns (3-1 style)
        "gemini-{major:d}-{minor:d}-{variant:variant}",
        # 点版本模式（2.5 风格）/ Dot-version patterns (2.5 style)
        "gemini-{version}-{variant:variant}",
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_vision=True,
        supports_audio=True,
        supports_video=True,
        supports_pdf=True,
        supports_function_calling=True,
        supports_structured_outputs=True,
        supports_streaming=True,
        supports_code_interpreter=True,
        max_tokens=65_536,
        context_window=1_000_000,
    ),
    specific_models={
        # ================================================================
        # Gemini 2.5 系列 / Gemini 2.5 Series
        # ================================================================
        "gemini-2.5-pro": SpecificModelConfig(
            version="2.5",
            variant="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_code_interpreter=True,
                max_tokens=65_536,
                context_window=1_000_000,
            ),
            patterns=[
                "gemini-2.5-pro-{suffix:variant}",
                "gemini-2.5-pro",
            ],
        ),
        "gemini-2.5-flash-lite": SpecificModelConfig(
            version="2.5",
            variant="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=False,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_code_interpreter=False,
                max_tokens=65_536,
                context_window=1_000_000,
            ),
            patterns=[
                "gemini-2.5-flash-lite-{suffix:variant}",
                "gemini-2.5-flash-lite",
            ],
        ),
        "gemini-2.5-flash": SpecificModelConfig(
            version="2.5",
            variant="flash",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_code_interpreter=True,
                max_tokens=65_536,
                context_window=1_000_000,
            ),
            patterns=[
                "gemini-2.5-flash-{suffix:variant}",
                "gemini-2.5-flash",
            ],
        ),
        # ================================================================
        # Gemini 3.x 系列 / Gemini 3.x Series
        # ================================================================
        "gemini-3-flash-preview": SpecificModelConfig(
            version="3.0",
            variant="flash",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_code_interpreter=True,
                max_tokens=65_536,
                context_window=1_000_000,
            ),
            patterns=[
                "gemini-3-flash-preview",
            ],
        ),
        "gemini-3-1-pro-preview": SpecificModelConfig(
            version="3.1",
            variant="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_code_interpreter=True,
                max_tokens=65_536,
                context_window=1_000_000,
            ),
            patterns=[
                "gemini-3-1-pro-preview",
            ],
        ),
        "gemini-3-1-flash-lite-preview": SpecificModelConfig(
            version="3.1",
            variant="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_streaming=True,
                supports_code_interpreter=True,
                max_tokens=65_536,
                context_window=1_000_000,
            ),
            patterns=[
                "gemini-3-1-flash-lite-preview",
            ],
        ),
    },
)
