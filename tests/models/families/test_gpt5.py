# filename: test_gpt5.py
# @Time    : 2025/11/7 16:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
GPT-5 模型家族测试 / GPT-5 model family tests
"""

from datetime import date

import pytest

from whosellm import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_specific_model_config, match_model_pattern

# ============================================================================
# GPT-5 基础模型测试 / GPT-5 Base Model Tests
# ============================================================================


def test_gpt5_base_model():
    """测试基础GPT-5模型 / Test base GPT-5 model"""
    matched = match_model_pattern("gpt-5")

    assert matched is not None
    assert matched["family"] == ModelFamily.GPT_5
    assert matched["version"] == "5.0"
    assert matched["variant"] == "base"


def test_gpt5_base_capabilities():
    """测试GPT-5基础模型能力 / Test GPT-5 base model capabilities"""
    m = LLMeta("gpt-5")
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_vision is True
    assert m.capabilities.supports_pdf is True
    assert m.capabilities.supports_function_calling is True
    assert m.capabilities.supports_streaming is True
    assert m.capabilities.supports_structured_outputs is True
    assert m.capabilities.supports_fine_tuning is False
    assert m.capabilities.supports_distillation is True
    assert m.capabilities.supports_web_search is True
    assert m.capabilities.supports_file_search is True
    assert m.capabilities.supports_image_generation is True
    assert m.capabilities.supports_code_interpreter is True
    assert m.capabilities.supports_mcp is True
    assert m.capabilities.max_tokens == 128_000
    assert m.capabilities.context_window == 400_000


def test_gpt5_base_with_date_suffix():
    """测试带日期的GPT-5基础模型 / Test GPT-5 base with date suffix"""
    matched = match_model_pattern("gpt-5-2025-08-07")
    assert matched is not None
    assert matched["family"] == ModelFamily.GPT_5
    assert matched["variant"] == "base"

    from whosellm.models.base import parse_date_from_model_name

    parsed_date = parse_date_from_model_name("gpt-5-2025-08-07")
    assert parsed_date == date(2025, 8, 7)


# ============================================================================
# GPT-5 变体测试 / GPT-5 Variant Tests
# ============================================================================


def test_gpt5_mini_model():
    """测试GPT-5 mini变体 / Test GPT-5 mini variant"""
    config = get_specific_model_config("gpt-5-mini")
    assert config is not None
    version, variant, capabilities = config
    assert version == "5.0"
    assert variant == "mini"
    assert capabilities is not None
    assert capabilities.max_tokens == 128_000
    assert capabilities.context_window == 400_000
    assert capabilities.supports_thinking is True
    assert capabilities.supports_vision is True
    assert capabilities.supports_pdf is True
    assert capabilities.supports_distillation is False
    assert capabilities.supports_image_generation is False


def test_gpt5_nano_model():
    """测试GPT-5 nano变体 / Test GPT-5 nano variant"""
    config = get_specific_model_config("gpt-5-nano")
    assert config is not None
    version, variant, capabilities = config
    assert version == "5.0"
    assert variant == "nano"
    assert capabilities is not None
    assert capabilities.max_tokens == 16_384
    assert capabilities.context_window == 128_000
    assert capabilities.supports_thinking is True
    assert capabilities.supports_distillation is False


def test_gpt5_pro_model():
    """测试GPT-5 Pro变体 / Test GPT-5 pro variant"""
    config = get_specific_model_config("gpt-5-pro")
    assert config is not None
    version, variant, capabilities = config
    assert version == "5.0"
    assert variant == "pro"
    assert capabilities is not None
    assert capabilities.max_tokens == 128_000
    assert capabilities.context_window == 400_000
    assert capabilities.supports_computer_use is True


def test_gpt5_mini_with_date_suffix():
    """测试带日期后缀的GPT-5 mini / Test GPT-5 mini with date suffix"""
    matched = match_model_pattern("gpt-5-mini-2025-08-07")
    assert matched is not None
    assert matched["variant"] == "mini"

    from whosellm.models.base import parse_date_from_model_name

    parsed_date = parse_date_from_model_name("gpt-5-mini-2025-08-07")
    assert parsed_date == date(2025, 8, 7)


def test_gpt5_pro_with_date_suffix():
    """测试带日期的GPT-5 Pro模型 / Test GPT-5 pro with date suffix"""
    matched = match_model_pattern("gpt-5-pro-2025-10-06")
    assert matched is not None
    assert matched["variant"] == "pro"

    from whosellm.models.base import parse_date_from_model_name

    parsed_date = parse_date_from_model_name("gpt-5-pro-2025-10-06")
    assert parsed_date == date(2025, 10, 6)


# ============================================================================
# GPT-5.1 测试 / GPT-5.1 Tests
# ============================================================================


def test_gpt5_1_model():
    """测试GPT-5.1模型 / Test GPT-5.1 model"""
    m = LLMeta("gpt-5.1")
    assert m.family == ModelFamily.GPT_5_1
    assert m.version == "5.1"
    assert m.variant == "base"
    assert m.capabilities.context_window == 1_050_000
    assert m.capabilities.max_tokens == 128_000


# ============================================================================
# GPT-5.2 测试 / GPT-5.2 Tests
# ============================================================================


def test_gpt5_2_model():
    """测试GPT-5.2模型 / Test GPT-5.2 model"""
    m = LLMeta("gpt-5.2")
    assert m.family == ModelFamily.GPT_5_2
    assert m.version == "5.2"
    assert m.variant == "base"
    assert m.capabilities.context_window == 1_050_000


def test_gpt5_2_pro_model():
    """测试GPT-5.2-pro模型 / Test GPT-5.2-pro model"""
    m = LLMeta("gpt-5.2-pro")
    assert m.family == ModelFamily.GPT_5_2
    assert m.version == "5.2"
    assert m.variant == "pro"
    assert m.capabilities.supports_computer_use is True


# ============================================================================
# GPT-5.4 测试 / GPT-5.4 Tests (当前旗舰 / Current flagship)
# ============================================================================


def test_gpt5_4_model():
    """测试GPT-5.4模型（当前旗舰）/ Test GPT-5.4 model (current flagship)"""
    m = LLMeta("gpt-5.4")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "base"
    assert m.capabilities.context_window == 1_050_000
    assert m.capabilities.max_tokens == 128_000
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_vision is True
    assert m.capabilities.supports_computer_use is True
    assert m.capabilities.supports_mcp is True


def test_gpt5_4_with_date_suffix():
    """测试带日期的GPT-5.4模型 / Test GPT-5.4 with date suffix"""
    m = LLMeta("gpt-5.4-2026-03-05")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "base"
    assert m.release_date == date(2026, 3, 5)


def test_gpt5_4_pro_model():
    """测试GPT-5.4-pro模型 / Test GPT-5.4-pro model"""
    m = LLMeta("gpt-5.4-pro")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "pro"
    assert m.capabilities.supports_computer_use is True


def test_gpt5_4_pro_with_date_suffix():
    """测试带日期的GPT-5.4-pro模型 / Test GPT-5.4-pro with date suffix"""
    m = LLMeta("gpt-5.4-pro-2026-03-05")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "pro"
    assert m.release_date == date(2026, 3, 5)


def test_gpt5_4_mini_model():
    """测试GPT-5.4-mini模型 / Test GPT-5.4-mini model"""
    m = LLMeta("gpt-5.4-mini")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "mini"
    assert m.capabilities.context_window == 400_000
    assert m.capabilities.max_tokens == 128_000
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_vision is True
    assert m.capabilities.supports_function_calling is True
    assert m.capabilities.supports_streaming is True
    assert m.capabilities.supports_structured_outputs is True
    assert m.capabilities.supports_fine_tuning is False
    assert m.capabilities.supports_distillation is True
    assert m.capabilities.supports_computer_use is True
    assert m.capabilities.supports_mcp is True


def test_gpt5_4_mini_with_date_suffix():
    """测试带日期的GPT-5.4-mini模型 / Test GPT-5.4-mini with date suffix"""
    m = LLMeta("gpt-5.4-mini-2026-03-17")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "mini"
    assert m.release_date == date(2026, 3, 17)


def test_gpt5_4_nano_model():
    """测试GPT-5.4-nano模型 / Test GPT-5.4-nano model"""
    m = LLMeta("gpt-5.4-nano")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "nano"
    assert m.capabilities.context_window == 400_000
    assert m.capabilities.max_tokens == 128_000
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_vision is True
    assert m.capabilities.supports_function_calling is True
    assert m.capabilities.supports_streaming is True
    assert m.capabilities.supports_structured_outputs is True
    assert m.capabilities.supports_fine_tuning is False
    assert m.capabilities.supports_distillation is True
    assert m.capabilities.supports_computer_use is False
    assert m.capabilities.supports_mcp is True


def test_gpt5_4_nano_with_date_suffix():
    """测试带日期的GPT-5.4-nano模型 / Test GPT-5.4-nano with date suffix"""
    m = LLMeta("gpt-5.4-nano-2026-03-17")
    assert m.family == ModelFamily.GPT_5_4
    assert m.version == "5.4"
    assert m.variant == "nano"
    assert m.release_date == date(2026, 3, 17)


# ============================================================================
# GPT-5 Codex 系列测试 / GPT-5 Codex Series Tests
# ============================================================================


def test_gpt5_codex_model():
    """测试GPT-5 Codex模型 / Test GPT-5 Codex model"""
    m = LLMeta("gpt-5-codex")
    assert m.family == ModelFamily.GPT_5
    assert m.version == "5.0"
    assert m.variant == "codex"
    assert m.capabilities.supports_thinking is True
    assert m.capabilities.supports_vision is False


def test_gpt5_1_codex_model():
    """测试GPT-5.1 Codex模型 / Test GPT-5.1 Codex model"""
    m = LLMeta("gpt-5.1-codex")
    assert m.family == ModelFamily.GPT_5_1
    assert m.version == "5.1"
    assert m.variant == "codex"


def test_gpt5_1_codex_mini_model():
    """测试GPT-5.1 Codex mini模型 / Test GPT-5.1 Codex mini model"""
    m = LLMeta("gpt-5.1-codex-mini")
    assert m.family == ModelFamily.GPT_5_1
    assert m.version == "5.1"
    assert m.variant == "codex-mini"


def test_gpt5_3_codex_model():
    """测试GPT-5.3 Codex模型 / Test GPT-5.3 Codex model"""
    m = LLMeta("gpt-5.3-codex")
    assert m.family == ModelFamily.GPT_5_3
    assert m.version == "5.3"
    assert m.variant == "codex"


# ============================================================================
# GPT-5 变体优先级测试 / GPT-5 Variant Priority Tests
# ============================================================================


def test_gpt5_variant_priority():
    """测试GPT-5变体优先级 / Test GPT-5 variant priority"""
    mini = LLMeta("gpt-5-mini")
    base = LLMeta("gpt-5")
    pro = LLMeta("gpt-5-pro")

    assert mini < base
    assert base < pro


def test_gpt5_4_variant_priority():
    """测试GPT-5.4变体优先级 / Test GPT-5.4 variant priority"""
    nano = LLMeta("gpt-5.4-nano")
    mini = LLMeta("gpt-5.4-mini")
    base = LLMeta("gpt-5.4")
    pro = LLMeta("gpt-5.4-pro")

    assert nano < base
    assert mini < base
    assert base < pro


# ============================================================================
# 参数化测试 / Parametrized Tests
# ============================================================================


@pytest.mark.parametrize(
    "model_name,expected_family,expected_version,expected_variant",
    [
        ("gpt-5", ModelFamily.GPT_5, "5.0", "base"),
        ("gpt-5-mini", ModelFamily.GPT_5, "5.0", "mini"),
        ("gpt-5-nano", ModelFamily.GPT_5, "5.0", "nano"),
        ("gpt-5-pro", ModelFamily.GPT_5, "5.0", "pro"),
        ("gpt-5-codex", ModelFamily.GPT_5, "5.0", "codex"),
        ("gpt-5.1", ModelFamily.GPT_5_1, "5.1", "base"),
        ("gpt-5.1-codex", ModelFamily.GPT_5_1, "5.1", "codex"),
        ("gpt-5.1-codex-mini", ModelFamily.GPT_5_1, "5.1", "codex-mini"),
        ("gpt-5.2", ModelFamily.GPT_5_2, "5.2", "base"),
        ("gpt-5.2-pro", ModelFamily.GPT_5_2, "5.2", "pro"),
        ("gpt-5.3-codex", ModelFamily.GPT_5_3, "5.3", "codex"),
        ("gpt-5.4", ModelFamily.GPT_5_4, "5.4", "base"),
        ("gpt-5.4-pro", ModelFamily.GPT_5_4, "5.4", "pro"),
        ("gpt-5.4-mini", ModelFamily.GPT_5_4, "5.4", "mini"),
        ("gpt-5.4-nano", ModelFamily.GPT_5_4, "5.4", "nano"),
    ],
)
def test_gpt5_family_version_variant(model_name, expected_family, expected_version, expected_variant):
    """参数化测试GPT-5系列家族、版本和变体解析"""
    m = LLMeta(model_name)
    assert m.family == expected_family
    assert m.version == expected_version
    assert m.variant == expected_variant


@pytest.mark.parametrize(
    "model_name,expected_ctx",
    [
        ("gpt-5", 400_000),
        ("gpt-5-mini", 400_000),
        ("gpt-5-nano", 128_000),
        ("gpt-5.1", 1_050_000),
        ("gpt-5.2", 1_050_000),
        ("gpt-5.4", 1_050_000),
        ("gpt-5.4-mini", 400_000),
        ("gpt-5.4-nano", 400_000),
    ],
)
def test_gpt5_context_window(model_name, expected_ctx):
    """参数化测试GPT-5上下文窗口 / Parametrized test for GPT-5 context window"""
    m = LLMeta(model_name)
    assert m.capabilities.context_window == expected_ctx
