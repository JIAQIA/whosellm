# filename: base.py
# @Time    : 2025/11/7 13:56
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型信息基础类 / Model information base class
"""

from dataclasses import dataclass
from enum import Enum

from llmver.capabilities import ModelCapabilities
from llmver.provider import Provider


class ModelFamily(str, Enum):
    """
    模型家族枚举 / Model family enum

    同一个模型家族可能有多个Provider提供
    Same model family may be provided by multiple providers
    """

    # OpenAI 家族 / OpenAI family
    GPT_4 = "gpt-4"
    GPT_3_5 = "gpt-3.5"
    O1 = "o1"
    O3 = "o3"

    # Anthropic 家族 / Anthropic family
    CLAUDE = "claude"

    # 智谱 AI 家族 / Zhipu AI family
    GLM_4 = "glm-4"
    GLM_4V = "glm-4v"
    GLM_3 = "glm-3"

    # 阿里云 家族 / Alibaba family
    QWEN = "qwen"

    # 百度 家族 / Baidu family
    ERNIE = "ernie"

    # 腾讯 家族 / Tencent family
    HUNYUAN = "hunyuan"

    # 月之暗面 家族 / Moonshot family
    MOONSHOT = "moonshot"

    # DeepSeek 家族 / DeepSeek family
    DEEPSEEK = "deepseek"

    # MiniMax 家族 / MiniMax family
    ABAB = "abab"

    UNKNOWN = "unknown"


@dataclass
class ModelInfo:
    """
    模型信息 / Model information
    """

    provider: Provider
    family: ModelFamily
    version: str
    variant: str
    capabilities: ModelCapabilities
    version_tuple: tuple[int, ...]
    variant_priority: tuple[int, ...] = (
        0,
    )  # 型号优先级元组，用于同版本不同型号的比较 / Variant priority tuple for comparing different variants of the same version


# 全局模型注册表 / Global model registry
# 格式: {"model_name": ModelInfo} 或 {"provider::model_name": ModelInfo}
# Format: {"model_name": ModelInfo} or {"provider::model_name": ModelInfo}
MODEL_REGISTRY: dict[str, ModelInfo] = {}

# 模型家族到默认Provider的映射 / Model family to default provider mapping
FAMILY_DEFAULT_PROVIDER: dict[ModelFamily, Provider] = {
    ModelFamily.GPT_4: Provider.OPENAI,
    ModelFamily.GPT_3_5: Provider.OPENAI,
    ModelFamily.O1: Provider.OPENAI,
    ModelFamily.O3: Provider.OPENAI,
    ModelFamily.CLAUDE: Provider.ANTHROPIC,
    ModelFamily.GLM_4: Provider.ZHIPU,
    ModelFamily.GLM_4V: Provider.ZHIPU,
    ModelFamily.GLM_3: Provider.ZHIPU,
    ModelFamily.QWEN: Provider.ALIBABA,
    ModelFamily.ERNIE: Provider.BAIDU,
    ModelFamily.HUNYUAN: Provider.TENCENT,
    ModelFamily.MOONSHOT: Provider.MOONSHOT,
    ModelFamily.DEEPSEEK: Provider.DEEPSEEK,
    ModelFamily.ABAB: Provider.MINIMAX,
}


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


def parse_model_name(model_name: str) -> tuple[Provider | None, str]:
    """
    解析模型名称，支持 {{Provider::ModelName}} 语法 / Parse model name, supporting {{Provider::ModelName}} syntax

    Args:
        model_name: 模型名称，可能包含provider前缀 / Model name, may include provider prefix

    Returns:
        tuple: (指定的Provider或None, 实际模型名称) / (specified Provider or None, actual model name)
    """
    if "::" in model_name:
        # 解析 {{Provider::ModelName}} 格式 / Parse {{Provider::ModelName}} format
        parts = model_name.split("::", 1)
        provider_str = parts[0].strip().strip("{}")
        actual_name = parts[1].strip()

        # 尝试匹配Provider / Try to match Provider
        try:
            provider = Provider(provider_str.lower())
            return provider, actual_name
        except ValueError:
            # 如果Provider不存在，忽略前缀 / If Provider doesn't exist, ignore prefix
            return None, actual_name

    return None, model_name


def get_model_info(model_name: str) -> ModelInfo:
    """
    获取模型信息 / Get model information

    支持以下格式: / Supports the following formats:
    1. "gpt-4" - 使用默认Provider / Use default Provider
    2. "{{openai::gpt-4}}" - 指定Provider / Specify Provider
    3. "openai::gpt-4" - 指定Provider（无大括号） / Specify Provider (without braces)

    Args:
        model_name: 模型名称 / Model name

    Returns:
        ModelInfo: 模型信息 / Model information
    """
    # 解析模型名称 / Parse model name
    specified_provider, actual_name = parse_model_name(model_name)
    model_lower = actual_name.lower()

    # 如果指定了Provider，优先查找 "provider::model_name" 格式的注册
    # If Provider is specified, prioritize "provider::model_name" format registration
    if specified_provider:
        provider_key = f"{specified_provider.value}::{model_lower}"
        if provider_key in MODEL_REGISTRY:
            return MODEL_REGISTRY[provider_key]

    # 检查注册表中是否有精确匹配 / Check if there's an exact match in the registry
    if model_lower in MODEL_REGISTRY:
        info = MODEL_REGISTRY[model_lower]
        # 如果指定了Provider且与注册的不同，创建新的ModelInfo
        # If Provider is specified and different from registered, create new ModelInfo
        if specified_provider and specified_provider != info.provider:
            return ModelInfo(
                provider=specified_provider,
                family=info.family,
                version=info.version,
                variant=info.variant,
                capabilities=info.capabilities,
                version_tuple=info.version_tuple,
                variant_priority=info.variant_priority,
            )
        return info

    # 检查是否有部分匹配 / Check if there's a partial match
    for registered_name, info in MODEL_REGISTRY.items():
        # 跳过带provider前缀的注册项 / Skip registrations with provider prefix
        if "::" in registered_name:
            continue
        if registered_name in model_lower or model_lower in registered_name:
            # 如果指定了Provider且与注册的不同，创建新的ModelInfo
            # If Provider is specified and different from registered, create new ModelInfo
            if specified_provider and specified_provider != info.provider:
                return ModelInfo(
                    provider=specified_provider,
                    family=info.family,
                    version=info.version,
                    variant=info.variant,
                    capabilities=info.capabilities,
                    version_tuple=info.version_tuple,
                    variant_priority=info.variant_priority,
                )
            return info

    # 如果没有找到，返回默认信息 / If not found, return default information
    provider = specified_provider or Provider.from_model_name(actual_name)

    return ModelInfo(
        provider=provider,
        family=ModelFamily.UNKNOWN,
        version="",
        variant="",
        capabilities=ModelCapabilities(),
        version_tuple=(0,),
        variant_priority=(0,),
    )
