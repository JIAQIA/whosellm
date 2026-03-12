# filename: test_gemini.py
# @Time    : 2025/12/12 13:17
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Google Gemini 模型家族测试 / Google Gemini model family tests
"""

import pytest

from whosellm.model_version import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_default_capabilities, get_specific_model_config, match_model_pattern
from whosellm.provider import Provider


def test_gemini_family_defaults():
    """验证 Gemini 家族默认能力 / Validate Gemini family default capabilities"""
    capabilities = get_default_capabilities(ModelFamily.GEMINI)

    assert capabilities.supports_thinking is True
    assert capabilities.supports_vision is True
    assert capabilities.supports_audio is True
    assert capabilities.supports_video is True
    assert capabilities.supports_pdf is True
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_structured_outputs is True
    assert capabilities.supports_streaming is True
    assert capabilities.supports_code_interpreter is True
    assert capabilities.context_window == 1_048_576
    assert capabilities.max_tokens == 65_536


class TestGemini25Pro:
    """Gemini 2.5 Pro 测试 / Gemini 2.5 Pro tests"""

    def test_specific_model_config(self):
        config = get_specific_model_config("gemini-2.5-pro")
        assert config is not None
        version, variant, capabilities = config
        assert version == "2.5"
        assert variant == "pro"
        assert capabilities is not None
        assert capabilities.supports_thinking is True
        assert capabilities.supports_vision is True
        assert capabilities.supports_audio is True
        assert capabilities.supports_video is True
        assert capabilities.supports_pdf is True
        assert capabilities.context_window == 1_048_576
        assert capabilities.max_tokens == 65_536

    def test_pattern_match(self):
        matched = match_model_pattern("gemini-2.5-pro")
        assert matched is not None
        assert matched["family"] == ModelFamily.GEMINI
        assert matched["variant"] == "pro"
        assert matched["provider"] == Provider.GOOGLE


class TestGemini25Flash:
    """Gemini 2.5 Flash 测试 / Gemini 2.5 Flash tests"""

    def test_specific_model_config(self):
        config = get_specific_model_config("gemini-2.5-flash")
        assert config is not None
        version, variant, capabilities = config
        assert version == "2.5"
        assert variant == "flash"
        assert capabilities is not None
        assert capabilities.supports_thinking is True
        assert capabilities.supports_pdf is True

    def test_pattern_match(self):
        matched = match_model_pattern("gemini-2.5-flash")
        assert matched is not None
        assert matched["family"] == ModelFamily.GEMINI
        assert matched["variant"] == "flash"
        assert matched["provider"] == Provider.GOOGLE


class TestGemini25FlashLite:
    """Gemini 2.5 Flash Lite 测试 / Gemini 2.5 Flash Lite tests"""

    def test_specific_model_config(self):
        config = get_specific_model_config("gemini-2.5-flash-lite")
        assert config is not None
        version, variant, capabilities = config
        assert version == "2.5"
        assert variant == "flash-lite"
        assert capabilities is not None
        assert capabilities.supports_thinking is False
        assert capabilities.supports_code_interpreter is False

    def test_pattern_match(self):
        matched = match_model_pattern("gemini-2.5-flash-lite")
        assert matched is not None
        assert matched["family"] == ModelFamily.GEMINI
        assert matched["variant"] == "flash-lite"


class TestGemini3x:
    """Gemini 3.x 系列测试 / Gemini 3.x series tests"""

    def test_gemini_3_pro_preview(self):
        config = get_specific_model_config("gemini-3-pro-preview")
        assert config is not None
        version, variant, capabilities = config
        assert version == "3.0"
        assert variant == "pro"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_audio is True
        assert capabilities.supports_video is True
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        assert capabilities.max_tokens == 65_536
        assert capabilities.context_window == 1_048_576

    def test_gemini_3_pro_image_preview(self):
        config = get_specific_model_config("gemini-3-pro-image-preview")
        assert config is not None
        version, variant, capabilities = config
        assert version == "3.0"
        assert variant == "pro-image"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_image_generation is True
        assert capabilities.max_tokens == 32_768
        assert capabilities.context_window == 65_536

    def test_gemini_3_1_pro_preview(self):
        config = get_specific_model_config("gemini-3-1-pro-preview")
        assert config is not None
        version, variant, capabilities = config
        assert version == "3.1"
        assert variant == "pro"

    def test_gemini_3_1_flash_lite_preview(self):
        config = get_specific_model_config("gemini-3-1-flash-lite-preview")
        assert config is not None
        version, variant, capabilities = config
        assert version == "3.1"
        assert variant == "flash-lite"


class TestGemini20:
    """Gemini 2.0 系列测试 / Gemini 2.0 series tests"""

    def test_gemini_2_0_flash(self):
        config = get_specific_model_config("gemini-2.0-flash")
        assert config is not None
        version, variant, capabilities = config
        assert version == "2.0"
        assert variant == "flash"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.max_tokens == 8192
        assert capabilities.context_window == 1_048_576

    def test_gemini_2_0_flash_variants(self):
        for model_name in ["gemini-2.0-flash-001", "gemini-2.0-flash-exp"]:
            config = get_specific_model_config(model_name)
            assert config is not None
            version, variant, _ = config
            assert version == "2.0"
            assert variant == "flash"

    def test_gemini_2_0_flash_image(self):
        config = get_specific_model_config("gemini-2.0-flash-preview-image-generation")
        assert config is not None
        version, variant, capabilities = config
        assert version == "2.0"
        assert variant == "flash-image"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_image_generation is True

    def test_gemini_2_0_flash_lite(self):
        config = get_specific_model_config("gemini-2.0-flash-lite")
        assert config is not None
        version, variant, capabilities = config
        assert version == "2.0"
        assert variant == "flash-lite"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.max_tokens == 8192


class TestGeminiVersionComparison:
    """Gemini 版本比较测试 / Gemini version comparison tests"""

    def test_version_ordering(self):
        """验证 2.5 < 3.0 < 3.1 / Validate 2.5 < 3.0 < 3.1"""
        gemini_25 = LLMeta("gemini-2.5-flash")
        gemini_30 = LLMeta("gemini-3-pro-preview")
        gemini_31 = LLMeta("gemini-3-1-pro-preview")

        assert gemini_25 < gemini_30
        assert gemini_30 < gemini_31
        assert gemini_25 < gemini_31


class TestGeminiLLMeta:
    """Gemini LLMeta 端到端测试 / Gemini LLMeta end-to-end tests"""

    def test_gemini_25_pro_resolution(self):
        meta = LLMeta("gemini-2.5-pro")
        assert meta.provider == Provider.GOOGLE
        assert meta.family == ModelFamily.GEMINI
        assert meta.version == "2.5"
        assert meta.variant == "pro"

    def test_gemini_25_flash_resolution(self):
        meta = LLMeta("gemini-2.5-flash")
        assert meta.provider == Provider.GOOGLE
        assert meta.family == ModelFamily.GEMINI
        assert meta.version == "2.5"
        assert meta.variant == "flash"

    def test_gemini_3_1_pro_preview_resolution(self):
        meta = LLMeta("gemini-3-1-pro-preview")
        assert meta.provider == Provider.GOOGLE
        assert meta.family == ModelFamily.GEMINI
        assert meta.version == "3.1"
        assert meta.variant == "pro"


class TestGeminiParametrized:
    """参数化测试 / Parametrized tests"""

    @pytest.mark.parametrize(
        "model_name,expected_version,expected_variant",
        [
            ("gemini-2.5-pro", "2.5", "pro"),
            ("gemini-2.5-flash", "2.5", "flash"),
            ("gemini-2.5-flash-lite", "2.5", "flash-lite"),
            ("gemini-3-pro-preview", "3.0", "pro"),
            ("gemini-3-1-pro-preview", "3.1", "pro"),
            ("gemini-3-1-flash-lite-preview", "3.1", "flash-lite"),
        ],
    )
    def test_all_specific_models(self, model_name: str, expected_version: str, expected_variant: str):
        config = get_specific_model_config(model_name)
        assert config is not None
        version, variant, _ = config
        assert version == expected_version
        assert variant == expected_variant

    @pytest.mark.parametrize(
        "model_name,expected_tokens,expected_context",
        [
            ("gemini-3-pro-preview", 65_536, 1_048_576),
            ("gemini-3-pro-image-preview", 32_768, 65_536),
            ("gemini-2.5-flash", 65_536, 1_048_576),
            ("gemini-2.5-flash-lite", 65_536, 1_048_576),
            ("gemini-2.5-pro", 65_536, 1_048_576),
            ("gemini-2.0-flash", 8192, 1_048_576),
            ("gemini-2.0-flash-lite", 8192, 1_048_576),
        ],
    )
    def test_gemini_max_tokens_and_context(self, model_name, expected_tokens, expected_context):
        """参数化测试 Gemini 各型号的 max_tokens 和 context_window"""
        config = get_specific_model_config(model_name)
        assert config is not None
        assert config[2].max_tokens == expected_tokens
        assert config[2].context_window == expected_context
