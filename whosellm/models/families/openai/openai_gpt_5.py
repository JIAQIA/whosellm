# filename: gpt_5.py
# @Time    : 2025/11/8 13:28
# @Author  : JQQ
# @Email   : jiaqia@qknode.com
# @Software: PyCharm
from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5 系列 / GPT-5 Series
#
# 包含 GPT-5 基础版及其子版本（5.1, 5.2, 5.4）和变体（mini, nano, pro, codex）
# Includes GPT-5 base and sub-versions (5.1, 5.2, 5.4) and variants (mini, nano, pro, codex)
# ============================================================================


GPT_5 = ModelFamilyConfig(
    family=ModelFamily.GPT_5,
    provider=Provider.OPENAI,
    version_default="5.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[
        # 点版本模式（最具体在前）/ Dot-version patterns (most specific first)
        "gpt-5.{minor:d}-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-5.4-pro-2026-03-05
        "gpt-5.{minor:d}-{year:4d}-{month:2d}-{day:2d}",  # gpt-5.4-2026-03-05
        "gpt-5.{minor:d}-{variant:variant}",  # gpt-5.4-pro
        "gpt-5.{minor:d}",  # gpt-5.4
        # 基础模式 / Base patterns
        "gpt-5-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-5-mini-2025-08-07
        "gpt-5-{variant:variant}",  # gpt-5-mini
        "gpt-5-{year:4d}-{month:2d}-{day:2d}",  # gpt-5-2025-08-07
        "gpt-5",  # gpt-5 (base)
    ],
    capabilities=ModelCapabilities(
        supports_thinking=True,
        supports_vision=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_fine_tuning=False,
        supports_distillation=True,
        supports_web_search=True,
        supports_file_search=True,
        supports_image_generation=True,
        supports_code_interpreter=True,
        supports_mcp=True,
        max_tokens=128_000,
        context_window=400_000,
    ),
    specific_models={
        # ================================================================
        # GPT-5 变体 / GPT-5 Variants
        # ================================================================
        "gpt-5-mini": SpecificModelConfig(
            version="5.0",
            variant="mini",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=False,
                supports_code_interpreter=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-mini",
            ],
        ),
        "gpt-5-nano": SpecificModelConfig(
            version="5.0",
            variant="nano",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=False,
                supports_code_interpreter=False,
                supports_mcp=True,
                max_tokens=16_384,
                context_window=128_000,
            ),
            patterns=[
                "gpt-5-nano-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-nano",
            ],
        ),
        "gpt-5-pro": SpecificModelConfig(
            version="5.0",
            variant="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_computer_use=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-pro",
            ],
        ),
        # ================================================================
        # GPT-5.1 / GPT-5.1
        # ================================================================
        "gpt-5.1": SpecificModelConfig(
            version="5.1",
            variant="base",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.1-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1",
            ],
        ),
        # ================================================================
        # GPT-5.2 及其变体 / GPT-5.2 and variants
        # ================================================================
        "gpt-5.2": SpecificModelConfig(
            version="5.2",
            variant="base",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.2-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.2",
            ],
        ),
        "gpt-5.2-pro": SpecificModelConfig(
            version="5.2",
            variant="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_computer_use=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.2-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.2-pro",
            ],
        ),
        # ================================================================
        # GPT-5.4 及其变体 / GPT-5.4 and variants (当前旗舰 / Current flagship)
        # ================================================================
        "gpt-5.4": SpecificModelConfig(
            version="5.4",
            variant="base",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_computer_use=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.4-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.4",
            ],
        ),
        "gpt-5.4-pro": SpecificModelConfig(
            version="5.4",
            variant="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_computer_use=True,
                supports_mcp=True,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.4-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.4-pro",
            ],
        ),
        # ================================================================
        # GPT-5 Codex 系列 / GPT-5 Codex Series
        # ================================================================
        "gpt-5-codex": SpecificModelConfig(
            version="5.0",
            variant="codex",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5-codex",
            ],
        ),
        "gpt-5.1-codex": SpecificModelConfig(
            version="5.1",
            variant="codex",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.1-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1-codex",
            ],
        ),
        "gpt-5.1-codex-mini": SpecificModelConfig(
            version="5.1",
            variant="codex-mini",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=400_000,
            ),
            patterns=[
                "gpt-5.1-codex-mini-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1-codex-mini",
            ],
        ),
        "gpt-5.1-codex-max": SpecificModelConfig(
            version="5.1",
            variant="codex-max",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.1-codex-max-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.1-codex-max",
            ],
        ),
        "gpt-5.2-codex": SpecificModelConfig(
            version="5.2",
            variant="codex",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.2-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.2-codex",
            ],
        ),
        "gpt-5.3-codex": SpecificModelConfig(
            version="5.3",
            variant="codex",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.3-codex-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.3-codex",
            ],
        ),
    },
)
