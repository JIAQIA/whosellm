from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5.5 系列 / GPT-5.5 Series（2026-04-23 发布 / Released 2026-04-23）
#
# 官方定位：面向编码与专业工作的新一代智能 / A new class of intelligence for
# coding and professional work
# 来源 / Source: https://developers.openai.com/api/docs/models/gpt-5.5
# ============================================================================

GPT_5_5 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="5.5",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[],  # 父 patterns 由 gpt_5_4.py 通过 Registry Merge 提供
    # 父 patterns provided by gpt_5_4.py via Registry Merge
    capabilities=ModelCapabilities(
        supports_thinking=True,  # reasoning.effort: none/low/medium(默认)/high/xhigh
        supports_vision=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_fine_tuning=False,
        supports_distillation=False,  # 官方文档已不按模型标注 distillation / docs no longer flag per-model
        supports_web_search=True,
        supports_file_search=True,
        supports_image_generation=True,
        supports_code_interpreter=True,
        supports_computer_use=True,
        max_tokens=128_000,
        context_window=1_050_000,
    ),
    specific_models={
        "gpt-5.5": SpecificModelConfig(
            version_default="5.5",
            variant_default="base",
            variant_priority=(1,),
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.5-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.5",
            ],
        ),
        "gpt-5.5-pro": SpecificModelConfig(
            version_default="5.5",
            variant_default="pro",
            variant_priority=(4,),
            # 仅 Responses API（含 Batch），不支持 Chat Completions 与 streaming
            # Responses API only (incl. Batch); no Chat Completions, no streaming
            capabilities=ModelCapabilities(
                supports_thinking=True,  # reasoning.effort: medium/high(默认)/xhigh
                supports_vision=True,
                supports_function_calling=True,
                supports_streaming=False,
                supports_structured_outputs=True,
                supports_fine_tuning=False,
                supports_distillation=False,
                supports_web_search=True,
                supports_file_search=True,
                supports_image_generation=True,
                supports_code_interpreter=True,
                supports_computer_use=False,
                max_tokens=128_000,
                context_window=1_050_000,
            ),
            patterns=[
                "gpt-5.5-pro-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.5-pro",
            ],
        ),
    },
)
