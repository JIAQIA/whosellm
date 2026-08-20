# filename: test_glm5v_turbo.py
# @Time    : 2026/8/20 11:00
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""GLM-5V-Turbo 视觉模型测试 / GLM-5V-Turbo vision model tests."""

from whosellm import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_specific_model_config, match_model_pattern
from whosellm.provider import Provider


class TestGLM5VTurboSpecificModel:
    """GLM-5V-Turbo specific_models 配置测试 / GLM-5V-Turbo specific_models config tests"""

    def test_glm5v_turbo_specific_config_exists(self) -> None:
        """验证 glm-5v-turbo specific_model 配置存在 / Validate glm-5v-turbo config exists"""
        config = get_specific_model_config("glm-5v-turbo")
        assert config is not None

        version, variant, capabilities = config
        assert version == "5.0"
        assert variant == "turbo"
        assert capabilities is not None

    def test_glm5v_turbo_specific_capabilities(self) -> None:
        """验证 glm-5v-turbo 能力与官方文档一致 / Validate glm-5v-turbo capabilities match official docs"""
        config = get_specific_model_config("glm-5v-turbo")
        assert config is not None
        _, _, capabilities = config

        assert capabilities is not None
        # 多模态 Coding 基座：图片/视频/文件输入 / Multimodal coding base: image/video/file input
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        assert capabilities.supports_vision is True
        assert capabilities.supports_video is True
        assert capabilities.supports_pdf is True
        assert capabilities.supports_streaming is True

        # 官方无结构化输出标注 / No structured output in official docs
        assert capabilities.supports_json_outputs is False
        assert capabilities.supports_structured_outputs is False

        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 200000

    def test_glm5v_turbo_date_suffix_patterns(self) -> None:
        """验证 glm-5v-turbo 日期后缀模式 / Validate glm-5v-turbo date suffix patterns"""
        for name in ("glm-5v-turbo-2026-08-01", "glm-5v-turbo-0801"):
            matched = match_model_pattern(name)
            assert matched is not None
            assert matched["family"] == ModelFamily.GLM_VISION
            assert matched["version"] == "5.0"
            assert matched["variant"] == "turbo"


class TestGLM5VTurboLLMetaIntegration:
    """GLM-5V-Turbo 端到端集成测试 / GLM-5V-Turbo end-to-end integration tests"""

    def test_glm5v_turbo_llmeta_basic(self) -> None:
        model = LLMeta("glm-5v-turbo")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM_VISION
        assert model.version == "5.0"
        assert model.variant == "turbo"
        assert model.capabilities.supports_vision is True
        assert model.capabilities.supports_video is True

    def test_glm5v_turbo_with_provider_prefix(self) -> None:
        model = LLMeta("zhipu::glm-5v-turbo")

        assert model.provider == Provider.ZHIPU
        assert model.family == ModelFamily.GLM_VISION
        assert model.version == "5.0"

    def test_glm5v_turbo_greater_than_glm46v(self) -> None:
        """验证版本排序：GLM-5V-Turbo > GLM-4.6V / Validate ordering: GLM-5V-Turbo > GLM-4.6V"""
        assert LLMeta("glm-5v-turbo") > LLMeta("glm-4.6v")
