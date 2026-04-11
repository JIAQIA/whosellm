"""Registry Merge 测试 / Registry Merge tests

验证多个 ModelFamilyConfig 声明相同 family 时的自动合并逻辑。
Verify auto-merge logic when multiple ModelFamilyConfig instances declare the same family.
"""

import pytest

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.models.registry import _FAMILY_CONFIGS, get_family_config, match_model_pattern
from whosellm.provider import Provider


@pytest.fixture()
def _clean_test_family():
    """注册测试用 family，测试结束后清理 / Register test family, clean up after test"""
    # 动态添加测试用枚举
    ModelFamily.add_member("_TEST_MERGE", "_test-merge")
    Provider.add_member("_TEST_PROVIDER", "_test-provider")

    yield

    # 清理注册表
    key = (ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
    _FAMILY_CONFIGS.pop(key, None)


@pytest.mark.usefixtures("_clean_test_family")
class TestRegistryMerge:
    """Registry Merge 功能测试"""

    def test_patterns_prepended_on_merge(self):
        """新 patterns 应追加到列表前面"""
        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}-{variant:variant}"],
            version_default="2.0",
        )

        config = get_family_config(ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
        assert config is not None
        # 新的 pattern 在前
        assert config.patterns[0] == "_test-merge-{version}-{variant:variant}"
        assert config.patterns[1] == "_test-merge-{version}"
        assert len(config.patterns) == 2

    def test_patterns_deduplicated_on_merge(self):
        """重复的 patterns 应自动去重"""
        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}", "_test-merge-{version}-new"],
            version_default="2.0",
        )

        config = get_family_config(ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
        assert config is not None
        # 重复的不应出现两次
        assert config.patterns.count("_test-merge-{version}") == 1
        # 新的在前
        assert config.patterns[0] == "_test-merge-{version}-new"

    def test_specific_models_merged(self):
        """specific_models 应合并，后注册覆盖"""
        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            specific_models={
                "_test-merge-alpha": SpecificModelConfig(
                    version_default="1.0",
                    variant_default="alpha",
                    capabilities=ModelCapabilities(max_tokens=100),
                ),
            },
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=[],
            version_default="2.0",
            specific_models={
                "_test-merge-beta": SpecificModelConfig(
                    version_default="2.0",
                    variant_default="beta",
                    capabilities=ModelCapabilities(max_tokens=200),
                ),
            },
        )

        config = get_family_config(ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
        assert config is not None
        # 两个 specific_models 都存在
        assert "_test-merge-alpha" in config.specific_models
        assert "_test-merge-beta" in config.specific_models

    def test_specific_models_override_on_conflict(self):
        """specific_models key 冲突时后注册覆盖"""
        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            specific_models={
                "_test-merge-x": SpecificModelConfig(
                    version_default="1.0",
                    variant_default="old",
                ),
            },
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=[],
            version_default="2.0",
            specific_models={
                "_test-merge-x": SpecificModelConfig(
                    version_default="2.0",
                    variant_default="new",
                ),
            },
        )

        config = get_family_config(ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
        assert config is not None
        assert config.specific_models["_test-merge-x"].variant_default == "new"

    def test_defaults_use_last_registered(self):
        """version_default / variant_default / capabilities 取最后注册的值"""
        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            variant_default="old-default",
            capabilities=ModelCapabilities(max_tokens=100),
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=[],
            version_default="2.0",
            variant_default="new-default",
            capabilities=ModelCapabilities(max_tokens=999),
        )

        config = get_family_config(ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
        assert config is not None
        assert config.version_default == "2.0"
        assert config.variant_default == "new-default"
        assert config.capabilities.max_tokens == 999

    def test_merged_config_pattern_matching_works(self):
        """合并后的 patterns 能正确匹配模型名"""
        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}-{variant:variant}"],
            version_default="2.0",
        )

        # 用第一个 config 的 pattern 匹配
        result1 = match_model_pattern("_test-merge-3.0")
        assert result1 is not None
        assert result1["family"] == ModelFamily._TEST_MERGE
        assert result1["version"] == "3.0"

        # 用第二个 config 的 pattern 匹配
        result2 = match_model_pattern("_test-merge-3.0-pro")
        assert result2 is not None
        assert result2["family"] == ModelFamily._TEST_MERGE
        assert result2["variant"] == "pro"

    def test_version_capabilities_stored_on_merge(self):
        """merge 后 _version_capabilities 应包含每个版本的 capabilities"""
        caps_v1 = ModelCapabilities(max_tokens=100)
        caps_v2 = ModelCapabilities(max_tokens=200)

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            capabilities=caps_v1,
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=[],
            version_default="2.0",
            capabilities=caps_v2,
        )

        config = get_family_config(ModelFamily._TEST_MERGE, Provider._TEST_PROVIDER)
        assert config is not None
        # 两个版本的 capabilities 都应保留
        assert "1.0" in config._version_capabilities
        assert "2.0" in config._version_capabilities
        assert config._version_capabilities["1.0"].max_tokens == 100
        assert config._version_capabilities["2.0"].max_tokens == 200
        # family default 是最后注册的
        assert config.capabilities.max_tokens == 200

    def test_version_capabilities_inheritance(self):
        """specific_model caps=None 时应继承版本级 caps 而非 family default"""
        from whosellm.models.base import auto_register_model
        from whosellm.models.registry import get_version_capabilities

        caps_v1 = ModelCapabilities(max_tokens=111, context_window=1000)
        caps_v2 = ModelCapabilities(max_tokens=999, context_window=9000)

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            capabilities=caps_v1,
            specific_models={
                "_test-merge-1.0": SpecificModelConfig(
                    version_default="1.0",
                    variant_default="base",
                    # capabilities=None → 应继承 v1 的 caps，不是 v2 的
                ),
            },
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=[],
            version_default="2.0",
            capabilities=caps_v2,
        )

        # 验证 get_version_capabilities 返回正确的版本级 caps
        v1_caps = get_version_capabilities(ModelFamily._TEST_MERGE, "1.0", Provider._TEST_PROVIDER)
        assert v1_caps is not None
        assert v1_caps.max_tokens == 111

        # 验证 auto_register_model 使用版本级 caps 而非 family default
        info = auto_register_model("_test-merge-1.0")
        assert info.capabilities.max_tokens == 111
        assert info.capabilities.context_window == 1000

    def test_specific_model_caps_override_version(self):
        """Level 1：specific_model 显式设置 caps 时应优先于 version caps"""
        from whosellm.models.base import auto_register_model

        caps_version = ModelCapabilities(max_tokens=500, context_window=5000)
        caps_specific = ModelCapabilities(max_tokens=777, context_window=7777)

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            capabilities=caps_version,
            specific_models={
                "_test-merge-special": SpecificModelConfig(
                    version_default="1.0",
                    variant_default="base",
                    capabilities=caps_specific,  # Level 1: 显式设置
                ),
            },
        )

        info = auto_register_model("_test-merge-special")
        # 应使用 Level 1 (specific_model caps)，而非 Level 2 (version caps)
        assert info.capabilities.max_tokens == 777
        assert info.capabilities.context_window == 7777

    def test_fallback_to_family_default(self):
        """Level 3：version 不在 _version_capabilities 中时回退到 family default"""
        from whosellm.models.base import auto_register_model

        caps_v1 = ModelCapabilities(max_tokens=100, context_window=1000)
        caps_v2 = ModelCapabilities(max_tokens=999, context_window=9000)

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=["_test-merge-{version}"],
            version_default="1.0",
            capabilities=caps_v1,
        )

        ModelFamilyConfig(
            family=ModelFamily._TEST_MERGE,
            provider=Provider._TEST_PROVIDER,
            patterns=[],
            version_default="2.0",
            capabilities=caps_v2,
        )

        # v3.0 不存在版本级 caps，应回退到 family default (v2.0 的 caps)
        info = auto_register_model("_test-merge-3.0")
        assert info.capabilities.max_tokens == 999
        assert info.capabilities.context_window == 9000
