# filename: base.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型信息基础类 / Model information base class
"""

from dataclasses import dataclass

from llmver.capabilities import ModelCapabilities
from llmver.provider import Provider


@dataclass
class ModelInfo:
    """
    模型信息 / Model information
    """

    provider: Provider
    version: str
    variant: str
    capabilities: ModelCapabilities
    version_tuple: tuple[int, ...]


# 全局模型注册表 / Global model registry
MODEL_REGISTRY: dict[str, ModelInfo] = {}


def register_model(model_name: str, info: ModelInfo) -> None:
    """
    注册模型信息 / Register model information

    Args:
        model_name: 模型名称（小写） / Model name (lowercase)
        info: 模型信息 / Model information
    """
    MODEL_REGISTRY[model_name.lower()] = info


def parse_version(version_str: str) -> tuple[int, ...]:
    """
    解析版本字符串为元组 / Parse version string to tuple

    Args:
        version_str: 版本字符串，如 "4.0", "3.5" / Version string like "4.0", "3.5"

    Returns:
        tuple: 版本元组 / Version tuple
    """
    if not version_str:
        return (0,)

    parts = []
    for part in version_str.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            # 如果包含非数字字符，尝试提取数字部分
            # If contains non-numeric characters, try to extract numeric part
            numeric = "".join(c for c in part if c.isdigit())
            if numeric:
                parts.append(int(numeric))
            else:
                parts.append(0)

    return tuple(parts)


def get_model_info(model_name: str) -> ModelInfo:
    """
    获取模型信息 / Get model information

    Args:
        model_name: 模型名称 / Model name

    Returns:
        ModelInfo: 模型信息 / Model information
    """
    model_lower = model_name.lower()

    # 检查注册表中是否有精确匹配
    # Check if there's an exact match in the registry
    if model_lower in MODEL_REGISTRY:
        return MODEL_REGISTRY[model_lower]

    # 检查是否有部分匹配
    # Check if there's a partial match
    for registered_name, info in MODEL_REGISTRY.items():
        if registered_name in model_lower or model_lower in registered_name:
            return info

    # 如果没有找到，返回默认信息
    # If not found, return default information
    provider = Provider.from_model_name(model_name)

    return ModelInfo(
        provider=provider,
        version="",
        variant="",
        capabilities=ModelCapabilities(),
        version_tuple=(0,),
    )
