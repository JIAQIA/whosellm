# filename: test_glm5.py
# @Time    : 2026/3/12 14:00
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""GLM-5 模型家族测试 / GLM-5 model family tests."""

from datetime import date

from whosellm import LLMeta
from whosellm.models.base import ModelFamily, parse_date_from_model_name
from whosellm.models.registry import get_specific_model_config, match_model_pattern
from whosellm.provider import Provider


class TestGLM5SpecificModel:
    """GLM-5 specific_models 配置测试 / GLM-5 specific_models config tests"""

    def test_glm5_specific_config_exists(self) -> None:
        """验证 glm-5 specific_model 配置存在 / Validate glm-5 specific_model config exists"""
        config = get_specific_model_config("glm-5")
        assert config is not None

        version, variant, capabilities = config
        assert version == "5.0"
        assert variant == "base"
        assert capabilities is not None

    def test_glm5_specific_capabilities(self) -> None:
        """验证 glm-5 能力与官方文档一致 / Validate glm-5 capabilities match official docs"""
        config = get_specific_model_config("glm-5")
        assert config is not None
        _, _, capabilities = config

        assert capabilities is not None
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        assert capabilities.supports_structured_outputs is True
        assert capabilities.supports_streaming is True
        assert capabilities.supports_mcp is True
        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 200000

        # 明确断言不支持的能力 / Explicitly assert unsupported capabilities
        assert capabilities.supports_vision is False
        assert capabilities.supports_audio is False
        assert capabilities.supports_video is False


class TestGLM5PatternMatching:
    """GLM-5 模式匹配测试 / GLM-5 pattern matching tests"""

    def test_glm5_base_pattern(self) -> None:
        """验证基础 glm-5 模型匹配 / Validate base glm-5 model pattern"""
        matched = match_model_pattern("glm-5")

        assert matched is not None
        assert matched["family"] == ModelFamily.GLM_TEXT
        assert matched["provider"].value == "zhipu"
        assert matched["variant"] == "base"
        assert matched["version"] == "5.0"
        assert matched["_from_specific_model"] == "glm-5"

    def test_glm5_with_variant_pattern(self) -> None:
        """验证带变体的 glm-5 模型匹配 / Validate glm-5 with variant pattern"""
        matched = match_model_pattern("glm-5-flash")

        assert matched is not None
        assert matched["family"] == ModelFamily.GLM_TEXT
        assert matched["variant"] == "flash"
        assert matched["version"] == "5"

    def test_glm5_with_variant_and_date_pattern(self) -> None:
        """验证带变体和日期的 glm-5 模型匹配 / Validate glm-5 with variant and date"""
        matched = match_model_pattern("glm-5-plus-2026-03-01")

        assert matched is not None
        assert matched["family"] == ModelFamily.GLM_TEXT
        assert matched["variant"] == "plus"
        assert matched["version"] == "5"

        parsed_date = parse_date_from_model_name("glm-5-plus-2026-03-01")
        assert parsed_date == date(2026, 3, 1)

    def test_glm5_with_mmdd_suffix(self) -> None:
        """验证带 MMDD 日期后缀的匹配 / Validate MMDD date suffix pattern"""
        matched = match_model_pattern("glm-5-0212")

        assert matched is not None
        assert matched["family"] == ModelFamily.GLM_TEXT
        assert matched["version"] == "5"

        parsed_date = parse_date_from_model_name("glm-5-0212")
        assert parsed_date is not None
        assert parsed_date.month == 2
        assert parsed_date.day == 12


class TestGLM5LLMetaIntegration:
    """GLM-5 端到端集成测试 / GLM-5 end-to-end integration tests"""

    def test_glm5_llmeta_basic(self) -> None:
        """端到端：glm-5 → LLMeta 对象 / End-to-end: glm-5 → LLMeta object"""
        model = LLMeta("glm-5")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM_TEXT
        assert model.variant == "base"
        assert model.version == "5.0"
        assert model.capabilities.supports_thinking is True
        assert model.capabilities.supports_mcp is True
        assert model.capabilities.supports_function_calling is True

    def test_glm5_llmeta_with_provider_prefix(self) -> None:
        """端到端：带 Provider 前缀 / End-to-end: with Provider prefix"""
        model = LLMeta("zhipu::glm-5")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM_TEXT
        assert model.version == "5.0"

    def test_glm5_greater_than_glm47(self) -> None:
        """验证版本排序：GLM-5 > GLM-4.7 / Validate version ordering: GLM-5 > GLM-4.7"""
        glm5 = LLMeta("glm-5")
        glm47 = LLMeta("glm-4.7")

        assert glm5 > glm47

    def test_glm5_family_alias(self) -> None:
        """验证 ModelFamily.GLM_5 别名 / Validate ModelFamily.GLM_5 alias"""
        assert ModelFamily.GLM_5 == ModelFamily.GLM_TEXT
        assert ModelFamily.GLM_5.value == "glm-text"
