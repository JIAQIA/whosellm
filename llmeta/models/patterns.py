# filename: patterns.py
# @Time    : 2025/11/7 17:06
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
模型命名模式定义 / Model naming pattern definitions

使用 parse 库进行模式匹配，提供清晰、高性能的模型名称解析
Using parse library for pattern matching, providing clear and high-performance model name parsing
"""

from dataclasses import dataclass
from datetime import date
from typing import Any

import parse  # type: ignore[import-untyped]

from llmeta.models.base import ModelFamily
from llmeta.provider import Provider


@dataclass
class ModelPattern:
    """
    模型命名模式 / Model naming pattern

    定义模型家族的命名规则和提取逻辑
    Defines naming rules and extraction logic for model families
    """

    family: ModelFamily
    provider: Provider
    patterns: list[str]  # 多个模式，按优先级排序 / Multiple patterns, ordered by priority
    version_default: str = ""  # 默认版本 / Default version

    def match(self, model_name: str) -> dict[str, Any] | None:
        """
        尝试匹配模型名称 / Try to match model name

        Args:
            model_name: 模型名称 / Model name

        Returns:
            dict | None: 匹配结果字典或None / Match result dict or None
        """
        model_lower = model_name.lower()

        for pattern in self.patterns:
            result = parse.parse(pattern, model_lower)
            if result:
                # 转换为字典并添加默认值 / Convert to dict and add defaults
                matched = dict(result.named)
                if not matched.get("version"):
                    matched["version"] = self.version_default
                matched["family"] = self.family
                matched["provider"] = self.provider
                return matched

        return None


# 定义所有模型家族的命名模式 / Define naming patterns for all model families
# 模式语法说明 / Pattern syntax:
# - {} 表示任意字符 / {} means any characters
# - {:d} 表示整数 / {:d} means integer
# - {:w} 表示单词字符 / {:w} means word characters
# - 可选部分用多个模式表示 / Optional parts are represented by multiple patterns

MODEL_PATTERNS: list[ModelPattern] = [
    # OpenAI GPT-4 系列 / OpenAI GPT-4 series
    ModelPattern(
        family=ModelFamily.GPT_4,
        provider=Provider.OPENAI,
        version_default="4.0",
        patterns=[
            "gpt-4o-{variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-4o-mini-2024-07-18
            "gpt-4o-{variant}",  # gpt-4o-mini
            "gpt-4-{variant}-{year:4d}-{month:2d}-{day:2d}",  # gpt-4-turbo-2024-04-09
            "gpt-4-{variant}-{mmdd:4d}",  # gpt-4-0125-preview
            "gpt-4-{variant}",  # gpt-4-turbo, gpt-4-plus, gpt-4-custom
            "gpt-4o",  # gpt-4o (base)
            "gpt-4",  # gpt-4 (base)
        ],
    ),
    # OpenAI GPT-3.5 系列 / OpenAI GPT-3.5 series
    ModelPattern(
        family=ModelFamily.GPT_3_5,
        provider=Provider.OPENAI,
        version_default="3.5",
        patterns=[
            "gpt-3.5-{variant}-{year:4d}-{month:2d}-{day:2d}",
            "gpt-3.5-{variant}",
            "gpt-3.5",
        ],
    ),
    # OpenAI O1 系列 / OpenAI O1 series
    ModelPattern(
        family=ModelFamily.O1,
        provider=Provider.OPENAI,
        version_default="1.0",
        patterns=[
            "o1-{variant}-{year:4d}-{month:2d}-{day:2d}",
            "o1-{variant}",
            "o1",
        ],
    ),
    # OpenAI O3 系列 / OpenAI O3 series
    ModelPattern(
        family=ModelFamily.O3,
        provider=Provider.OPENAI,
        version_default="3.0",
        patterns=[
            "o3-{variant}-{year:4d}-{month:2d}-{day:2d}",
            "o3-{variant}",
            "o3",
        ],
    ),
    # Anthropic Claude 系列 / Anthropic Claude series
    ModelPattern(
        family=ModelFamily.CLAUDE,
        provider=Provider.ANTHROPIC,
        version_default="3.0",
        patterns=[
            "claude-{version:d}-{variant}-{year:4d}-{month:2d}-{day:2d}",
            "claude-{version:d}-{variant}",
            "claude-{variant}",
            "claude",
        ],
    ),
    # 智谱 GLM-4V 系列（必须在 GLM-4 之前） / Zhipu GLM-4V series (must be before GLM-4)
    ModelPattern(
        family=ModelFamily.GLM_4V,
        provider=Provider.ZHIPU,
        version_default="4.0",
        patterns=[
            "glm-4v-{variant}-{mmdd:4d}",  # glm-4v-plus-0111
            "glm-4v-{variant}",  # glm-4v-plus, glm-4v-flash
            "glm-4v",  # glm-4v (base)
        ],
    ),
    # 智谱 GLM-4 系列 / Zhipu GLM-4 series
    ModelPattern(
        family=ModelFamily.GLM_4,
        provider=Provider.ZHIPU,
        version_default="4.0",
        patterns=[
            "glm-4-{variant}-{year:4d}-{month:2d}-{day:2d}",
            "glm-4-{variant}",
            "glm-4",
        ],
    ),
    # 智谱 GLM-3 系列 / Zhipu GLM-3 series
    ModelPattern(
        family=ModelFamily.GLM_3,
        provider=Provider.ZHIPU,
        version_default="3.0",
        patterns=[
            "glm-3-{variant}",
            "glm-3",
        ],
    ),
    # 阿里 Qwen 系列 / Alibaba Qwen series
    ModelPattern(
        family=ModelFamily.QWEN,
        provider=Provider.ALIBABA,
        version_default="1.0",
        patterns=[
            "qwen-{version:d}-{variant}",
            "qwen-{variant}",
            "qwen",
        ],
    ),
    # 百度 ERNIE 系列 / Baidu ERNIE series
    ModelPattern(
        family=ModelFamily.ERNIE,
        provider=Provider.BAIDU,
        version_default="1.0",
        patterns=[
            "ernie-{version:d}-{variant}",
            "ernie-{variant}",
            "ernie",
        ],
    ),
    # 腾讯混元系列 / Tencent Hunyuan series
    ModelPattern(
        family=ModelFamily.HUNYUAN,
        provider=Provider.TENCENT,
        version_default="1.0",
        patterns=[
            "hunyuan-{variant}",
            "hunyuan",
        ],
    ),
    # 月之暗面 Moonshot 系列 / Moonshot series
    ModelPattern(
        family=ModelFamily.MOONSHOT,
        provider=Provider.MOONSHOT,
        version_default="1.0",
        patterns=[
            "moonshot-{version:d}-{variant}",
            "moonshot-{variant}",
            "moonshot",
        ],
    ),
    # DeepSeek 系列 / DeepSeek series
    ModelPattern(
        family=ModelFamily.DEEPSEEK,
        provider=Provider.DEEPSEEK,
        version_default="1.0",
        patterns=[
            "deepseek-{variant}-v{version:d}",  # deepseek-chat-v2
            "deepseek-{variant}",
            "deepseek",
        ],
    ),
    # MiniMax ABAB 系列 / MiniMax ABAB series
    ModelPattern(
        family=ModelFamily.ABAB,
        provider=Provider.MINIMAX,
        version_default="1.0",
        patterns=[
            "abab-{version:d}-{variant}",
            "abab-{variant}",
            "abab",
        ],
    ),
]


def match_model_pattern(model_name: str) -> dict[str, Any] | None:
    """
    使用模式匹配解析模型名称 / Parse model name using pattern matching

    Args:
        model_name: 模型名称 / Model name

    Returns:
        dict | None: 匹配结果或None / Match result or None
    """
    for pattern in MODEL_PATTERNS:
        result = pattern.match(model_name)
        if result:
            return result

    return None


def parse_date_from_match(matched: dict[str, Any]) -> date | None:
    """
    从匹配结果中解析日期 / Parse date from match result

    Args:
        matched: 匹配结果字典 / Match result dict

    Returns:
        date | None: 解析的日期或None / Parsed date or None
    """
    # 尝试解析完整日期 YYYY-MM-DD / Try to parse full date YYYY-MM-DD
    if all(k in matched for k in ["year", "month", "day"]):
        try:
            return date(matched["year"], matched["month"], matched["day"])
        except (ValueError, TypeError):
            pass

    # 尝试解析 MMDD 格式（假设为2024年） / Try to parse MMDD format (assume 2024)
    if "mmdd" in matched:
        try:
            mmdd_str = str(matched["mmdd"]).zfill(4)
            month = int(mmdd_str[:2])
            day = int(mmdd_str[2:])
            return date(2024, month, day)
        except (ValueError, TypeError):
            pass

    return None


def normalize_variant(variant: str | None) -> str:
    """
    规范化型号名称 / Normalize variant name


    Args:
        variant: 原始型号名称 / Original variant name

    Returns:
        str: 规范化后的型号名称 / Normalized variant name
    """
    if not variant:
        return "base"

    # 移除常见的后缀 / Remove common suffixes
    variant = variant.lower().strip()

    # 定义需要移除的后缀 / Define suffixes to remove
    suffixes_to_remove = ["custom", "test", "latest", "new", "experimental", "v1", "v2", "v3"]

    # 分割型号名称 / Split variant name
    parts = variant.split("-")

    # 过滤掉后缀 / Filter out suffixes
    filtered_parts = [p for p in parts if p not in suffixes_to_remove]

    if filtered_parts:
        return "-".join(filtered_parts)

    return "base"
