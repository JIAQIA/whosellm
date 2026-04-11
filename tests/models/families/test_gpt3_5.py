"""
GPT-3.5 模型家族测试 / GPT-3.5 model family tests

验证三级继承：gpt-3.5-turbo (specific_model, caps=None) → version_caps["3.5"] → family default
"""

from whosellm import LLMeta
from whosellm.models.base import ModelFamily, get_model_info


def test_gpt3_5_turbo_capabilities():
    """测试 GPT-3.5-turbo capabilities 继承自版本级配置 / Test GPT-3.5-turbo capabilities inherited from version-level config"""
    info = get_model_info("gpt-3.5-turbo")

    assert info.family == ModelFamily.GPT
    assert info.version == "3.5"
    assert info.variant == "turbo"

    # 版本级 caps (ctx=16385, max_tokens=4096)，而非 family default (ctx=1,050,000, max_tokens=128,000)
    assert info.capabilities.context_window == 16_385
    assert info.capabilities.max_tokens == 4096
    assert info.capabilities.supports_thinking is False
    assert info.capabilities.supports_function_calling is False
    assert info.capabilities.supports_streaming is False


def test_gpt3_5_turbo_llmeta():
    """测试通过 LLMeta 入口获取 GPT-3.5-turbo / Test GPT-3.5-turbo via LLMeta entry point"""
    m = LLMeta("gpt-3.5-turbo")

    assert m.family == ModelFamily.GPT
    assert m.version == "3.5"
    assert m.variant == "turbo"
    assert m.capabilities.context_window == 16_385
    assert m.capabilities.max_tokens == 4096
