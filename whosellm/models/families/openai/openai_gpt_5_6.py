from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ============================================================================
# GPT-5.6 系列 / GPT-5.6 Series（当前旗舰 / Current flagship）
#
# GPT-5.6 弃用 mini/nano 命名，改用天体三档命名，官方明示与旧档位的对应关系：
# GPT-5.6 replaces mini/nano with celestial tier names; official mapping:
#   sol   ≈ 无后缀 base 档（gpt-5.6 别名路由到 sol） / unsuffixed tier (alias target)
#   terra ≈ mini 档 / mini tier
#   luna  ≈ nano 档 / nano tier
# 三档能力完全一致，仅价格与速率限制不同。
# All three tiers share identical capabilities; only pricing/rate limits differ.
# 来源 / Source: https://developers.openai.com/api/docs/models/gpt-5.6-sol
# ============================================================================

GPT_5_6 = ModelFamilyConfig(
    family=ModelFamily.GPT,
    provider=Provider.OPENAI,
    version_default="5.6",
    variant_priority_default=(1,),  # base 的优先级 / base priority
    patterns=[],  # 父 patterns 由 gpt_5_4.py 通过 Registry Merge 提供
    # 父 patterns provided by gpt_5_4.py via Registry Merge
    capabilities=ModelCapabilities(
        supports_thinking=True,  # reasoning.effort: none/low/medium(默认)/high/xhigh/max
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
        "gpt-5.6": SpecificModelConfig(
            version_default="5.6",
            variant_default="base",
            variant_priority=(1,),
            # 官方别名，路由到 gpt-5.6-sol / Official alias routing to gpt-5.6-sol
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.6-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.6",
            ],
        ),
        "gpt-5.6-sol": SpecificModelConfig(
            version_default="5.6",
            variant_default="sol",
            variant_priority=(1,),  # 官方：≈ 无后缀 base 档 / official: ≈ unsuffixed tier
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.6-sol-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.6-sol",
            ],
        ),
        "gpt-5.6-terra": SpecificModelConfig(
            version_default="5.6",
            variant_default="terra",
            variant_priority=(0,),  # 官方：≈ mini 档 / official: ≈ mini tier
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.6-terra-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.6-terra",
            ],
        ),
        "gpt-5.6-luna": SpecificModelConfig(
            version_default="5.6",
            variant_default="luna",
            variant_priority=(0,),  # 官方：≈ nano 档 / official: ≈ nano tier
            # capabilities 继承版本级默认值 / inherits version-level default
            patterns=[
                "gpt-5.6-luna-{year:4d}-{month:2d}-{day:2d}",
                "gpt-5.6-luna",
            ],
        ),
    },
)
