# filename: provider.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型提供商定义 / Model provider definitions
"""

from enum import Enum

from llmeta.models.dynamic_enum import DynamicEnumMeta


class Provider(str, Enum, metaclass=DynamicEnumMeta):
    """
    支持的模型提供商 / Supported model providers

    支持动态添加新成员，第三方用户可以在运行时扩展
    Supports dynamically adding new members, third-party users can extend at runtime

    Example:
        >>> # 动态添加新的提供商 / Dynamically add new provider
        >>> Provider.add_member("GOOGLE", "google")
        >>> Provider.add_member("META", "meta")
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

        # 定义提供商关键词映射 / Define provider keyword mapping
        provider_keywords = {
            cls.OPENAI: ["gpt", "o1", "o3"],
            cls.ANTHROPIC: ["claude"],
            cls.ZHIPU: ["glm", "chatglm", "cogview", "cogvideo"],
            cls.ALIBABA: ["qwen", "tongyi"],
            cls.BAIDU: ["ernie", "wenxin"],
            cls.TENCENT: ["hunyuan"],
            cls.MOONSHOT: ["moonshot"],
            cls.DEEPSEEK: ["deepseek"],
            cls.MINIMAX: ["minimax", "abab"],
        }

        # 匹配提供商 / Match provider
        for provider, keywords in provider_keywords.items():
            match any(keyword in model_lower for keyword in keywords):
                case True:
                    return provider

        return cls.UNKNOWN
