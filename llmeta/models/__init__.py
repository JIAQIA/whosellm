# filename: __init__.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型信息注册表 / Model information registry
"""

# 导入模型定义以触发注册 / Import model definitions to trigger registration
from llmeta.models import openai, zhipu
from llmeta.models.base import ModelInfo, get_model_info, register_model

__all__ = [
    "ModelInfo",
    "get_model_info",
    "register_model",
]
