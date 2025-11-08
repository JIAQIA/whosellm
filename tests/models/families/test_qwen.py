# filename: test_qwen.py
# @Time    : 2025/11/8 19:02
# @Author  : Cascade
"""
Qwen 模型家族测试 / Qwen model family tests
"""

from datetime import date

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


def test_qwen3_max_pattern_match() -> None:
    matched = match_model_pattern("qwen3-max")

    assert matched is not None
    assert matched["family"] == ModelFamily.QWEN
    assert matched["version"] == "3"
    assert matched["variant"] == "max"


def test_qwen3_max_specific_config() -> None:
    config = get_specific_model_config("qwen3-max")

    assert config is not None
    version, variant, capabilities = config
    assert version == "3"
    assert variant == "max"
    assert capabilities.context_window == 256000
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_structured_outputs is True


def test_qwen3_max_auto_register() -> None:
    meta = LLMeta("qwen3-max")

    assert meta.family == ModelFamily.QWEN
    assert meta.version == "3"
    assert meta.variant == "max"
    assert meta.capabilities.context_window == 256000
    assert meta.capabilities.supports_function_calling is True


def test_qwen3_max_general_pattern_isolated() -> None:
    meta = LLMeta("qwen-max")

    assert meta.family == ModelFamily.QWEN
    assert meta.variant == "max"
    assert meta.capabilities.context_window == 32000


def test_qwen3_max_preview_pattern_match() -> None:
    matched = match_model_pattern("qwen3-max-preview")

    assert matched is not None
    assert matched["family"] == ModelFamily.QWEN
    assert matched["version"] == "3"
    assert matched["variant"] == "max-preview"


def test_qwen3_max_preview_specific_config() -> None:
    config = get_specific_model_config("qwen3-max-preview")

    assert config is not None
    version, variant, capabilities = config
    assert version == "3"
    assert variant == "max-preview"
    assert capabilities.supports_thinking is True
    assert capabilities.context_window == 256000
    assert capabilities.max_tokens == 64000


def test_qwen3_max_preview_auto_register() -> None:
    meta = LLMeta("qwen3-max-preview")

    assert meta.family == ModelFamily.QWEN
    assert meta.version == "3"
    assert meta.variant == "max-preview"
    assert meta.capabilities.supports_thinking is True
    assert meta.capabilities.context_window == 256000
    assert meta.capabilities.max_tokens == 64000


def test_qwen3_max_preview_general_pattern_isolated() -> None:
    meta = LLMeta("qwen-max-preview")

    assert meta.family == ModelFamily.QWEN
    assert meta.variant == "max-preview"
    assert meta.capabilities.supports_thinking is False


def test_qwen3_max_preview_with_date_suffix() -> None:
    meta = LLMeta("qwen3-max-preview-2025-09-23")

    assert meta.family == ModelFamily.QWEN
    assert meta.variant == "max-preview"
    assert meta.release_date == date(2025, 9, 23)


def test_qwen3_max_snapshot_pattern_match() -> None:
    matched = match_model_pattern("qwen3-max-2025-09-23")

    assert matched is not None
    assert matched["family"] == ModelFamily.QWEN
    assert matched["variant"] == "max"
    assert matched["version"] == "3"
    # specific_model 匹配不会保留年月日字段


def test_qwen3_max_snapshot_specific_config() -> None:
    config = get_specific_model_config("qwen3-max-2025-09-23")

    assert config is not None
    version, variant, capabilities = config
    assert version == "3"
    assert variant == "max"
    assert capabilities.context_window == 256000
    assert capabilities.max_tokens == 32000


def test_qwen3_max_snapshot_auto_register() -> None:
    meta = LLMeta("qwen3-max-2025-09-23")

    assert meta.family == ModelFamily.QWEN
    assert meta.version == "3"
    assert meta.variant == "max"
    assert meta.capabilities.context_window == 256000
    assert meta.capabilities.max_tokens == 32000


def test_qwen3_max_snapshot_date_inference() -> None:
    meta = LLMeta("qwen3-max-2025-09-23")

    assert meta.release_date == date(2025, 9, 23)


def test_qwen_image_plus_pattern_match() -> None:
    matched = match_model_pattern("qwen-image-plus")

    assert matched is not None
    assert matched["family"] == ModelFamily.QWEN
    assert matched["variant"] == "image-plus"
    assert matched["version"] == "1.0"


def test_qwen_image_plus_specific_config() -> None:
    config = get_specific_model_config("qwen-image-plus")

    assert config is not None
    version, variant, capabilities = config
    assert version == "1.0"
    assert variant == "image-plus"
    assert capabilities.supports_vision is True
    assert capabilities.supports_function_calling is False
    assert capabilities.supports_structured_outputs is False
    assert capabilities.supports_streaming is False


def test_qwen_image_plus_auto_register() -> None:
    meta = LLMeta("qwen-image-plus")

    assert meta.family == ModelFamily.QWEN
    assert meta.variant == "image-plus"
    assert meta.capabilities.supports_vision is True
    assert meta.capabilities.supports_function_calling is False


def test_qwen_image_general_pattern_intact() -> None:
    meta = LLMeta("qwen-image")

    assert meta.family == ModelFamily.QWEN
    assert meta.variant == "image"
    assert meta.capabilities.supports_function_calling is False
    assert meta.capabilities.supports_structured_outputs is False
    assert meta.capabilities.supports_streaming is False
