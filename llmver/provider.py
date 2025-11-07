# filename: provider.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型提供商定义 / Model provider definitions
"""

from enum import Enum


class Provider(str, Enum):
    """
    支持的模型提供商 / Supported model providers
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    ZHIPU = "zhipu"  # 智谱AI
    ALIBABA = "alibaba"  # 阿里云
    BAIDU = "baidu"  # 百度
    TENCENT = "tencent"  # 腾讯
    MOONSHOT = "moonshot"  # 月之暗面
    DEEPSEEK = "deepseek"  # DeepSeek
    MINIMAX = "minimax"  # MiniMax
    UNKNOWN = "unknown"

    @classmethod
    def from_model_name(cls, model_name: str) -> "Provider":
        """
        从模型名称推断提供商 / Infer provider from model name

        Args:
            model_name: 模型名称 / Model name

        Returns:
            Provider: 提供商枚举 / Provider enum
        """
        model_lower = model_name.lower()

        # OpenAI 系列
        if any(x in model_lower for x in ["gpt", "o1", "o3"]):
            return cls.OPENAI

        # Anthropic 系列
        if "claude" in model_lower:
            return cls.ANTHROPIC

        # 智谱 AI
        if any(x in model_lower for x in ["glm", "chatglm", "cogview", "cogvideo"]):
            return cls.ZHIPU

        # 阿里云
        if any(x in model_lower for x in ["qwen", "tongyi"]):
            return cls.ALIBABA

        # 百度
        if any(x in model_lower for x in ["ernie", "wenxin"]):
            return cls.BAIDU

        # 腾讯
        if "hunyuan" in model_lower:
            return cls.TENCENT

        # 月之暗面
        if "moonshot" in model_lower:
            return cls.MOONSHOT

        # DeepSeek
        if "deepseek" in model_lower:
            return cls.DEEPSEEK

        # MiniMax
        if "minimax" in model_lower or "abab" in model_lower:
            return cls.MINIMAX

        return cls.UNKNOWN
