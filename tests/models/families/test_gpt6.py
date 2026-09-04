# filename: test_gpt6.py
# @Time    : 2026/09/04
# @Author  : JQQ
# @Email   : jiaqia@qknode.com
# @Software: PyCharm
"""
GPT-6 模型家族测试 / GPT-6 model family tests
"""

from datetime import date

from whosellm import LLMeta
from whosellm.models.base import ModelFamily

# ============================================================================
# GPT-6 Astra 测试 / GPT-6 Astra Tests
# ============================================================================


def test_gpt6_astra_model():
    """测试GPT-6 Astra模型（2026-09-04 发布，旗舰） / Test GPT-6 Astra model"""
    m = LLMeta("gpt-6-astra")
    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "astra"
    assert m.capabilities.context_window == 1_050_000
    assert m.capabilities.max_tokens == 128_000
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_vision is True
    assert m.capabilities.supports_function_calling is True
    assert m.capabilities.supports_streaming is True
    assert m.capabilities.supports_structured_outputs is True
    assert m.capabilities.supports_web_search is True
    assert m.capabilities.supports_file_search is True
    assert m.capabilities.supports_image_generation is True
    assert m.capabilities.supports_code_interpreter is True
    assert m.capabilities.supports_computer_use is True
    assert m.capabilities.supports_fine_tuning is False


def test_gpt6_astra_snapshot():
    """测试带日期后缀的GPT-6 Astra / Test GPT-6 Astra with date suffix"""
    m = LLMeta("gpt-6-astra-2026-09-04")
    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "astra"
    assert m.release_date == date(2026, 9, 4)


def test_gpt6_parent_pattern_inheritance():
    """测试 parent pattern 匹配的 GPT-6 变体继承版本级 capabilities
    Test parent pattern matched GPT-6 variant inherits version-level capabilities
    """
    m = LLMeta("gpt-6-turbo")

    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "turbo"
    # 应继承 GPT-6.0 版本级 caps，而非 family default
    assert m.capabilities.context_window == 1_050_000
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_computer_use is True


def test_gpt6_version_ordering():
    """测试GPT-6版本排序 / Test GPT-6 version ordering"""
    v56 = LLMeta("gpt-5.6")
    v60 = LLMeta("gpt-6-astra")

    assert v56 < v60
