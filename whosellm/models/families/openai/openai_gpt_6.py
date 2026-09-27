from whosellm.capabilities import MediaCountLimit, ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-6 系列 / GPT-6 Series（2026-09-04 首发 / First released 2026-09-04）
#
# 天体三档命名 / Three celestial tiers:
#   astra 旗舰，专为最难的端到端工作而建 / flagship, for the hardest end-to-end work
#         复杂推理、编码、计算机使用、研究与文档创作
#         Complex reasoning, coding, computer use, research, and document creation
#   sol   中档主力，面向复杂编码与 agentic 工作流（2026-09-22 发布）
#         Mid-tier workhorse for complex coding and agentic workflows (released 2026-09-22)
#   luna  低成本高并发，适合路由、分类、抽取、摘要（2026-09-22 发布）
#         Cost-efficient, high-volume tier for routing, classification, extraction (2026-09-22)
# GPT-6 无 terra 档；"-pro" 不是独立模型 ID，而是 reasoning 参数
# No GPT-6 terra tier; "-pro" is a reasoning mode, not a model ID
#
# 档位差异 / Tier differences:
#   - 三档上下文窗口与工具面一致（1.05M ctx / 128K out，web search / file search /
#     图像生成 / code interpreter / computer use 全支持）
#     Identical context window and tool surface across all three tiers
#   - astra 的 reasoning.effort: low/medium/high/xhigh/max（不接受 none，需改用 low）
#     astra: low/medium/high/xhigh/max only (rejects none; use low instead)
#   - sol/luna 额外接受 none，默认 medium / sol/luna also accept none, default medium
# 企业级 Trusted Access Program 首批开放（Plus/Pro 等后续开放）
# Initially available via enterprise Trusted Access Program
# 来源 / Sources:
#   https://developers.openai.com/api/docs/models/gpt-6-astra
#   https://developers.openai.com/api/docs/models/gpt-6-sol
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
        # 官方文档：单请求最多 1500 张图片（https://developers.openai.com/api/docs/guides/images-vision）
        # Per docs: up to 1,500 images per request
        media_count_limit=MediaCountLimit(per_type={"image": 1500}),
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
        "gpt-6-sol": SpecificModelConfig(
            version_default="6.0",
            variant_default="sol",
            variant_priority=(1,),  # 中档主力档位 / mid-tier workhorse tier
            # capabilities 继承版本级默认值 / inherits version-level default
            # reasoning.effort: none/low/medium(默认)/high/xhigh/max
            patterns=[
                "gpt-6-sol-{year:4d}-{month:2d}-{day:2d}",
                "gpt-6-sol",
            ],
        ),
        "gpt-6-luna": SpecificModelConfig(
            version_default="6.0",
            variant_default="luna",
            variant_priority=(0,),  # 低成本档位 / cost-efficient tier
            # capabilities 继承版本级默认值 / inherits version-level default
            # reasoning.effort: none/low/medium(默认)/high/xhigh/max
            patterns=[
                "gpt-6-luna-{year:4d}-{month:2d}-{day:2d}",
                "gpt-6-luna",
            ],
        ),
    },
)
