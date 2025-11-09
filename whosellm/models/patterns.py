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
from datetime import date, datetime
from typing import Any

import parse  # type: ignore[import-untyped]

from whosellm.models.base import ModelFamily
from whosellm.provider import Provider


def _convert_variant(text: str) -> str:
    if not text:
        msg = "variant must be non-empty"
        raise ValueError(msg)

    first = text[0]
    if not first.isalpha():
        msg = "variant must start with a letter"
        raise ValueError(msg)

    for ch in text:
        if ch.isalnum() or ch == "-":
            continue
        msg = "variant may only contain letters, digits, or '-'"
        raise ValueError(msg)

    return text


DEFAULT_EXTRA_TYPES: dict[str, Any] = {"variant": _convert_variant}


def _merge_extra_types(extra_types: dict[str, Any] | None) -> dict[str, Any]:
    if not extra_types:
        return dict(DEFAULT_EXTRA_TYPES)

    merged = dict(DEFAULT_EXTRA_TYPES)
    merged.update(extra_types)
    return merged


def parse_pattern(
    pattern: str,
    text: str,
    *,
    extra_types: dict[str, Any] | None = None,
) -> parse.Result | None:
    try:
        return parse.parse(pattern, text, extra_types=_merge_extra_types(extra_types))
    except ValueError:
        return None


@dataclass
class ModelPattern:
    """
    模型命名模式 / Model naming pattern

    定义模型家族的命名规则和提取逻辑
    Defines naming rules and extraction logic for model families
    """

    family: ModelFamily
    provider: Provider
    patterns: list[str]
    version_default: str = ""

    def match(self, model_name: str) -> dict[str, Any] | None:
        model_lower = model_name.lower()

        for pattern in self.patterns:
            result = parse_pattern(pattern, model_lower)
            if result:
                matched = dict(result.named)
                if not matched.get("version"):
                    matched["version"] = self.version_default
                matched["family"] = self.family
                matched["provider"] = self.provider
                return matched

        return None


MODEL_PATTERNS: list[ModelPattern] = [
    ModelPattern(
        family=ModelFamily.GPT_4,
        provider=Provider.OPENAI,
        version_default="4.0",
        patterns=[
            "gpt-4-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "gpt-4-{variant:variant}-{mmdd:4d}",
            "gpt-4-{variant:variant}",
            "gpt-4",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GPT_4O,
        provider=Provider.OPENAI,
        version_default="4.0",
        patterns=[
            "gpt-4o-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "gpt-4o-{variant:variant}",
            "gpt-4o-{year:4d}-{month:2d}-{day:2d}",
            "gpt-4o",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GPT_3_5,
        provider=Provider.OPENAI,
        version_default="3.5",
        patterns=[
            "gpt-3.5-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "gpt-3.5-{variant:variant}",
            "gpt-3.5",
        ],
    ),
    ModelPattern(
        family=ModelFamily.O1,
        provider=Provider.OPENAI,
        version_default="1.0",
        patterns=[
            "o1-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "o1-{variant:variant}",
            "o1-{year:4d}-{month:2d}-{day:2d}",
            "o1",
        ],
    ),
    ModelPattern(
        family=ModelFamily.O3,
        provider=Provider.OPENAI,
        version_default="3.0",
        patterns=[
            "o3-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "o3-{variant:variant}",
            "o3",
        ],
    ),
    ModelPattern(
        family=ModelFamily.O4,
        provider=Provider.OPENAI,
        version_default="4.0",
        patterns=[
            "o4-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "o4-{variant:variant}",
        ],
    ),
    ModelPattern(
        family=ModelFamily.CLAUDE,
        provider=Provider.ANTHROPIC,
        version_default="3.0",
        patterns=[
            "claude-{version:d}-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "claude-{version:d}-{variant:variant}",
            "claude-{variant:variant}",
            "claude",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GLM_4V,
        provider=Provider.ZHIPU,
        version_default="4.0",
        patterns=[
            "glm-4v-{variant:variant}-{mmdd:4d}",
            "glm-4v-{variant:variant}",
            "glm-4v",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GLM_45,
        provider=Provider.ZHIPU,
        version_default="4.5",
        patterns=[
            "glm-4.5-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "glm-4.5-{variant:variant}-{mmdd:4d}",
            "glm-4.5-{variant:variant}",
            "glm-4.5-{year:4d}-{month:2d}-{day:2d}",
            "glm-4.5-{mmdd:4d}",
            "glm-4.5",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GLM_45V,
        provider=Provider.ZHIPU,
        version_default="4.5",
        patterns=[
            "glm-4.5v-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "glm-4.5v-{variant:variant}-{mmdd:4d}",
            "glm-4.5v-{variant:variant}",
            "glm-4.5v-{year:4d}-{month:2d}-{day:2d}",
            "glm-4.5v-{mmdd:4d}",
            "glm-4.5v",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GLM_46,
        provider=Provider.ZHIPU,
        version_default="4.6",
        patterns=[
            "glm-4.6-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "glm-4.6-{variant:variant}-{mmdd:4d}",
            "glm-4.6-{variant:variant}",
            "glm-4.6-{year:4d}-{month:2d}-{day:2d}",
            "glm-4.6-{mmdd:4d}",
            "glm-4.6",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GLM_4,
        provider=Provider.ZHIPU,
        version_default="4.0",
        patterns=[
            "glm-4-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
            "glm-4-{variant:variant}",
            "glm-4",
        ],
    ),
    ModelPattern(
        family=ModelFamily.GLM_3,
        provider=Provider.ZHIPU,
        version_default="3.0",
        patterns=[
            "glm-3-{variant:variant}",
            "glm-3",
        ],
    ),
    ModelPattern(
        family=ModelFamily.QWEN,
        provider=Provider.ALIBABA,
        version_default="1.0",
        patterns=[
            "qwen-{version:d}-{variant:variant}",
            "qwen-{variant:variant}",
            "qwen",
        ],
    ),
    ModelPattern(
        family=ModelFamily.ERNIE,
        provider=Provider.BAIDU,
        version_default="1.0",
        patterns=[
            "ernie-{version:d}-{variant:variant}",
            "ernie-{variant:variant}",
            "ernie",
        ],
    ),
    ModelPattern(
        family=ModelFamily.HUNYUAN,
        provider=Provider.TENCENT,
        version_default="1.0",
        patterns=[
            "hunyuan-{variant:variant}",
            "hunyuan",
        ],
    ),
    ModelPattern(
        family=ModelFamily.MOONSHOT,
        provider=Provider.MOONSHOT,
        version_default="1.0",
        patterns=[
            "moonshot-{version:d}-{variant:variant}",
            "moonshot-{variant:variant}",
            "moonshot",
        ],
    ),
    ModelPattern(
        family=ModelFamily.DEEPSEEK,
        provider=Provider.DEEPSEEK,
        version_default="1.0",
        patterns=[
            "deepseek-{variant:variant}-v{version:d}",
            "deepseek-{variant:variant}",
            "deepseek",
        ],
    ),
    ModelPattern(
        family=ModelFamily.ABAB,
        provider=Provider.MINIMAX,
        version_default="1.0",
        patterns=[
            "abab-{version:d}-{variant:variant}",
            "abab-{variant:variant}",
            "abab",
        ],
    ),
]


def match_model_pattern(model_name: str) -> dict[str, Any] | None:
    for pattern in MODEL_PATTERNS:
        result = pattern.match(model_name)
        if result:
            return result

    return None


def parse_date_from_match(matched: dict[str, Any]) -> date | None:
    if all(k in matched for k in ["year", "month", "day"]):
        try:
            return date(matched["year"], matched["month"], matched["day"])
        except (ValueError, TypeError):
            pass

    if "mmdd" in matched:
        try:
            mmdd_str = str(matched["mmdd"]).zfill(4)
            month = int(mmdd_str[:2])
            day = int(mmdd_str[2:])
            # 默认当前年份
            year = datetime.now().year
            return date(year=year, month=month, day=day)
        except (ValueError, TypeError):
            pass

    return None


def normalize_variant(variant: str | None) -> str:
    if not variant:
        return "base"

    variant = variant.lower().strip()

    suffixes_to_remove = ["custom", "test", "latest", "new", "experimental", "v1", "v2", "v3"]

    parts = variant.split("-")

    filtered_parts = [p for p in parts if p not in suffixes_to_remove]

    if filtered_parts:
        return "-".join(filtered_parts)

    return "base"
