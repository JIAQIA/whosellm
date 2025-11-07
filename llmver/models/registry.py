# filename: registry.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型注册表 / Model registry
"""

from llmver.models.base import ModelInfo

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
