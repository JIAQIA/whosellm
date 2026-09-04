from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-6 系列 / GPT-6 Series（2026-09-04 发布 / Released 2026-09-04）
#
# GPT-6 Astra：OpenAI 迄今最强模型，专为最难的端到端工作而建
# GPT-6 Astra: OpenAI's most capable model, built for the hardest end-to-end work
# 官方文案 / Tags:
#   - 复杂推理、编码、计算机使用、研究与文档创作
#     Complex reasoning, coding, computer use, research, and document creation
#   - reasoning.effort: low/medium/high/xhigh/max
#   - 1,050,000 上下文窗口 / 1,050,000 context window
#   - 企业级 Trusted Access Program 首批开放（Plus/Pro 等后续开放）
#     Initially available via enterprise Trusted Access Program
# 来源 / Source: https://developers.openai.com/api/docs/models/gpt-6-astra
# ============================================================================

GPT_6 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="6.0",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[],  # 父 patterns 由 gpt_5_4.py 通过 Registry Merge 提供
    # 父 patterns provided by gpt_5_4.py via Registry Merge
    capabilities=ModelCapabilities(
        supports_thinking=True,  # reasoning.effort: low/medium/high/xhigh/max
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
        "gpt-6-astra": SpecificModelConfig(
            version_default="6.0",
            variant_default="astra",
            variant_priority=(5,),  # 旗舰级优先级 / flagship-tier priority
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-6-astra-{year:4d}-{month:2d}-{day:2d}",
                "gpt-6-astra",
            ],
        ),
    },
)
