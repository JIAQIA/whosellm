# filename: model_version.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型版本管理核心类 / Core model version management class
"""

from dataclasses import dataclass, field
from functools import total_ordering
from typing import Any

from llmver.capabilities import ModelCapabilities
from llmver.models import get_model_info
from llmver.provider import Provider


@total_ordering
@dataclass
class ModelVersion:
    """
    模型版本类 / Model version class

    支持从单个字符串初始化，自动识别提供商、版本和型号
    Supports initialization from a single string, automatically recognizing provider, version, and model
    """

    model_name: str
    provider: Provider = Provider.UNKNOWN
    version: str = ""
    variant: str = ""
    capabilities: ModelCapabilities = field(default_factory=ModelCapabilities)
    _version_tuple: tuple[int, ...] = field(default_factory=tuple, repr=False)

    def __post_init__(self) -> None:
        """
        初始化后的处理 / Post-initialization processing

        自动从模型名称解析并填充其他字段
        Automatically parse and populate other fields from model name
        """
        # 从模型名称获取信息 / Get information from model name
        model_info = get_model_info(self.model_name)

        # 如果字段为默认值，则使用解析的值 / Use parsed values if fields are default values
        if self.provider == Provider.UNKNOWN:
            self.provider = model_info.provider
        if not self.version:
            self.version = model_info.version
        if not self.variant:
            self.variant = model_info.variant
        # 检查 capabilities 是否为默认的空对象 / Check if capabilities is default empty object
        if self.capabilities == ModelCapabilities():
            self.capabilities = model_info.capabilities
        # 设置版本元组用于比较 / Set version tuple for comparison
        self._version_tuple = model_info.version_tuple

    def __str__(self) -> str:
        """字符串表示 / String representation"""
        return self.model_name

    def __repr__(self) -> str:
        """详细表示 / Detailed representation"""
        return f"ModelVersion(model_name='{self.model_name}', provider={self.provider}, version='{self.version}')"

    def __eq__(self, other: object) -> bool:
        """
        相等比较 / Equality comparison

        只有同一提供商的模型才能比较
        Only models from the same provider can be compared
        """
        if not isinstance(other, ModelVersion):
            return NotImplemented

        if self.provider != other.provider:
            return False

        return self._version_tuple == other._version_tuple

    def __lt__(self, other: object) -> bool:
        """
        小于比较 / Less than comparison

        只有同一提供商的模型才能比较
        Only models from the same provider can be compared
        """
        if not isinstance(other, ModelVersion):
            return NotImplemented

        if self.provider != other.provider:
            raise ValueError(
                f"无法比较不同提供商的模型: {self.provider} vs {other.provider} / "
                f"Cannot compare models from different providers: {self.provider} vs {other.provider}",
            )

        return self._version_tuple < other._version_tuple

    def validate_params(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        验证并调整参数 / Validate and adjust parameters

        使用 VRL 脚本进行参数验证和调整
        Use VRL script for parameter validation and adjustment

        Args:
            params: 原始参数 / Original parameters

        Returns:
            dict: 验证后的参数 / Validated parameters
        """
        # TODO: 实现基于 VRL 的参数验证
        # TODO: Implement VRL-based parameter validation
        return params

    @property
    def supports_multimodal(self) -> bool:
        """
        是否支持多模态 / Whether multimodal is supported

        Returns:
            bool: 支持任意多模态输入即返回True / Returns True if any multimodal input is supported
        """
        return any(
            [
                self.capabilities.supports_vision,
                self.capabilities.supports_audio,
                self.capabilities.supports_video,
                self.capabilities.supports_pdf,
            ],
        )
