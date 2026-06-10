# filename: test_anthropic.py
"""
Anthropic Claude 模型家族测试 / Anthropic Claude model family tests
"""

import pytest

from whosellm.model_version import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_default_capabilities, get_specific_model_config, match_model_pattern
from whosellm.provider import Provider


def test_claude_family_defaults():
    """验证 Claude 家族默认能力 / Validate Claude family default capabilities"""
    capabilities = get_default_capabilities(ModelFamily.CLAUDE)

    assert capabilities.supports_vision is True
    assert capabilities.supports_thinking is True
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_streaming is True
    assert capabilities.context_window == 200000
    assert capabilities.max_tokens == 64000


class TestClaudeOpus46:
    """Claude Opus 4.6 测试 / Claude Opus 4.6 tests"""

    def test_specific_model_config(self):
        """验证 claude-opus-4-6 配置 / Validate claude-opus-4-6 config"""
        config = get_specific_model_config("claude-opus-4-6")
        assert config is not None
        version, variant, capabilities = config
        assert version == "4.6"
        assert variant == "opus"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        assert capabilities.supports_streaming is True
        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 1000000

    def test_pattern_match(self):
        """验证 claude-opus-4-6 模式匹配 / Validate claude-opus-4-6 pattern match"""
        matched = match_model_pattern("claude-opus-4-6")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "opus"
        assert matched["provider"] == Provider.ANTHROPIC

    def test_pattern_with_snapshot(self):
        """验证带 snapshot 的 claude-opus-4-6 模式匹配 / Validate claude-opus-4-6 with snapshot"""
        matched = match_model_pattern("claude-opus-4-6-20260301")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "opus"
        assert matched["_from_specific_model"] == "claude-opus-4-6"

    def test_pattern_with_at_snapshot(self):
        """验证 @ 格式 snapshot / Validate @ format snapshot"""
        matched = match_model_pattern("claude-opus-4-6@20260301")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "opus"
        assert matched["_from_specific_model"] == "claude-opus-4-6"


class TestClaudeSonnet46:
    """Claude Sonnet 4.6 测试 / Claude Sonnet 4.6 tests"""

    def test_specific_model_config(self):
        """验证 claude-sonnet-4-6 配置 / Validate claude-sonnet-4-6 config"""
        config = get_specific_model_config("claude-sonnet-4-6")
        assert config is not None
        version, variant, capabilities = config
        assert version == "4.6"
        assert variant == "sonnet"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        assert capabilities.supports_streaming is True
        assert capabilities.max_tokens == 64000
        assert capabilities.context_window == 1000000

    def test_pattern_match(self):
        """验证 claude-sonnet-4-6 模式匹配 / Validate claude-sonnet-4-6 pattern match"""
        matched = match_model_pattern("claude-sonnet-4-6")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "sonnet"
        assert matched["provider"] == Provider.ANTHROPIC

    def test_pattern_with_snapshot(self):
        """验证带 snapshot 的 claude-sonnet-4-6 模式匹配 / Validate claude-sonnet-4-6 with snapshot"""
        matched = match_model_pattern("claude-sonnet-4-6-20260301")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "sonnet"
        assert matched["_from_specific_model"] == "claude-sonnet-4-6"

    def test_pattern_with_at_snapshot(self):
        """验证 @ 格式 snapshot / Validate @ format snapshot"""
        matched = match_model_pattern("claude-sonnet-4-6@20260301")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "sonnet"
        assert matched["_from_specific_model"] == "claude-sonnet-4-6"


class TestClaudeFable5:
    """Claude Fable 5 测试（Mythos-class，2026-06-09 GA） / Claude Fable 5 tests"""

    def test_specific_model_config(self):
        """验证 claude-fable-5 配置 / Validate claude-fable-5 config"""
        config = get_specific_model_config("claude-fable-5")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.0"
        assert variant == "fable"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_thinking is True
        assert capabilities.supports_function_calling is True
        assert capabilities.supports_streaming is True
        assert capabilities.supports_structured_outputs is True
        assert capabilities.supports_computer_use is True
        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 1000000

    def test_pattern_match(self):
        """验证 claude-fable-5 模式匹配 / Validate claude-fable-5 pattern match"""
        matched = match_model_pattern("claude-fable-5")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "fable"
        assert matched["provider"] == Provider.ANTHROPIC

    @pytest.mark.parametrize("model_name", ["claude-fable-5-20260609", "claude-fable-5@20260609"])
    def test_pattern_with_snapshot(self, model_name: str):
        """验证带 snapshot 的解析（- 与 @ 两种格式，版本号不被吞） / Validate snapshot forms keep version 5.0"""
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert meta.version == "5.0"
        assert meta.variant == "fable"


class TestClaudeMythos5:
    """Claude Mythos 5 测试（Glasswing 受邀版） / Claude Mythos 5 tests"""

    def test_specific_model_config(self):
        """验证 claude-mythos-5 配置 / Validate claude-mythos-5 config"""
        config = get_specific_model_config("claude-mythos-5")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.0"
        assert variant == "mythos"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_thinking is True
        assert capabilities.supports_structured_outputs is True
        assert capabilities.supports_computer_use is True
        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 1000000

    def test_pattern_match(self):
        """验证 claude-mythos-5 模式匹配 / Validate claude-mythos-5 pattern match"""
        matched = match_model_pattern("claude-mythos-5")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "mythos"
        assert matched["provider"] == Provider.ANTHROPIC


class TestClaudeMythosClassOrdering:
    """Mythos-class 版本比较：mythos > fable > opus > sonnet / Mythos-class ordering"""

    def test_fable5_outranks_opus48(self):
        """fable-5 (v5.0) 高于 opus-4-8 (v4.8) / fable-5 outranks opus-4-8 by version"""
        assert LLMeta("claude-fable-5") > LLMeta("claude-opus-4-8")

    def test_mythos5_outranks_fable5(self):
        """同版本下 mythos 变体优先级高于 fable / mythos outranks fable on variant priority"""
        assert LLMeta("claude-mythos-5") > LLMeta("claude-fable-5")

    def test_mythos5_is_top(self):
        """mythos-5 为当前最高 / mythos-5 is the highest among current Claude models"""
        models = [
            LLMeta("claude-mythos-5"),
            LLMeta("claude-fable-5"),
            LLMeta("claude-opus-4-8"),
            LLMeta("claude-sonnet-4-6"),
            LLMeta("claude-haiku-4-5"),
        ]
        assert max(models).variant == "mythos"


class TestClaudeExistingModels:
    """验证现有模型未受影响 / Validate existing models are not affected"""

    @pytest.mark.parametrize(
        "model_name,expected_version,expected_variant",
        [
            ("claude-sonnet-4-5", "4.5", "sonnet"),
            ("claude-haiku-4-5", "4.5", "haiku"),
            ("claude-opus-4-1", "4.1", "opus"),
            ("claude-sonnet-4-0", "4.0", "sonnet"),
            ("claude-opus-4-0", "4.0", "opus"),
            ("claude-3-7-sonnet", "3.7", "sonnet"),
            ("claude-3-5-haiku", "3.5", "haiku"),
        ],
    )
    def test_existing_model_config(self, model_name: str, expected_version: str, expected_variant: str):
        """验证现有模型配置正确 / Validate existing model configs are correct"""
        config = get_specific_model_config(model_name)
        assert config is not None
        version, variant, _ = config
        assert version == expected_version
        assert variant == expected_variant
