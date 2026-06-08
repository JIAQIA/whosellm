# filename: test_claude_4x_versions.py
"""
回归测试：Claude 4.x 别名版本解析 + 版本比较稳定性
Regression tests: Claude 4.x alias version parsing + version-comparison stability

背景 / Context:
    TFRobotV2 需要门控 Claude 4.6+ 移除的 assistant prefill。决定**用版本比较**判断
    （`family == CLAUDE and parse_version(version) >= (4, 6)`），而非依赖能力位。
    因此 whosellm 必须保证 4.x 别名（含未注册的新别名）版本解析正确、比较稳定。

    根因：parse 的 ``{snapshot:8d}`` 是最大宽度，会把 ``claude-opus-4-5`` 的 ``5`` 当 snapshot，
    使 minor 被吞、版本回退 4.0。修复后通过精确 8 位 snapshot 自定义类型解决。
"""

import pytest

from whosellm import LLMeta
from whosellm.models.base import ModelFamily, parse_version

# 官方 prefill 真值表（platform.claude.com，逐字核实）：不支持 prefill 的恰为版本 >= 4.6
# Authoritative prefill truth table: models WITHOUT prefill are exactly version >= 4.6
_PREFILL_REMOVED = {
    "claude-opus-4-8",
    "claude-opus-4-7",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
}
_PREFILL_SUPPORTED = {
    "claude-opus-4-5",
    "claude-opus-4-1",
    "claude-opus-4-0",
    "claude-sonnet-4-5",
    "claude-sonnet-4-0",
    "claude-haiku-4-5",
    "claude-3-7-sonnet",
    "claude-3-5-haiku",
}


class TestClaude4xAliasVersionParsing:
    """未注册/新增的 Claude 4.x 别名应解析出正确版本，而非回退 family 默认 4.0"""

    @pytest.mark.parametrize(
        "model_name,expected_version,expected_variant",
        [
            ("claude-opus-4-8", "4.8", "opus"),
            ("claude-opus-4-7", "4.7", "opus"),
            ("claude-opus-4-6", "4.6", "opus"),
            ("claude-opus-4-5", "4.5", "opus"),
            ("claude-opus-4-5-20251101", "4.5", "opus"),
            ("claude-haiku-4-5-20251001", "4.5", "haiku"),
            ("claude-sonnet-4-6", "4.6", "sonnet"),
            ("claude-sonnet-4-5", "4.5", "sonnet"),
        ],
    )
    def test_alias_version(self, model_name: str, expected_version: str, expected_variant: str):
        meta = LLMeta(model_name)
        assert meta.version == expected_version, f"{model_name} 解析出错误版本 {meta.version}"
        assert meta.variant == expected_variant
        assert meta.family == ModelFamily.CLAUDE

    def test_dated_4_0_snapshot_still_resolves_to_4_0(self):
        """带 8 位日期的原始 4.0 snapshot 仍应识别为 4.0，不被精确宽度修复破坏"""
        meta = LLMeta("claude-opus-4-20250514")
        assert meta.version == "4.0"
        assert meta.variant == "opus"

    def test_short_digit_not_swallowed_as_snapshot(self):
        """根因回归：单个数字 minor 不得被 {snapshot} 吞掉"""
        assert LLMeta("claude-opus-4-5").version == "4.5"
        assert LLMeta("claude-opus-4-7").version == "4.7"
        assert LLMeta("claude-opus-4-8").version == "4.8"


class TestClaude4xCapabilities:
    """新增模型应带官方真实能力（非臆测/镜像）"""

    @pytest.mark.parametrize(
        "model_name,ctx,max_out",
        [
            ("claude-opus-4-8", 1000000, 128000),
            ("claude-opus-4-7", 1000000, 128000),
            ("claude-opus-4-5", 200000, 64000),
        ],
    )
    def test_new_model_specs(self, model_name: str, ctx: int, max_out: int):
        caps = LLMeta(model_name).capabilities
        assert caps.context_window == ctx
        assert caps.max_tokens == max_out
        assert caps.supports_structured_outputs is True
        assert caps.supports_computer_use is True


class TestClaude4xVersionComparison:
    """版本比较稳定可用——TFRobotV2 门控的基石"""

    def test_monotonic_opus_chain(self):
        assert LLMeta("claude-opus-4-5") < LLMeta("claude-opus-4-6")
        assert LLMeta("claude-opus-4-6") < LLMeta("claude-opus-4-7")
        assert LLMeta("claude-opus-4-7") < LLMeta("claude-opus-4-8")

    def test_cross_minor(self):
        assert LLMeta("claude-opus-4-1") < LLMeta("claude-opus-4-6")
        assert LLMeta("claude-opus-4-0") < LLMeta("claude-opus-4-5")

    def test_dated_alias_equivalent_version(self):
        """带日期与不带日期解析出相同版本元组"""
        assert LLMeta("claude-opus-4-5").version == LLMeta("claude-opus-4-5-20251101").version


class TestVersionGateMatchesPrefillTruth:
    """关键：纯版本门控 `parse_version(version) >= (4, 6)` 的真假必须与官方 prefill 真值表完全一致"""

    @pytest.mark.parametrize("model_name", sorted(_PREFILL_REMOVED))
    def test_no_prefill_models_are_ge_4_6(self, model_name: str):
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert parse_version(meta.version) >= (4, 6), f"{model_name} 应被版本门控判为不支持 prefill"

    @pytest.mark.parametrize("model_name", sorted(_PREFILL_SUPPORTED))
    def test_prefill_models_are_lt_4_6(self, model_name: str):
        meta = LLMeta(model_name)
        assert meta.family == ModelFamily.CLAUDE
        assert parse_version(meta.version) < (4, 6), f"{model_name} 应被版本门控判为支持 prefill"
