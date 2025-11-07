# filename: registry.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型注册表 / Model registry

注意：此文件已废弃，注册表功能已移至 base.py
Note: This file is deprecated, registry functionality has been moved to base.py
"""

# 为了向后兼容，从 base 导入
# For backward compatibility, import from base
from llmver.models.base import MODEL_REGISTRY, register_model

__all__ = ["MODEL_REGISTRY", "register_model"]
