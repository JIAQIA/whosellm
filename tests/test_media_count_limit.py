# filename: test_media_count_limit.py
"""
MediaCountLimit 单元测试 / MediaCountLimit unit tests

值域约定 / Value domain:
- 0         确认不支持 / confirmed unsupported
- 正整数    文档化上限 / documented cap
- UNLIMITED 无文档化上限，仅受上下文 token 预算约束 / no documented cap (math.inf)
- 键缺失 = 未实测，视同不支持 / missing key = unmeasured, treated as unsupported
"""

import math
from dataclasses import FrozenInstanceError

import pytest

from whosellm import UNLIMITED, MediaCountLimit
from whosellm.capabilities import ModelCapabilities


class TestDefault:
    """默认行为 / Default behavior"""

    def test_default_per_type_empty(self):
        mcl = MediaCountLimit()
        assert mcl.per_type == {}
        assert mcl.count_mode == "per_type"
        assert mcl.combined is None

    def test_missing_key_returns_zero(self):
        """键缺失（未实测）视同不支持 / Missing keys are treated as unsupported"""
        mcl = MediaCountLimit(per_type={"image": 10})
        assert mcl.get("video") == 0
        assert mcl.is_supported("video") is False

    def test_model_capabilities_default(self):
        caps = ModelCapabilities()
        assert caps.media_count_limit == MediaCountLimit()
        assert caps.media_count_limit.get("image") == 0


class TestValueDomain:
    """取值域语义 / Value domain semantics: 0 / int / UNLIMITED"""

    def test_zero_means_unsupported(self):
        mcl = MediaCountLimit(per_type={"image": 0})
        assert mcl.get("image") == 0
        assert mcl.is_supported("image") is False
        assert bool(mcl.get("image")) is False

    def test_positive_int_is_documented_cap(self):
        mcl = MediaCountLimit(per_type={"image": 600})
        assert mcl.get("image") == 600
        assert mcl.is_supported("image") is True
        assert bool(mcl.get("image")) is True

    def test_unlimited_is_truthy(self):
        """UNLIMITED 必须是 truthy——这是 0 与"无上限"在 bool 上下文的唯一区分点"""
        mcl = MediaCountLimit(per_type={"image": UNLIMITED})
        assert mcl.get("image") is math.inf
        assert mcl.is_supported("image") is True
        assert bool(mcl.get("image")) is True

    def test_bool_never_conflates_zero_and_unlimited(self):
        assert bool(0) is False
        assert bool(UNLIMITED) is True

    def test_unlimited_comparison_with_positive_ints(self):
        assert UNLIMITED > 50
        assert UNLIMITED > 0
        assert not UNLIMITED < 600

    def test_is_supported_uses_positive_check(self):
        """is_supported 基于 limit > 0，区分 0 / 正整数 / UNLIMITED"""
        assert MediaCountLimit(per_type={"image": 0}).is_supported("image") is False
        assert MediaCountLimit(per_type={"image": 1}).is_supported("image") is True
        assert MediaCountLimit(per_type={"image": UNLIMITED}).is_supported("image") is True


class TestCountingMode:
    """计数模式 / Counting mode"""

    def test_per_type_mode_default(self):
        mcl = MediaCountLimit(per_type={"image": 600})
        assert mcl.count_mode == "per_type"
        assert mcl.combined is None

    def test_combined_mode(self):
        mcl = MediaCountLimit(per_type={"image": 50, "video": 50}, count_mode="combined", combined=50)
        assert mcl.count_mode == "combined"
        assert mcl.combined == 50
        assert mcl.get("image") == 50


class TestImmutability:
    """不可变性 / Immutability (frozen dataclass)

    注意：frozen 为浅冻结——字段引用不可重绑，与项目内既有 list 字段
    （supported_image_mime_type 等）的语义保持一致。
    Note: frozen is shallow — field rebinding is rejected, same semantics as
    existing list fields (supported_image_mime_type etc.).
    """

    def test_field_reassignment_rejected(self):
        mcl = MediaCountLimit(per_type={"image": 50})
        with pytest.raises(FrozenInstanceError):
            mcl.per_type = {}  # type: ignore[misc]

    def test_default_factory_isolation(self):
        """default_factory 保证每个实例独立，不共享可变状态"""
        a = ModelCapabilities()
        b = ModelCapabilities()
        assert a.media_count_limit is not b.media_count_limit
        assert a.media_count_limit.per_type is not b.media_count_limit.per_type
