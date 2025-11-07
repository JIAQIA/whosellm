# filename: model_version.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型版本管理核心类 / Core model version management class
"""

from functools import total_ordering
from typing import Any

from pydantic import BaseModel, Field

from llmver.capabilities import ModelCapabilities
from llmver.models import get_model_info
from llmver.provider import Provider


@total_ordering
class ModelVersion(BaseModel):
    """
    模型版本类 / Model version class

    支持从单个字符串初始化，自动识别提供商、版本和型号
    Supports initialization from a single string, automatically recognizing provider, version, and model
    """

    model_name: str = Field(
        description="完整的模型名称 / Full model name",
    )

    provider: Provider = Field(
        description="模型提供商 / Model provider",
    )

    version: str = Field(
        default="",
        description="模型版本 / Model version",
    )

    variant: str = Field(
        default="",
        description="模型变体/型号 / Model variant/type",
    )

    capabilities: ModelCapabilities = Field(
        description="模型能力 / Model capabilities",
    )

    _version_tuple: tuple[int, ...] = Field(
        default_factory=tuple,
        description="版本号元组，用于比较 / Version tuple for comparison",
    )

    class Config:
        """Pydantic 配置 / Pydantic configuration"""

        arbitrary_types_allowed = True

    def __init__(self, model_name: str, **data: Any) -> None:
        """
        初始化模型版本 / Initialize model version

        Args:
            model_name: 模型名称字符串 / Model name string
            **data: 其他参数 / Other parameters
        """
        # 从模型名称获取信息
        model_info = get_model_info(model_name)

        # 合并数据
        init_data = {
            "model_name": model_name,
            "provider": model_info.provider,
            "version": model_info.version,
            "variant": model_info.variant,
            "capabilities": model_info.capabilities,
            "_version_tuple": model_info.version_tuple,
            **data,
        }

        super().__init__(**init_data)

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
