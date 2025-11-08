# filename: test_qwen.py
# @Time    : 2025/11/8 19:02
# @Author  : Cascade
"""
Qwen 模型家族测试 / Qwen model family tests
"""

from llmeta import LLMeta
from llmeta.models.base import ModelFamily
from llmeta.models.registry import get_specific_model_config, match_model_pattern


def test_qwen3_vl_plus_pattern_match() -> None:
    matched = match_model_pattern("qwen3-vl-plus")

    assert matched is not None
    assert matched["family"] == ModelFamily.QWEN
    assert matched["version"] == "3"
    assert matched["variant"] == "vl-plus"


def test_qwen3_vl_plus_specific_config() -> None:
    config = get_specific_model_config("qwen3-vl-plus")

    assert config is not None
    version, variant, capabilities = config
    assert version == "3"
    assert variant == "vl-plus"
    assert capabilities.supports_thinking is True
    assert capabilities.supports_vision is True
    assert capabilities.supports_video is True
    assert capabilities.context_window == 256000


def test_qwen3_vl_plus_auto_register() -> None:
    meta = LLMeta("qwen3-vl-plus")

    assert meta.family == ModelFamily.QWEN
    assert meta.version == "3"
    assert meta.variant == "vl-plus"
    assert meta.capabilities.context_window == 256000
    assert meta.capabilities.supports_video is True


def test_qwen3_vl_plus_with_date_suffix() -> None:
    meta = LLMeta("qwen3-vl-plus-2025-09-23")

    assert meta.family == ModelFamily.QWEN
    assert meta.version == "3"
    assert meta.variant == "vl-plus"
    assert meta.release_date.year == 2025
    assert meta.release_date.month == 9
    assert meta.release_date.day == 23
