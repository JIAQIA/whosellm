# filename: test_model_version.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型版本测试 / Model version tests
"""

import pytest

from llmver import ModelVersion, Provider


class TestModelVersion:
    """模型版本测试类 / Model version test class"""

    def test_init_from_string(self) -> None:
        """测试从字符串初始化 / Test initialization from string"""
        model = ModelVersion("gpt-4")
        assert model.model_name == "gpt-4"
        assert model.provider == Provider.OPENAI

    def test_provider_detection(self) -> None:
        """测试提供商检测 / Test provider detection"""
        # OpenAI
        assert ModelVersion("gpt-4").provider == Provider.OPENAI
        assert ModelVersion("gpt-3.5-turbo").provider == Provider.OPENAI

        # 智谱 AI
        assert ModelVersion("glm-4").provider == Provider.ZHIPU
        assert ModelVersion("glm-4v-plus").provider == Provider.ZHIPU

    def test_version_comparison_same_provider(self) -> None:
        """测试同一提供商的版本比较 / Test version comparison for same provider"""
        gpt4 = ModelVersion("gpt-4")
        gpt35 = ModelVersion("gpt-3.5-turbo")

        assert gpt4 > gpt35
        assert gpt35 < gpt4
        assert gpt4 != gpt35

    def test_version_comparison_different_provider_raises(self) -> None:
        """测试不同提供商的版本比较应该抛出异常 / Test version comparison for different providers should raise"""
        gpt4 = ModelVersion("gpt-4")
        glm4 = ModelVersion("glm-4")

        with pytest.raises(ValueError, match="无法比较不同提供商的模型"):
            _ = gpt4 > glm4

    def test_capabilities(self) -> None:
        """测试能力检测 / Test capability detection"""
        # GPT-4 Turbo 支持视觉
        gpt4_turbo = ModelVersion("gpt-4-turbo")
        assert gpt4_turbo.capabilities.supports_vision is True
        assert gpt4_turbo.supports_multimodal is True

        # GPT-3.5 不支持视觉
        gpt35 = ModelVersion("gpt-3.5-turbo")
        assert gpt35.capabilities.supports_vision is False
        assert gpt35.supports_multimodal is False

    def test_zhipu_glm4v_capabilities(self) -> None:
        """测试智谱 GLM-4V 的能力 / Test Zhipu GLM-4V capabilities"""
        # GLM-4V-Plus
        glm4v_plus = ModelVersion("glm-4v-plus")
        assert glm4v_plus.capabilities.supports_vision is True
        assert glm4v_plus.capabilities.supports_video is True
        assert glm4v_plus.capabilities.max_video_size_mb == 20.0
        assert glm4v_plus.capabilities.max_video_duration_seconds == 30

        # GLM-4V-Plus-0111
        glm4v_plus_0111 = ModelVersion("glm-4v-plus-0111")
        assert glm4v_plus_0111.capabilities.max_video_size_mb == 200.0
        assert glm4v_plus_0111.capabilities.max_video_duration_seconds is None

        # GLM-4V-Flash 不支持 base64
        glm4v_flash = ModelVersion("glm-4v-flash")
        assert glm4v_flash.capabilities.supports_image_base64 is False

    def test_thinking_models(self) -> None:
        """测试推理模型 / Test thinking models"""
        o1 = ModelVersion("o1")
        assert o1.capabilities.supports_thinking is True
        assert o1.capabilities.supports_streaming is False

    def test_string_representation(self) -> None:
        """测试字符串表示 / Test string representation"""
        model = ModelVersion("gpt-4")
        assert str(model) == "gpt-4"
        assert "ModelVersion" in repr(model)
        assert "gpt-4" in repr(model)
