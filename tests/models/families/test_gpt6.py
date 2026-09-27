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


def test_gpt6_sol_model():
    """测试GPT-6 Sol模型（2026-09-22 发布，中档主力） / Test GPT-6 Sol model"""
    m = LLMeta("gpt-6-sol")
    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "sol"
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


def test_gpt6_luna_model():
    """测试GPT-6 Luna模型（2026-09-22 发布，低成本档） / Test GPT-6 Luna model"""
    m = LLMeta("gpt-6-luna")
    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "luna"
    # 与 sol/astra 同窗口同工具面 / Same window and tool surface as sol/astra
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


def test_gpt6_sol_snapshot():
    """测试带日期后缀的GPT-6 Sol / Test GPT-6 Sol with date suffix"""
    m = LLMeta("gpt-6-sol-2026-09-22")
    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "sol"
    assert m.release_date == date(2026, 9, 22)


def test_gpt6_luna_snapshot():
    """测试带日期后缀的GPT-6 Luna / Test GPT-6 Luna with date suffix"""
    m = LLMeta("gpt-6-luna-2026-09-22")
    assert m.family == ModelFamily.GPT
    assert m.version == "6.0"
    assert m.variant == "luna"
    assert m.release_date == date(2026, 9, 22)


def test_gpt6_media_count_limit():
    """测试GPT-6三档图片数量上限（版本级继承） / Test GPT-6 image count cap (version-level inherited)

    官方文档：单请求最多 1500 张图片
    Per docs: up to 1,500 images per request
    """
    for model_name in ("gpt-6-astra", "gpt-6-sol", "gpt-6-luna"):
        mcl = LLMeta(model_name).capabilities.media_count_limit
        assert mcl.get("image") == 1500, f"{model_name}: {mcl.get('image')}"
        assert mcl.count_mode == "per_type"


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


def test_gpt6_tier_ordering():
    """测试GPT-6天体档位优先级 / Test GPT-6 celestial tier priority

    官方档位：luna(0) 低成本 < sol(1) 中档主力 < astra(5) 旗舰
    Official tiers: luna(0) < sol(1) < astra(5)
    """
    luna = LLMeta("gpt-6-luna")
    sol = LLMeta("gpt-6-sol")
    astra = LLMeta("gpt-6-astra")

    assert luna < sol < astra


def test_gpt6_cross_version_ordering():
    """测试GPT-6与上一代跨版本排序 / Test GPT-6 cross-version ordering vs previous gen

    版本优先于档位：GPT-6 最低档的 luna 仍高于 GPT-5.6 最高档的 sol
    Version precedes tier: GPT-6 luna (lowest tier) still outranks GPT-5.6 sol
    """
    assert LLMeta("gpt-5.6-sol") < LLMeta("gpt-6-luna")
    assert LLMeta("gpt-5.5-pro") < LLMeta("gpt-6-luna")
