# filename: test_glm53.py
# @Time    : 2026/8/20 11:00
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""GLM-5.x 文本系列测试（5.3/5.2/5.1/5-turbo）/ GLM-5.x text series tests."""

from whosellm import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_specific_model_config, match_model_pattern
from whosellm.provider import Provider


class TestGLM53SpecificModel:
    """GLM-5.3 specific_models 配置测试 / GLM-5.3 specific_models config tests"""

    def test_glm53_specific_config_exists(self) -> None:
        """验证 glm-5.3 specific_model 配置存在 / Validate glm-5.3 specific_model config exists"""
        config = get_specific_model_config("glm-5.3")
        assert config is not None

        version, variant, capabilities = config
        assert version == "5.3"
        assert variant == "base"
        assert capabilities is not None

    def test_glm53_specific_capabilities(self) -> None:
        """验证 glm-5.3 能力与官方文档一致 / Validate glm-5.3 capabilities match official docs"""
        config = get_specific_model_config("glm-5.3")
        assert config is not None
        _, _, capabilities = config

        assert capabilities is not None
        # 思考常开（low/high/max），不可禁用 / Always-on thinking, cannot be disabled
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        # 官方"结构化输出"为 json_object 模式 / Official "structured output" is json_object mode
        assert capabilities.supports_json_outputs is True
        assert capabilities.supports_structured_outputs is False
        assert capabilities.supports_streaming is True

        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 1000000  # 1M 上下文 / 1M context

        # 明确断言不支持的能力 / Explicitly assert unsupported capabilities
        assert capabilities.supports_vision is False
        assert capabilities.supports_audio is False
        assert capabilities.supports_video is False


class TestGLM5xSpecificCapabilities:
    """GLM-5.2/5.1/5-turbo 能力测试 / GLM-5.2/5.1/5-turbo capability tests"""

    def test_glm52_capabilities(self) -> None:
        """glm-5.2：1M 上下文，128K 输出 / glm-5.2: 1M context, 128K output"""
        config = get_specific_model_config("glm-5.2")
        assert config is not None
        version, variant, capabilities = config

        assert version == "5.2"
        assert variant == "base"
        assert capabilities is not None
        assert capabilities.context_window == 1000000
        assert capabilities.max_tokens == 128000
        assert capabilities.supports_json_outputs is True
        assert capabilities.supports_vision is False

    def test_glm51_capabilities(self) -> None:
        """glm-5.1：200K 上下文，128K 输出 / glm-5.1: 200K context, 128K output"""
        config = get_specific_model_config("glm-5.1")
        assert config is not None
        version, variant, capabilities = config

        assert version == "5.1"
        assert variant == "base"
        assert capabilities is not None
        assert capabilities.context_window == 200000
        assert capabilities.max_tokens == 128000
        assert capabilities.supports_json_outputs is True

    def test_glm5_turbo_capabilities(self) -> None:
        """glm-5-turbo：200K 上下文，turbo 变体 / glm-5-turbo: 200K context, turbo variant"""
        config = get_specific_model_config("glm-5-turbo")
        assert config is not None
        version, variant, capabilities = config

        assert version == "5.0"
        assert variant == "turbo"
        assert capabilities is not None
        assert capabilities.context_window == 200000
        assert capabilities.max_tokens == 128000
        assert capabilities.supports_json_outputs is True

    def test_glm5_turbo_with_date_pattern(self) -> None:
        """验证 glm-5-turbo 日期后缀模式 / Validate glm-5-turbo date suffix patterns"""
        for name in ("glm-5-turbo-2026-01-15", "glm-5-turbo-0115"):
            matched = match_model_pattern(name)
            assert matched is not None
            assert matched["family"] == ModelFamily.GLM
            assert matched["version"] == "5.0"
            assert matched["variant"] == "turbo"


class TestGLMJsonOutputsUpdate:
    """官方已为 GLM-4.5+ 标注结构化输出（json_object）/ Official docs now mark structured output (json_object) for GLM-4.5+"""

    def test_glm5_json_outputs(self) -> None:
        model = LLMeta("glm-5")
        assert model.capabilities.supports_json_outputs is True
        assert model.capabilities.supports_structured_outputs is False

    def test_glm47_json_outputs(self) -> None:
        model = LLMeta("glm-4.7")
        assert model.capabilities.supports_json_outputs is True

    def test_glm46_json_outputs(self) -> None:
        model = LLMeta("glm-4.6")
        assert model.capabilities.supports_json_outputs is True

    def test_glm45_json_outputs(self) -> None:
        model = LLMeta("glm-4.5")
        assert model.capabilities.supports_json_outputs is True

    def test_glm46v_not_json_outputs(self) -> None:
        """glm-4.6v 官方无结构化输出标注 / glm-4.6v has no structured output in official docs"""
        model = LLMeta("glm-4.6v")
        assert model.capabilities.supports_json_outputs is False


class TestGLM5xOrdering:
    """GLM-5.x 版本排序测试 / GLM-5.x version ordering tests"""

    def test_glm5x_full_chain(self) -> None:
        """验证 5.3 > 5.2 > 5.1 > 5 > 5-turbo / Validate 5.3 > 5.2 > 5.1 > 5 > 5-turbo"""
        assert LLMeta("glm-5.3") > LLMeta("glm-5.2") > LLMeta("glm-5.1") > LLMeta("glm-5") > LLMeta("glm-5-turbo")

    def test_glm53_greater_than_glm47(self) -> None:
        assert LLMeta("glm-5.3") > LLMeta("glm-4.7")

    def test_version_beats_variant(self) -> None:
        """版本优先于变体：4.7 < 5-turbo / Version beats variant: 4.7 < 5-turbo"""
        assert LLMeta("glm-4.7") < LLMeta("glm-5-turbo")


class TestGLM5xLLMetaIntegration:
    """GLM-5.x 端到端集成测试 / GLM-5.x end-to-end integration tests"""

    def test_glm53_llmeta_basic(self) -> None:
        model = LLMeta("glm-5.3")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM
        assert model.version == "5.3"
        assert model.variant == "base"
        assert model.capabilities.context_window == 1000000

    def test_glm53_with_provider_prefix(self) -> None:
        model = LLMeta("zhipu::glm-5.3")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM
        assert model.version == "5.3"

    def test_glm5_turbo_llmeta(self) -> None:
        model = LLMeta("glm-5-turbo")

        assert model.family == ModelFamily.GLM
        assert model.version == "5.0"
        assert model.variant == "turbo"
