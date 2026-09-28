# filename: test_deepseek.py
"""
DeepSeek 官方模型元数据 E2E 测试 / DeepSeek official model metadata E2E tests.

来源 / Sources:
  https://api-docs.deepseek.com/zh-cn/updates/（2026-09-10 DeepSeek-V4.1-Flash 发布）
  https://api-docs.deepseek.com/zh-cn/quick_start/pricing
  https://api-docs.deepseek.com/zh-cn/guides/vision
采集日期 / Collected: 2026-09-28（含 api.deepseek.com 实探复核 / verified against the live API）

约定 / Conventions:
  * 旧名（deepseek-v4-flash / -vision-exp / deepseek-chat / deepseek-reasoner）版本仍按名字解析为
    4.0，能力按当前实际服务模型（转发到 DeepSeek-V4.1-Flash）标注。
    Legacy names keep their name-derived version (4.0) while capabilities follow the
    currently serving model (routed to DeepSeek-V4.1-Flash).
  * deepseek-v4-pro 未被路由，保持纯文本（无图像输入）。
"""

import pytest

from whosellm import ModelFamily, Provider

from .conftest import assert_model_metadata

# ============================================================================
# DeepSeek V4.1-Flash 正式名（2026-09-10 发布）/ Canonical name of DeepSeek-V4.1-Flash
# 官方："将模型名称更改为 deepseek-flash 即可调用最新的 V4.1 Flash 模型"
# ============================================================================

V41_FLASH_MODELS = [
    (
        "deepseek-flash",
        {
            "provider": Provider.DEEPSEEK,
            "family": ModelFamily.DEEPSEEK,
            # 名字无版本号 → 按官方模型版本 DeepSeek-V4.1-Flash 标注
            "version": "4.1",
            "variant": "flash",
            "supports_thinking": True,  # 默认开启，effort 默认 high
            "supports_vision": True,  # 原生多模态视觉理解
            "supports_function_calling": True,
            "supports_streaming": True,
            "supports_json_outputs": True,
            "supports_structured_outputs": False,  # 仅 json_object，无 json_schema
            "context_window": 1_000_000,
            "max_tokens": 384_000,
        },
    ),
]

# ============================================================================
# 兼容路由旧名（官方措辞"暂时路由"）/ Routed legacy names ("temporarily routed" per vendor)
# ============================================================================

ROUTED_LEGACY_MODELS = [
    (
        "deepseek-v4-flash",
        {
            "provider": Provider.DEEPSEEK,
            "family": ModelFamily.DEEPSEEK,
            "version": "4.0",  # 版本轴按名字 / version parses from the name
            "variant": "flash",
            "supports_thinking": True,
            "supports_vision": True,  # 能力轴跟实际服务模型 / capabilities follow the serving model
            "supports_function_calling": True,
            "supports_streaming": True,
            "context_window": 1_000_000,
            "max_tokens": 384_000,
        },
    ),
    (
        "deepseek-v4-flash-vision-exp",
        {
            "provider": Provider.DEEPSEEK,
            "family": ModelFamily.DEEPSEEK,
            "version": "4.0",
            "variant": "flash-vision-exp",
            "supports_thinking": True,
            "supports_vision": True,
            "context_window": 1_000_000,
            "max_tokens": 384_000,
        },
    ),
    (
        "deepseek-chat",
        {
            "provider": Provider.DEEPSEEK,
            "family": ModelFamily.DEEPSEEK,
            "version": "4.0",
            "variant": "chat",
            "supports_thinking": False,  # 别名默认非思考模式 / alias defaults to non-thinking
            "supports_vision": True,
            "context_window": 1_000_000,
            "max_tokens": 384_000,
        },
    ),
    (
        "deepseek-reasoner",
        {
            "provider": Provider.DEEPSEEK,
            "family": ModelFamily.DEEPSEEK,
            "version": "4.0",
            "variant": "reasoner",
            "supports_thinking": True,  # 别名默认思考模式 / alias defaults to thinking
            "supports_vision": True,
            "context_window": 1_000_000,
            "max_tokens": 384_000,
        },
    ),
]

# ============================================================================
# 未被路由：deepseek-v4-pro 仍是 DeepSeek-V4-Pro-0813，纯文本
# Not routed: deepseek-v4-pro is still DeepSeek-V4-Pro-0813, text-only
# 实探 2026-09-28：带图不报错但静默忽略并编造答案 → supports_vision 必须为 False
# ============================================================================

TEXT_ONLY_MODELS = [
    (
        "deepseek-v4-pro",
        {
            "provider": Provider.DEEPSEEK,
            "family": ModelFamily.DEEPSEEK,
            "version": "4.0",
            "variant": "pro",
            "supports_thinking": True,
            "supports_vision": False,
            "supports_function_calling": True,
            "supports_streaming": True,
            "context_window": 1_000_000,
            "max_tokens": 384_000,
        },
    ),
]

# ============================================================================
# 聚合 + 参数化 / Aggregation & parametrization
# ============================================================================

ALL_MODELS = V41_FLASH_MODELS + ROUTED_LEGACY_MODELS + TEXT_ONLY_MODELS


@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name,expected",
    ALL_MODELS,
    ids=[m[0] for m in ALL_MODELS],
)
def test_model_metadata(model_name: str, expected: dict) -> None:  # type: ignore[type-arg]
    """验证 DeepSeek 模型元数据与官方文档一致。"""
    assert_model_metadata(model_name, expected)
