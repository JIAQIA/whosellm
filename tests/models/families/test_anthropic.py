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


class TestClaudeFable51:
    """Claude Fable 5.1 测试（2026-09-01 发布，当前最新） / Claude Fable 5.1 tests"""

    def test_specific_model_config(self):
        """验证 claude-fable-5-1 配置 / Validate claude-fable-5-1 config"""
        config = get_specific_model_config("claude-fable-5-1")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.1"
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
        """验证 claude-fable-5-1 模式匹配 / Validate claude-fable-5-1 pattern match"""
        matched = match_model_pattern("claude-fable-5-1")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "fable"
        assert matched["provider"] == Provider.ANTHROPIC

    @pytest.mark.parametrize("model_name", ["claude-fable-5-1-20260901", "claude-fable-5-1@20260901"])
    def test_pattern_with_snapshot(self, model_name: str):
        """验证带 snapshot 的解析（版本号不被吞） / Validate snapshot forms keep version 5.1"""
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert meta.version == "5.1"
        assert meta.variant == "fable"

    def test_version_ordering(self):
        """验证 5.0 < 5.1 / Validate Fable 5.0 < Fable 5.1"""
        assert LLMeta("claude-fable-5") < LLMeta("claude-fable-5-1")


class TestClaudeMythos51:
    """Claude Mythos 5.1 测试（Glasswing 受邀版） / Claude Mythos 5.1 tests"""

    def test_specific_model_config(self):
        """验证 claude-mythos-5-1 配置 / Validate claude-mythos-5-1 config"""
        config = get_specific_model_config("claude-mythos-5-1")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.1"
        assert variant == "mythos"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_thinking is True
        assert capabilities.supports_structured_outputs is True
        assert capabilities.supports_computer_use is True
        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 1000000

    def test_pattern_match(self):
        """验证 claude-mythos-5-1 模式匹配 / Validate claude-mythos-5-1 pattern match"""
        matched = match_model_pattern("claude-mythos-5-1")
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
        """mythos-5 在所列模型中最高 / mythos-5 is the highest among the models listed"""
        models = [
            LLMeta("claude-mythos-5"),
            LLMeta("claude-fable-5"),
            LLMeta("claude-opus-4-8"),
            LLMeta("claude-sonnet-4-6"),
            LLMeta("claude-haiku-4-5"),
        ]
        assert max(models).variant == "mythos"


class TestClaudeOpus55:
    """Claude Opus 5.5 测试（2026-09-22 发布，当前最新） / Claude Opus 5.5 tests (released 2026-09-22)"""

    def test_specific_model_config(self):
        """验证 claude-opus-5-5 配置 / Validate claude-opus-5-5 config"""
        config = get_specific_model_config("claude-opus-5-5")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.5"
        assert variant == "opus"
        assert capabilities is not None
        assert capabilities.supports_vision is True
        assert capabilities.supports_thinking is True  # 自适应思考常开且不可关闭 / always on, cannot be disabled
        assert capabilities.supports_function_calling is True
        assert capabilities.supports_streaming is True
        assert capabilities.supports_structured_outputs is True
        assert capabilities.supports_computer_use is True
        assert capabilities.max_tokens == 128000
        assert capabilities.context_window == 1000000

    def test_pattern_match(self):
        """验证 claude-opus-5-5 模式匹配 / Validate claude-opus-5-5 pattern match"""
        matched = match_model_pattern("claude-opus-5-5")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "opus"
        assert matched["provider"] == Provider.ANTHROPIC
        assert matched["_from_specific_model"] == "claude-opus-5-5"

    @pytest.mark.parametrize("model_name", ["claude-opus-5-5-20260921", "claude-opus-5-5@20260921"])
    def test_pattern_with_snapshot(self, model_name: str):
        """验证带 snapshot 的解析（- 与 @ 两种格式，版本号不被吞） / Validate snapshot forms keep version 5.5"""
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert meta.version == "5.5"
        assert meta.variant == "opus"

    def test_not_swallowed_by_opus5(self):
        """claude-opus-5-5 不得被 claude-opus-5 的配置吞掉 / opus-5-5 must not be captured by opus-5

        回归保护：opus-5 的子模式在 opus-5-5 之前注册，若 snapshot 宽度匹配不当会退化为 5.0
        Regression guard: opus-5's sub-patterns register before opus-5-5's; a loose snapshot
        width would silently degrade opus-5-5 to version 5.0
        """
        meta = LLMeta("claude-opus-5-5")
        assert meta.version == "5.5"
        assert meta.variant == "opus"
        assert meta.capabilities.context_window == 1000000
        assert meta.capabilities.max_tokens == 128000


class TestClaudeOpus5:
    """Claude Opus 5 测试（2026-07-24 GA） / Claude Opus 5 tests"""

    def test_specific_model_config(self):
        """验证 claude-opus-5 配置 / Validate claude-opus-5 config"""
        config = get_specific_model_config("claude-opus-5")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.0"
        assert variant == "opus"
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
        """验证 claude-opus-5 模式匹配 / Validate claude-opus-5 pattern match"""
        matched = match_model_pattern("claude-opus-5")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "opus"
        assert matched["provider"] == Provider.ANTHROPIC

    @pytest.mark.parametrize("model_name", ["claude-opus-5-20260724", "claude-opus-5@20260724"])
    def test_pattern_with_snapshot(self, model_name: str):
        """验证带 snapshot 的解析（- 与 @ 两种格式，版本号不被吞） / Validate snapshot forms keep version 5.0"""
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert meta.version == "5.0"
        assert meta.variant == "opus"


class TestClaudeSonnet5:
    """Claude Sonnet 5 测试（2026-06-30 GA） / Claude Sonnet 5 tests"""

    def test_specific_model_config(self):
        """验证 claude-sonnet-5 配置 / Validate claude-sonnet-5 config"""
        config = get_specific_model_config("claude-sonnet-5")
        assert config is not None
        version, variant, capabilities = config
        assert version == "5.0"
        assert variant == "sonnet"
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
        """验证 claude-sonnet-5 模式匹配 / Validate claude-sonnet-5 pattern match"""
        matched = match_model_pattern("claude-sonnet-5")
        assert matched is not None
        assert matched["family"] == ModelFamily.CLAUDE
        assert matched["variant"] == "sonnet"
        assert matched["provider"] == Provider.ANTHROPIC

    @pytest.mark.parametrize("model_name", ["claude-sonnet-5-20260630", "claude-sonnet-5@20260630"])
    def test_pattern_with_snapshot(self, model_name: str):
        """验证带 snapshot 的解析（- 与 @ 两种格式，版本号不被吞） / Validate snapshot forms keep version 5.0"""
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert meta.version == "5.0"
        assert meta.variant == "sonnet"


class TestClaude5Ordering:
    """Claude 5 代版本比较：5.0 > 4.8 > 4.6；同版本 fable > opus > sonnet / Claude 5 generation ordering"""

    def test_opus5_outranks_opus48(self):
        """opus-5 (v5.0) 高于 opus-4-8 (v4.8) / opus-5 outranks opus-4-8 by version"""
        assert LLMeta("claude-opus-5") > LLMeta("claude-opus-4-8")

    def test_opus55_outranks_opus5(self):
        """opus-5-5 (v5.5) 高于 opus-5 (v5.0) / opus-5-5 outranks opus-5 by version"""
        assert LLMeta("claude-opus-5-5") > LLMeta("claude-opus-5")
        assert LLMeta("claude-opus-5-5") > LLMeta("claude-fable-5-1")

    def test_opus55_outranks_mythos5_by_version(self):
        """版本优先于档位：opus-5-5 (v5.5) 高于 mythos-5 (v5.0)，尽管 mythos 变体档更高
        Version precedes tier: opus-5-5 outranks mythos-5 despite mythos's higher variant tier
        """
        assert LLMeta("claude-opus-5-5") > LLMeta("claude-mythos-5")
        # 同版本 5.0 内档位排序不受影响 / tier ordering within v5.0 is unaffected
        assert LLMeta("claude-mythos-5") > LLMeta("claude-fable-5")

    def test_sonnet5_outranks_sonnet46(self):
        """sonnet-5 (v5.0) 高于 sonnet-4-6 (v4.6) / sonnet-5 outranks sonnet-4-6 by version"""
        assert LLMeta("claude-sonnet-5") > LLMeta("claude-sonnet-4-6")

    def test_opus5_outranks_sonnet5(self):
        """同版本 5.0 下 opus 变体优先级高于 sonnet / opus outranks sonnet on variant priority"""
        assert LLMeta("claude-opus-5") > LLMeta("claude-sonnet-5")

    def test_fable5_outranks_opus5(self):
        """同版本 5.0 下 fable（Mythos-class）仍高于 opus / fable still outranks opus on variant priority"""
        assert LLMeta("claude-fable-5") > LLMeta("claude-opus-5")

    def test_mythos5_is_top(self):
        """同代 v5.0 内 mythos 档最高（v5.1/v5.5 按版本另行比较）
        mythos is the top tier within the v5.0 generation (v5.1/v5.5 compare by version)
        """
        models = [
            LLMeta("claude-mythos-5"),
            LLMeta("claude-fable-5"),
            LLMeta("claude-opus-5"),
            LLMeta("claude-sonnet-5"),
            LLMeta("claude-opus-4-8"),
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
