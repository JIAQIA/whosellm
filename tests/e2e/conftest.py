"""E2E 元数据测试共享断言逻辑。

所有 Provider 的 test_*.py 共用此断言函数，确保检验规则一致。
"""

from whosellm import LLMeta


def assert_model_metadata(model_name: str, expected: dict) -> None:  # type: ignore[type-arg]
    """断言 LLMeta 解析结果与官方文档期望值一致。

    Args:
        model_name: 模型名称字符串
        expected: 官方文档采集的期望字典，必须包含 provider/family/version/variant，
                  可选包含 supports_* 和 context_window/max_tokens
    """
    model = LLMeta(model_name)

    # 身份标识 / Identity
    assert model.provider == expected["provider"], f"{model_name}: provider"
    assert model.family == expected["family"], f"{model_name}: family"
    assert model.version == expected["version"], f"{model_name}: version"
    assert model.variant == expected["variant"], f"{model_name}: variant"

    # 能力字段（仅断言 expected 中明确指定的）
    for key, value in expected.items():
        if key in ("provider", "family", "version", "variant"):
            continue
        if key in ("context_window", "max_tokens"):
            assert getattr(model.capabilities, key) == value, f"{model_name}: {key}"
        elif key.startswith("supports_"):
            assert getattr(model.capabilities, key) is value, f"{model_name}: {key}"
