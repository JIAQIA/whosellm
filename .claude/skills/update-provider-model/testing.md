# 测试最佳实践

## 测试文件位置

- 家族级测试：`tests/models/families/test_{family}.py`
- 跨家族集成测试：`tests/test_llmeta.py`、`tests/test_model_version.py`

## 必须覆盖的测试维度

每个新增/修改的模型家族，**至少**包含以下测试：

### 1. 家族默认能力测试

验证 `get_default_capabilities()` 返回的能力与官方文档一致。

```python
def test_{family}_base_defaults():
    """验证家族默认能力"""
    capabilities = get_default_capabilities(ModelFamily.MY_MODEL)
    assert capabilities.supports_streaming is True
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_fine_tuning is False  # 明确断言 False 的也要写
```

### 2. 特定模型配置测试

每个 `specific_models` 条目都需要独立的测试函数。使用辅助函数减少重复：

```python
def _assert_specific_config(
    name: str,
    variant: str,
    *,
    streaming: bool,
    function_calling: bool,
    # ... 其他关键能力
) -> None:
    config = get_specific_model_config(name)
    assert config is not None
    version, cfg_variant, capabilities = config
    assert cfg_variant == variant
    assert capabilities is not None
    assert capabilities.supports_streaming is streaming
    assert capabilities.supports_function_calling is function_calling

def test_{family}_pro_specific_model():
    """验证 pro 变体能力"""
    _assert_specific_config("my-model-pro", "pro", streaming=True, function_calling=True)
```

### 3. 模式匹配测试

每种命名模式至少一个测试用例，**特别是带日期的模式**：

```python
def test_{family}_base_with_date_pattern():
    """验证带日期的模型匹配"""
    matched = match_model_pattern("my-model-2025-04-16")
    assert matched is not None
    assert matched["family"] == ModelFamily.MY_MODEL
    assert matched["variant"] == "base"

def test_{family}_variant_with_date_pattern():
    """验证带日期的变体匹配"""
    matched = match_model_pattern("my-model-pro-2025-06-10")
    assert matched is not None
    assert matched["family"] == ModelFamily.MY_MODEL
    assert matched["_from_specific_model"] == "my-model-pro"
    assert matched["variant"] == "pro"
```

### 4. LLMeta 端到端测试

验证从模型名称到完整 LLMeta 对象的完整链路：

```python
def test_{family}_llmeta_integration():
    """端到端：模型名称 → LLMeta 对象"""
    model = LLMeta("my-model-pro")
    assert model.provider == Provider.MY_PROVIDER
    assert model.family == ModelFamily.MY_MODEL
    assert model.variant == "pro"
    assert model.capabilities.supports_streaming is True
```

### 5. 版本比较测试（如同一家族有多个版本/变体）

```python
def test_{family}_variant_ordering():
    """验证变体优先级排序"""
    mini = LLMeta("my-model-mini")
    base = LLMeta("my-model")
    pro = LLMeta("my-model-pro")
    assert mini < base < pro
```

## 测试风格规范

- 测试函数使用双语注释：`"""验证 xxx / Validate xxx"""`
- 对 `False` 的能力也要**显式断言**，确保不是默认值恰好匹配
- 使用 `@pytest.mark.parametrize` 做批量变体验证
- 不要 mock 注册表——直接测试真实注册链路
- 测试文件头部注释遵循项目风格（filename、Time、Author、Email、Software）
