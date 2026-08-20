# filename: test_glm41v_thinking.py
# @Time    : 2026/8/20 11:00
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""GLM-4.1V-Thinking 系列测试（thinking/flash/flashx）/ GLM-4.1V-Thinking series tests."""

from whosellm import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_specific_model_config, match_model_pattern
from whosellm.provider import Provider

# 全系列模型 ID 与变体 / All series model IDs and variants
SERIES_MODELS = {
    "glm-4.1v-thinking": "thinking",
    "glm-4.1v-thinking-flash": "thinking-flash",
    "glm-4.1v-thinking-flashx": "thinking-flashx",
}


class TestGLM41VThinkingSpecificModels:
    """GLM-4.1V-Thinking specific_models 配置测试 / GLM-4.1V-Thinking specific_models config tests"""

    def test_all_series_configs_exist(self) -> None:
        """验证全系列 specific_model 配置存在 / Validate all series configs exist"""
        for name, variant in SERIES_MODELS.items():
            config = get_specific_model_config(name)
            assert config is not None, name

            version, parsed_variant, capabilities = config
            assert version == "4.1", name
            assert parsed_variant == variant, name
            assert capabilities is not None, name

    def test_series_capabilities(self) -> None:
        """验证系列能力与官方文档一致 / Validate series capabilities match official docs

        官方能力标注：内置深度思考（默认开）、视觉理解（图片/视频）、流式输出；
        无 Function Calling / 结构化输出标注。
        Official: built-in thinking (on by default), vision (image/video), streaming;
        no function calling / structured output.
        """
        for name in SERIES_MODELS:
            config = get_specific_model_config(name)
            assert config is not None, name
            _, _, capabilities = config

            assert capabilities is not None, name
            assert capabilities.supports_thinking is True, name
            assert capabilities.supports_vision is True, name
            assert capabilities.supports_video is True, name
            assert capabilities.supports_streaming is True, name

            assert capabilities.supports_function_calling is False, name
            assert capabilities.supports_json_outputs is False, name
            assert capabilities.supports_structured_outputs is False, name

            assert capabilities.context_window == 64000, name
            # 官方未标注最大输出 / Max output not documented

    def test_date_suffix_patterns(self) -> None:
        """验证日期后缀模式 / Validate date suffix patterns"""
        for name in SERIES_MODELS:
            for dated in (f"{name}-2025-08-08", f"{name}-0808"):
                matched = match_model_pattern(dated)
                assert matched is not None, dated
                assert matched["family"] == ModelFamily.GLM_VISION, dated
                assert matched["version"] == "4.1", dated


class TestGLM41VThinkingLLMetaIntegration:
    """GLM-4.1V-Thinking 端到端集成测试 / GLM-4.1V-Thinking end-to-end integration tests"""

    def test_llmeta_basic(self) -> None:
        model = LLMeta("glm-4.1v-thinking")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM_VISION
        assert model.version == "4.1"
        assert model.variant == "thinking"
        assert model.capabilities.supports_vision is True

    def test_llmeta_with_provider_prefix(self) -> None:
        model = LLMeta("zhipu::glm-4.1v-thinking-flash")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM_VISION
        assert model.version == "4.1"

    def test_variant_priority_ordering(self) -> None:
        """验证变体排序：flash < thinking < flashx / Validate variant ordering: flash < thinking < flashx"""
        assert LLMeta("glm-4.1v-thinking-flash") < LLMeta("glm-4.1v-thinking")
        assert LLMeta("glm-4.1v-thinking") < LLMeta("glm-4.1v-thinking-flashx")

    def test_version_ordering_against_46v(self) -> None:
        """验证版本排序：4.6V > 4.1V-Thinking 系列 / Validate ordering: 4.6V > 4.1V-Thinking series"""
        glm46v = LLMeta("glm-4.6v")
        for name in SERIES_MODELS:
            assert glm46v > LLMeta(name), name
