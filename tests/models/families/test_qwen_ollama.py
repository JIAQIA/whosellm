"""
Qwen Ollama 短格式模式匹配测试 / Qwen Ollama short format pattern matching tests

覆盖 qwen2、qwen2.5、qwen2.5-coder 等 Ollama 风格模型名
Covers Ollama-style model names like qwen2, qwen2.5, qwen2.5-coder
"""

import pytest

from whosellm import LLMeta
from whosellm.models.base import ModelFamily
from whosellm.models.registry import match_model_pattern
from whosellm.provider import Provider

# ── match_model_pattern 层 ──


@pytest.mark.unit
class TestQwenOllamaPatternMatch:
    """match_model_pattern 对 Ollama 短格式的识别"""

    def test_qwen2(self) -> None:
        matched = match_model_pattern("qwen2")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["version"] == 2
        assert matched["provider"] == Provider.ALIBABA

    def test_qwen3(self) -> None:
        matched = match_model_pattern("qwen3")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["version"] == 3

    def test_qwen2_5(self) -> None:
        matched = match_model_pattern("qwen2.5")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["version"] == "2.5"

    def test_qwen2_5_coder(self) -> None:
        matched = match_model_pattern("qwen2.5-coder")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["version"] == "2.5"
        assert matched["variant"] == "coder"


# ── LLMeta 端到端 ──


@pytest.mark.integration
class TestQwenOllamaLLMeta:
    """LLMeta 端到端验证 Ollama 短格式"""

    def test_qwen2_llmeta(self) -> None:
        meta = LLMeta("qwen2")
        assert meta.family == ModelFamily.QWEN
        assert meta.version == "2"
        assert meta.provider == Provider.ALIBABA

    def test_qwen3_llmeta(self) -> None:
        meta = LLMeta("qwen3")
        assert meta.family == ModelFamily.QWEN
        assert meta.version == "3"

    def test_qwen2_5_llmeta(self) -> None:
        meta = LLMeta("qwen2.5")
        assert meta.family == ModelFamily.QWEN
        assert meta.version == "2.5"

    def test_qwen2_5_coder_llmeta(self) -> None:
        meta = LLMeta("qwen2.5-coder")
        assert meta.family == ModelFamily.QWEN
        assert meta.version == "2.5"
        assert meta.variant == "coder"


# ── 回归：现有模式不受影响 ──


@pytest.mark.unit
class TestQwenExistingPatternsUnaffected:
    """确保新增 Ollama 短格式不影响已有模式的匹配"""

    def test_qwen_turbo(self) -> None:
        matched = match_model_pattern("qwen-turbo")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["variant"] == "turbo"

    def test_qwen_plus(self) -> None:
        matched = match_model_pattern("qwen-plus")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["variant"] == "plus"

    def test_qwen3_max(self) -> None:
        matched = match_model_pattern("qwen3-max")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["version"] == "3"
        assert matched["variant"] == "max"

    def test_qwen3_vl_plus(self) -> None:
        matched = match_model_pattern("qwen3-vl-plus")
        assert matched is not None
        assert matched["family"] == ModelFamily.QWEN
        assert matched["variant"] == "vl-plus"
