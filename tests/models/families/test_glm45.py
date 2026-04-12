"""GLM-4.5 模型家族测试 / GLM-4.5 model family tests."""

from whosellm.models.base import ModelFamily
from whosellm.models.registry import match_model_pattern


def test_glm45_no_structured_outputs() -> None:
    """验证 glm-4.5 不支持 structured_outputs（ZhipuAI 仅支持 json_object，不支持 json_schema）"""
    matched = match_model_pattern("glm-4.5")

    assert matched is not None
    assert matched["family"] == ModelFamily.GLM

    capabilities = matched["capabilities"]
    assert capabilities.supports_structured_outputs is False, (
        "glm-4.5: ZhipuAI API 仅支持 response_format={type:'json_object'}，"
        "不支持 json_schema 类型，supports_structured_outputs 应为 False"
    )
    assert capabilities.supports_json_outputs is True, (
        "glm-4.5: ZhipuAI API 支持 response_format={type:'json_object'}，supports_json_outputs 应为 True"
    )
