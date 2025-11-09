# filename: test_deepseek.py
# @Time    : 2025/11/9 16:08
# @Author  : Cascade AI
"""
DeepSeek 模型家族测试 / DeepSeek model family tests
"""

from whosellm.models.base import ModelFamily
from whosellm.models.registry import (
    get_default_capabilities,
    get_specific_model_config,
    match_model_pattern,
)


def test_deepseek_default_capabilities() -> None:
    """验证 DeepSeek 家族默认能力 / Validate DeepSeek family default capabilities"""
    capabilities = get_default_capabilities(ModelFamily.DEEPSEEK)

    assert capabilities.supports_streaming is True
    assert capabilities.supports_function_calling is True
    assert capabilities.max_tokens == 8000
    assert capabilities.context_window == 128000
    assert capabilities.supports_thinking is False


def test_deepseek_chat_specific_model() -> None:
    """验证 deepseek-chat 特定模型配置 / Validate deepseek-chat specific configuration"""
    config = get_specific_model_config("deepseek-chat")

    assert config is not None
    version, variant, capabilities = config
    assert version == "1.0"
    assert variant == "chat"
    assert capabilities is not None
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_streaming is True
    assert capabilities.max_tokens == 8000
    assert capabilities.context_window == 128000


def test_deepseek_chat_pattern_matching() -> None:
    """验证 deepseek-chat 模式匹配 / Validate deepseek-chat pattern matching"""
    for name in ["deepseek-chat", "deepseek-chat-beta", "deepseek-chat-v3.2-exp"]:
        matched = match_model_pattern(name)

        assert matched is not None
        assert matched["family"] == ModelFamily.DEEPSEEK
        assert matched["variant"] == "chat"
        assert matched["version"] == "1.0"
        assert matched["_from_specific_model"] == "deepseek-chat"


def test_deepseek_reasoner_specific_model() -> None:
    """验证 deepseek-reasoner 特定模型配置 / Validate deepseek-reasoner specific configuration"""
    config = get_specific_model_config("deepseek-reasoner")

    assert config is not None
    version, variant, capabilities = config
    assert version == "1.0"
    assert variant == "reasoner"
    assert capabilities is not None
    assert capabilities.supports_thinking is True


def test_deepseek_base_pattern_without_variant() -> None:
    """验证无型号名称时的默认匹配 / Validate default match without explicit variant"""
    matched = match_model_pattern("deepseek")

    assert matched is not None
    assert matched["family"] == ModelFamily.DEEPSEEK
    assert matched["variant"] == "base"
    assert matched["version"] == "1.0"
    assert matched["capabilities"].supports_function_calling is True


def test_deepseek_reasoner_does_not_use_chat_capabilities() -> None:
    """验证 reasoner 不会意外继承 chat 的函数调用能力 / Ensure reasoner capabilities override family defaults"""
    matched = match_model_pattern("deepseek-reasoner")

    assert matched is not None
    assert matched["variant"] == "reasoner"
    assert matched["capabilities"].supports_function_calling is False
    assert matched["capabilities"].supports_thinking is True
