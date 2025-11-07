# filename: test_model_version.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型版本测试 / Model version tests
"""

import unittest

import pytest

from llmeta import LLMeta, ModelFamily, Provider


class TestModelVersion(unittest.TestCase):
    """模型版本测试类 / Model version test class"""

    def test_init_from_string(self) -> None:
        """测试从字符串初始化 / Test initialization from string"""
        model = LLMeta("gpt-4")
        assert model.model_name == "gpt-4"
        assert model.provider == Provider.OPENAI

    def test_provider_detection(self) -> None:
        """测试提供商检测 / Test provider detection"""
        # OpenAI
        assert LLMeta("gpt-4").provider == Provider.OPENAI
        assert LLMeta("gpt-3.5-turbo").provider == Provider.OPENAI

        # 智谱 AI
        assert LLMeta("glm-4").provider == Provider.ZHIPU
        assert LLMeta("glm-4v-plus").provider == Provider.ZHIPU

    def test_version_comparison_same_family(self) -> None:
        """测试同一模型家族的版本比较 / Test version comparison for same family"""
        # 注意: GPT-4 和 GPT-3.5 是不同的家族，不能直接比较
        # Note: GPT-4 and GPT-3.5 are different families, cannot be compared directly
        # 我们改为测试同一家族不同型号的比较
        # We test comparison of different variants in the same family instead
        gpt4_base = LLMeta("gpt-4")
        gpt4_turbo = LLMeta("gpt-4-turbo")
        gpt4o = LLMeta("gpt-4o")
        gpt4o_mini = LLMeta("gpt-4o-mini")

        # 测试型号优先级比较: mini < base < turbo < omni
        # Test variant priority comparison: mini < base < turbo < omni
        assert gpt4o_mini < gpt4_base
        assert gpt4_base < gpt4_turbo
        assert gpt4_turbo < gpt4o
        assert gpt4o_mini < gpt4o

    def test_version_comparison_different_family_raises(self) -> None:
        """测试不同模型家族的版本比较应该抛出异常 / Test version comparison for different families should raise"""
        gpt4 = LLMeta("gpt-4")
        glm4 = LLMeta("glm-4")

        with pytest.raises(ValueError, match="无法比较不同模型家族的模型"):
            _ = gpt4 > glm4

    def test_capabilities(self) -> None:
        """测试能力检测 / Test capability detection"""
        # GPT-4 Turbo 支持视觉
        gpt4_turbo = LLMeta("gpt-4-turbo")
        assert gpt4_turbo.capabilities.supports_vision is True
        assert gpt4_turbo.supports_multimodal is True

        # GPT-3.5 不支持视觉
        gpt35 = LLMeta("gpt-3.5-turbo")
        assert gpt35.capabilities.supports_vision is False
        assert gpt35.supports_multimodal is False

    def test_zhipu_glm4v_capabilities(self) -> None:
        """测试智谱 GLM-4V 的能力 / Test Zhipu GLM-4V capabilities"""
        # GLM-4V-Plus
        glm4v_plus = LLMeta("glm-4v-plus")
        assert glm4v_plus.capabilities.supports_vision is True
        assert glm4v_plus.capabilities.supports_video is True
        assert glm4v_plus.capabilities.max_video_size_mb == 20.0
        assert glm4v_plus.capabilities.max_video_duration_seconds == 30

        # GLM-4V-Plus-0111
        glm4v_plus_0111 = LLMeta("glm-4v-plus-0111")
        assert glm4v_plus_0111.capabilities.max_video_size_mb == 200.0
        assert glm4v_plus_0111.capabilities.max_video_duration_seconds is None

        # GLM-4V-Flash 不支持 base64
        glm4v_flash = LLMeta("glm-4v-flash")
        assert glm4v_flash.capabilities.supports_image_base64 is False

    def test_thinking_models(self) -> None:
        """测试推理模型 / Test thinking models"""
        o1 = LLMeta("o1")
        assert o1.capabilities.supports_thinking is True
        assert o1.capabilities.supports_streaming is False

    def test_string_representation(self) -> None:
        """测试字符串表示 / Test string representation"""
        model = LLMeta("gpt-4")
        assert str(model) == "gpt-4"
        assert "ModelVersion" in repr(model)
        assert "gpt-4" in repr(model)

    def test_variant_priority_comparison(self) -> None:
        """测试型号优先级比较 / Test variant priority comparison"""
        # GLM-4 系列: flash < base < plus
        glm4_flash = LLMeta("glm-4-flash")
        glm4_base = LLMeta("glm-4")
        glm4_plus = LLMeta("glm-4-plus")

        assert glm4_flash < glm4_base
        assert glm4_base < glm4_plus
        assert glm4_flash < glm4_plus

        # GLM-4V 系列: flash < base < plus-0111 <= plus (plus 指向最新版)
        # GLM-4V series: flash < base < plus-0111 <= plus (plus points to latest)
        glm4v_flash = LLMeta("glm-4v-flash")
        glm4v_base = LLMeta("glm-4v")
        glm4v_plus = LLMeta("glm-4v-plus")
        glm4v_plus_0111 = LLMeta("glm-4v-plus-0111")

        assert glm4v_flash < glm4v_base
        assert glm4v_base < glm4v_plus
        # plus 是最新版，应该 >= 特定日期版本 / plus is latest, should be >= specific date version
        assert glm4v_plus >= glm4v_plus_0111

    def test_model_family_detection(self) -> None:
        """测试模型家族检测 / Test model family detection"""
        # GPT-4 家族
        gpt4 = LLMeta("gpt-4")
        gpt4_turbo = LLMeta("gpt-4-turbo")
        gpt4o = LLMeta("gpt-4o")

        assert gpt4.family == ModelFamily.GPT_4
        assert gpt4_turbo.family == ModelFamily.GPT_4
        assert gpt4o.family == ModelFamily.GPT_4

        # GLM-4 家族
        glm4 = LLMeta("glm-4")
        glm4_plus = LLMeta("glm-4-plus")

        assert glm4.family == ModelFamily.GLM_4
        assert glm4_plus.family == ModelFamily.GLM_4

        # GLM-4V 家族（与 GLM-4 不同）
        glm4v = LLMeta("glm-4v")
        assert glm4v.family == ModelFamily.GLM_4V
        assert glm4v.family != glm4.family

    def test_provider_prefix_syntax(self) -> None:
        """测试 Provider::ModelName 语法 / Test Provider::ModelName syntax"""
        # 测试 Provider::ModelName 语法
        model1 = LLMeta("openai::gpt-4")
        assert model1.provider == Provider.OPENAI
        assert model1.family == ModelFamily.GPT_4

        # 测试不同的Provider
        model2 = LLMeta("openai::gpt-4")
        assert model2.provider == Provider.OPENAI
        assert model2.family == ModelFamily.GPT_4

        # 测试普通语法（使用默认Provider）
        model3 = LLMeta("gpt-4")
        assert model3.provider == Provider.OPENAI
        assert model3.family == ModelFamily.GPT_4

    def test_same_model_different_providers(self) -> None:
        """测试同一模型不同Provider / Test same model with different providers"""
        # 假设 DeepSeek 模型可以由原厂或腾讯提供
        # Assume DeepSeek model can be provided by original or Tencent
        # 这里仅作为示例，实际需要在注册表中添加相应配置

        # 测试指定不同Provider时，provider字段不同但family相同
        model_openai = LLMeta("openai::gpt-4")
        model_default = LLMeta("gpt-4")

        assert model_openai.provider == Provider.OPENAI
        assert model_default.provider == Provider.OPENAI
        assert model_openai.family == model_default.family

    def test_release_date_parsing(self) -> None:
        """测试发布日期解析 / Test release date parsing"""
        from datetime import date

        # 测试 YYYY-MM-DD 格式
        model1 = LLMeta("gpt-4-turbo-2024-04-09")
        assert model1.release_date == date(2024, 4, 9)
        assert model1.family == ModelFamily.GPT_4
        assert model1.variant == "turbo"

        # 测试 MMDD 格式（假设为2024年）
        model2 = LLMeta("gpt-4-0125-preview")
        assert model2.release_date == date(2024, 1, 25)
        assert model2.family == ModelFamily.GPT_4

        model3 = LLMeta("gpt-4")
        assert model3.release_date is None

    def test_release_date_comparison(self) -> None:
        """测试发布日期比较 / Test release date comparison"""

        # 同一型号不同日期的比较
        model_old = LLMeta("gpt-4-turbo-2024-01-01")
        model_new = LLMeta("gpt-4-turbo-2024-04-09")

        assert model_old < model_new
        assert model_new > model_old
        assert model_old != model_new

        # 没有日期的模型认为是最新的（指向latest）
        model_no_date = LLMeta("gpt-4-turbo")
        model_with_date = LLMeta("gpt-4-turbo-2024-04-09")

        assert model_with_date < model_no_date  # 有日期的 < 无日期的（最新）
        assert model_no_date > model_with_date

    def test_complex_comparison_with_date(self) -> None:
        """测试复杂的版本、型号和日期比较 / Test complex version, variant and date comparison"""

        # 创建不同版本、型号和日期的模型
        gpt4_base_with_date = LLMeta("gpt-4-0125-preview")  # base, 2024-01-25
        gpt4_base_no_date = LLMeta("gpt-4")  # base, no date
        gpt4_turbo_with_date = LLMeta("gpt-4-turbo-2024-04-09")  # turbo, 2024-04-09
        gpt4_turbo_no_date = LLMeta("gpt-4-turbo")  # turbo, no date

        # 验证型号优先级
        assert gpt4_base_with_date._variant_priority == (1,)
        assert gpt4_turbo_with_date._variant_priority == (2,)

        # 不同型号：turbo > base，无论日期如何
        assert gpt4_base_with_date < gpt4_turbo_with_date
        assert gpt4_base_no_date < gpt4_turbo_no_date

        # 同一型号：有日期 < 无日期（无日期指向最新）
        assert gpt4_base_with_date < gpt4_base_no_date
        assert gpt4_turbo_with_date < gpt4_turbo_no_date

        # 测试完整的比较链
        # base(有日期) < base(无日期/最新) < turbo(有日期) < turbo(无日期/最新)
        assert gpt4_base_with_date < gpt4_base_no_date < gpt4_turbo_with_date < gpt4_turbo_no_date
