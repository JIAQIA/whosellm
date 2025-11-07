# filename: config.py
# @Time    : 2025/11/7 17:35
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型家族配置类 / Model family configuration class

集中管理模型家族的所有配置信息，包括命名模式、默认能力等
Centrally manage all configuration for model families, including naming patterns, default capabilities, etc.
"""

from dataclasses import dataclass, field

from llmeta.capabilities import ModelCapabilities
from llmeta.models.base import ModelFamily
from llmeta.provider import Provider


@dataclass
class ModelFamilyConfig:
    """
    模型家族配置 / Model family configuration

    集中管理一个模型家族的所有配置信息
    Centrally manage all configuration for a model family
    """

    # 基本信息 / Basic information
    family: ModelFamily
    provider: Provider

    # 命名模式 / Naming patterns
    # 按优先级排序，更具体的在前 / Ordered by priority, more specific first
    patterns: list[str]

    # 默认值 / Defaults
    version_default: str = "1.0"

    # 默认能力 / Default capabilities
    capabilities: ModelCapabilities = field(default_factory=ModelCapabilities)

    # 预注册的特定模型（可选） / Pre-registered specific models (optional)
    # 格式: {model_name: (version, variant, custom_capabilities)}
    # Format: {model_name: (version, variant, custom_capabilities)}
    specific_models: dict[str, tuple[str, str, ModelCapabilities | None]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """注册到全局注册表 / Register to global registry"""
        from llmeta.models.registry import register_family_config

        register_family_config(self)
