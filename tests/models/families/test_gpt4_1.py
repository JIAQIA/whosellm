# filename: test_gpt4_1.py
# @Time    : 2025/11/7 16:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
GPT-4.1 模型家族测试 / GPT-4.1 model family tests
"""

from whosellm.models.base import ModelFamily, get_model_info
from whosellm.models.registry import (
    get_specific_model_config,
    match_model_pattern,
)


def test_gpt4_1_base_model():
    """测试基础 GPT-4.1 模型 / Test base GPT-4.1 model"""
    matched = match_model_pattern("gpt-4.1-2025-04-14")

    assert matched is not None
    assert matched["family"] == ModelFamily.GPT
    assert matched["version"] == "4.1"
    assert matched["variant"] == "base"

    # capabilities=None 表示继承版本级默认值，通过 get_model_info 验证解析后的能力
    # capabilities=None means inheriting version-level default, verify resolved via get_model_info
    info = get_model_info("gpt-4.1-2025-04-14")
    assert info.capabilities.supports_vision is True
    assert info.capabilities.supports_streaming is True
    assert info.capabilities.supports_structured_outputs is True
    assert info.capabilities.supports_fine_tuning is True
    assert info.capabilities.supports_distillation is True
    # 区分 GPT-4.1 与 GPT-5.4 family default 的关键字段
    assert info.capabilities.supports_thinking is False
    assert info.capabilities.context_window == 1_047_576
    assert info.capabilities.max_tokens == 32768


def test_gpt4_1_mini_model_specific_config():
    """测试 GPT-4.1 mini 配置 / Test GPT-4.1 mini specific config"""
    config = get_specific_model_config("gpt-4.1-mini")

    assert config is not None
    version, variant, capabilities = config
    assert version == "4.1"
    assert variant == "mini"
    assert capabilities is not None
    assert capabilities.supports_vision is True
    assert capabilities.supports_streaming is True
    assert capabilities.supports_structured_outputs is True
    assert capabilities.supports_fine_tuning is True
    assert capabilities.supports_distillation is False
    assert capabilities.supports_predicted_outputs is True


def test_gpt4_1_nano_model_specific_config():
    """测试 GPT-4.1 nano 配置 / Test GPT-4.1 nano specific config"""
    config = get_specific_model_config("gpt-4.1-nano")

    assert config is not None
    version, variant, capabilities = config
    assert version == "4.1"
    assert variant == "nano"
    assert capabilities is not None
    assert capabilities.supports_vision is True
    assert capabilities.supports_streaming is True
    assert capabilities.supports_structured_outputs is True
    assert capabilities.supports_fine_tuning is True
    assert capabilities.supports_distillation is False
    assert capabilities.supports_predicted_outputs is True


def test_gpt4_1_mini_date_pattern():
    """测试带日期的 GPT-4.1 mini 模型 / Test dated GPT-4.1 mini model"""
    matched = match_model_pattern("gpt-4.1-mini-2025-04-14")

    assert matched is not None
    assert matched["variant"] == "mini"
    assert matched["version"] == "4.1"
    assert matched["family"] == ModelFamily.GPT
    assert matched["_from_specific_model"] == "gpt-4.1-mini"

    config = get_specific_model_config(matched["_from_specific_model"])
    assert config is not None
    _, variant, capabilities = config
    assert variant == "mini"
    assert capabilities.supports_vision is True
    assert capabilities.supports_predicted_outputs is True


def test_gpt4_1_parent_pattern_capabilities():
    """测试 parent pattern 匹配的 GPT-4.1 变体继承版本级 capabilities / Test parent pattern matched GPT-4.1 variant inherits version-level capabilities"""
    # gpt-4.1-turbo 不在 specific_models 中，通过 parent pattern 匹配
    info = get_model_info("gpt-4.1-turbo")

    assert info.family == ModelFamily.GPT
    assert info.version == "4.1"
    assert info.variant == "turbo"
    # 应继承 GPT-4.1 版本级 caps，而非 GPT-5.4 family default
    assert info.capabilities.supports_thinking is False
    assert info.capabilities.context_window == 1_047_576
    assert info.capabilities.max_tokens == 32768


def test_gpt4_1_nano_date_pattern():
    """测试带日期的 GPT-4.1 nano 模型 / Test dated GPT-4.1 nano model"""
    matched = match_model_pattern("gpt-4.1-nano-2025-04-14")

    assert matched is not None
    assert matched["variant"] == "nano"
    assert matched["family"] == ModelFamily.GPT
    assert matched["_from_specific_model"] == "gpt-4.1-nano"

    config = get_specific_model_config(matched["_from_specific_model"])
    assert config is not None
    _, variant, capabilities = config
    assert variant == "nano"
    assert capabilities.supports_vision is True
    assert capabilities.supports_predicted_outputs is True
