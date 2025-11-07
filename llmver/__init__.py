# filename: __init__.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
LLMVer - 统一的大语言模型版本和能力管理库 / A unified LLM model version and capability management library
"""

__version__ = "0.1.0"

from llmver.capabilities import ModelCapabilities
from llmver.model_version import LLM
from llmver.models.base import ModelFamily
from llmver.provider import Provider

__all__ = [
    "LLM",
    "ModelCapabilities",
    "ModelFamily",
    "Provider",
    "__version__",
]
