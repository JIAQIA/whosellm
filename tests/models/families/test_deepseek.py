# filename: test_deepseek.py
# @Time    : 2025/11/9 16:08
# @Author  : Cascade AI
"""
DeepSeek 模型家族测试 / DeepSeek model family tests
"""

from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_specific_model_config
from whosellm.provider import Provider


def test_deepseek_default_capabilities() -> None:
    """验证 DeepSeek 官方家族默认能力（V4 基线） / Validate DeepSeek official family default capabilities (V4 baseline)"""
    from whosellm import LLMeta

    # 使用官方 Provider 前缀确保获取官方配置
    model = LLMeta("deepseek::deepseek-chat")
    capabilities = model.capabilities

    assert capabilities.supports_streaming is True
    assert capabilities.supports_function_calling is True
    # V4 系列：1M 上下文，384K 最大输出
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000
    # deepseek-chat 是 v4-flash 非思考模式的别名
    assert capabilities.supports_thinking is False


def test_deepseek_chat_specific_model() -> None:
    """验证 deepseek-chat 特定模型配置 / Validate deepseek-chat specific configuration"""
    config = get_specific_model_config("deepseek-chat")

    assert config is not None
    version, variant, capabilities = config
    assert version == "4.0"
    assert variant == "chat"
    assert capabilities is not None
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_streaming is True
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000


def test_deepseek_chat_pattern_matching() -> None:
    """验证 deepseek-chat 模式匹配 / Validate deepseek-chat pattern matching"""
    from whosellm import LLMeta

    for name in ["deepseek-chat", "deepseek-chat-beta", "deepseek-chat-v3.2-exp"]:
        # 使用 Provider 前缀确保匹配官方配置
        model = LLMeta(f"deepseek::{name}")

        assert model.family == ModelFamily.DEEPSEEK
        assert model.variant == "chat"
        assert model.version == "4.0"
        assert model.provider == Provider.DEEPSEEK


def test_deepseek_reasoner_specific_model() -> None:
    """验证 deepseek-reasoner 特定模型配置 / Validate deepseek-reasoner specific configuration"""
    config = get_specific_model_config("deepseek-reasoner")

    assert config is not None
    version, variant, capabilities = config
    assert version == "4.0"
    assert variant == "reasoner"
    assert capabilities is not None
    assert capabilities.supports_thinking is True
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000


def test_deepseek_base_pattern_without_variant() -> None:
    """验证无型号名称时的默认匹配 / Validate default match without explicit variant"""
    from whosellm import LLMeta

    # 使用 Provider 前缀确保匹配官方配置
    model = LLMeta("deepseek::deepseek-chat")

    assert model.family == ModelFamily.DEEPSEEK
    assert model.variant == "chat"
    assert model.version == "4.0"
    assert model.capabilities.supports_function_calling is True


def test_deepseek_reasoner_does_not_use_chat_capabilities() -> None:
    """验证 reasoner 不会意外继承 chat 的能力 / Ensure reasoner capabilities override family defaults"""
    from whosellm import LLMeta

    model = LLMeta("deepseek::deepseek-reasoner")

    assert model.variant == "reasoner"
    assert model.capabilities.supports_function_calling is True
    assert model.capabilities.supports_thinking is True


def test_deepseek_no_structured_outputs() -> None:
    """验证 DeepSeek 官方模型不支持 structured_outputs（仅支持 json_object）"""
    from whosellm import LLMeta

    for model_id in ["deepseek-chat", "deepseek-reasoner", "deepseek-v4-flash", "deepseek-v4-pro"]:
        model = LLMeta(f"deepseek::{model_id}")
        assert model.capabilities.supports_structured_outputs is False, (
            f"{model_id}: DeepSeek API 仅支持 response_format={{type:'json_object'}}，"
            "不支持 json_schema 类型，supports_structured_outputs 应为 False"
        )
        assert model.capabilities.supports_json_outputs is True, (
            f"{model_id}: DeepSeek API 支持 response_format={{type:'json_object'}}，supports_json_outputs 应为 True"
        )


def test_deepseek_v4_flash_specific_model() -> None:
    """验证 deepseek-v4-flash 特定模型配置 / Validate deepseek-v4-flash specific configuration"""
    from whosellm import LLMeta

    model = LLMeta("deepseek::deepseek-v4-flash")

    assert model.family == ModelFamily.DEEPSEEK
    assert model.provider == Provider.DEEPSEEK
    assert model.version == "4.0"
    assert model.variant == "flash"

    caps = model.capabilities
    assert caps.supports_thinking is True
    assert caps.supports_function_calling is True
    assert caps.supports_streaming is True
    assert caps.supports_json_outputs is True
    assert caps.supports_structured_outputs is False
    assert caps.max_tokens == 384_000
    assert caps.context_window == 1_000_000


def test_deepseek_v4_pro_specific_model() -> None:
    """验证 deepseek-v4-pro 特定模型配置 / Validate deepseek-v4-pro specific configuration"""
    from whosellm import LLMeta

    model = LLMeta("deepseek::deepseek-v4-pro")

    assert model.family == ModelFamily.DEEPSEEK
    assert model.provider == Provider.DEEPSEEK
    assert model.version == "4.0"
    assert model.variant == "pro"

    caps = model.capabilities
    assert caps.supports_thinking is True
    assert caps.supports_function_calling is True
    assert caps.max_tokens == 384_000
    assert caps.context_window == 1_000_000


def test_deepseek_v4_variant_ordering() -> None:
    """验证 v4-flash < v4-pro 的排序关系 / Validate v4-flash < v4-pro ordering"""
    from whosellm import LLMeta

    flash = LLMeta("deepseek::deepseek-v4-flash")
    pro = LLMeta("deepseek::deepseek-v4-pro")

    assert flash < pro


def test_deepseek_versioned_pattern_matches_official_family() -> None:
    """验证带版本号的 DS 模型名能被官方 family 识别 / Validate versioned DS names match the official family"""
    from whosellm import LLMeta

    # V4 是 DS 官方首次开放版本号命名的系列
    model = LLMeta("deepseek::deepseek-v4-flash")
    assert model.family == ModelFamily.DEEPSEEK
    assert model.provider == Provider.DEEPSEEK
    assert model.version == "4.0"

    # 带小数版本号也能匹配 family（即使当前没有 specific_model 条目）
    model_v32 = LLMeta("deepseek::deepseek-v3.2-exp")
    assert model_v32.family == ModelFamily.DEEPSEEK
    assert model_v32.provider == Provider.DEEPSEEK
    assert model_v32.version == "3.2"
    assert model_v32.variant == "exp"
