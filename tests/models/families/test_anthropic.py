# filename: test_anthropic.py
"""
Anthropic Claude 模型家族测试 / Anthropic Claude model family tests
"""

import pytest

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
        assert capabilities.context_window == 200000

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
        assert capabilities.context_window == 200000

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
