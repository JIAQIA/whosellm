# 如何添加新的模型家族 / How to Add a New Model Family

本文档介绍如何在 whosellm 中添加新的模型家族支持。

This document explains how to add support for a new model family in whosellm.

---

## 📋 添加步骤概览 / Steps Overview

添加新模型家族有 **2 种方式**：

There are **2 ways** to add a new model family:

### 方式 A：静态配置（推荐用于内置模型）/ Method A: Static Configuration (Recommended for Built-in Models)

1. **在 `base.py` 中定义模型家族枚举** / Define model family enum in `base.py`
2. **在 `families/` 目录中创建配置** / Create configuration in `families/` directory

### 方式 B：动态注册（推荐用于用户自定义模型）/ Method B: Dynamic Registration (Recommended for User-defined Models)

1. **使用 `add_member()` 动态添加枚举成员** / Use `add_member()` to dynamically add enum members
2. **使用 `register_family()` 函数动态注册配置** / Use `register_family()` function to register configuration

就这么简单！✨

That's it! ✨

---

## 方式 A：静态配置（推荐用于内置模型）/ Method A: Static Configuration (Recommended for Built-in Models)

### 步骤 1: 定义模型家族枚举 / Step 1: Define Model Family Enum

在 `whosellm/models/base.py` 的 `ModelFamily` 枚举中添加新的家族：

Add a new family to the `ModelFamily` enum in `whosellm/models/base.py`:

```python
class ModelFamily(str, Enum):
    """
    模型家族枚举 / Model family enum
    """
    
    # 现有的家族 / Existing families
    GPT_4 = "gpt-4"
    CLAUDE = "claude"
    # ... 其他家族
    
    # 添加新家族 / Add new family
    GEMINI = "gemini"  # 示例：添加 Google Gemini
    LLAMA = "llama"    # 示例：添加 Meta Llama
    
    UNKNOWN = "unknown"
```

**命名规范 / Naming Convention:**
- 枚举名使用大写下划线格式 / Use UPPER_SNAKE_CASE for enum names
- 枚举值使用小写连字符格式 / Use lowercase-with-hyphens for enum values
- 枚举值应该是模型名称的核心标识 / Enum value should be the core identifier of the model name

---

### 步骤 2: 创建家族配置 / Step 2: Create Family Configuration

在 `whosellm/models/families/` 目录中创建或编辑提供商配置文件：

Create or edit a provider configuration file in `whosellm/models/families/`:

**选项 A：添加到现有提供商文件** / Option A: Add to existing provider file

如果是已有提供商的新家族，编辑对应文件（如 `openai.py`, `zhipu.py`）

If it's a new family from an existing provider, edit the corresponding file (e.g., `openai.py`, `zhipu.py`)

**选项 B：创建新提供商文件** / Option B: Create new provider file

如果是新提供商，创建新文件（如 `google.py`）

If it's a new provider, create a new file (e.g., `google.py`)

```python
# whosellm/models/families/google.py
# -*- coding: utf-8 -*-
# filename: google.py
# @Time    : 2025/11/7 17:45
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Google 模型家族配置 / Google model family configurations
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig
from whosellm.provider import Provider

# ============================================================================
# Gemini 系列 / Gemini Series
# ============================================================================

GEMINI = ModelFamilyConfig(
    family=ModelFamily.GEMINI,
    provider=Provider.GOOGLE,
    version_default="1.0",
    patterns=[
        "gemini-{version:d}-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",  # gemini-1-pro-2024-01-15
        "gemini-{version:d}-{variant:variant}",  # gemini-1-pro, gemini-1-ultra
        "gemini-{variant:variant}",              # gemini-pro
        "gemini",                        # gemini (base)
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_video=True,
        supports_pdf=True,
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=1000000,  # 1M tokens
    ),
)
```

然后在 `families/__init__.py` 中导入：

Then import it in `families/__init__.py`:

```python
from whosellm.models.families import (
    alibaba,
    anthropic,
    google,  # 添加新的 / Add new
    openai,
    others,
    zhipu,
)

__all__ = [
    "openai",
    "anthropic",
    "zhipu",
    "alibaba",
    "google",  # 添加新的 / Add new
    "others",
]
```

### 模式语法说明 / Pattern Syntax

| 语法 / Syntax | 说明 / Description | 示例 / Example |
|--------------|-------------------|----------------|
| `{variant:variant}` | 匹配任意字符作为型号 / Match any characters as variant | `pro`, `ultra`, `mini` |
| `{version:d}` | 匹配整数作为版本号 / Match integer as version | `1`, `2`, `3` |
| `{year:4d}` | 匹配4位数字作为年份 / Match 4-digit year | `2024`, `2025` |
| `{month:2d}` | 匹配2位数字作为月份 / Match 2-digit month | `01`, `12` |
| `{day:2d}` | 匹配2位数字作为日期 / Match 2-digit day | `01`, `31` |
| `{mmdd:4d}` | 匹配4位数字作为月日 / Match 4-digit MMDD | `0115`, `1231` |

### 模式优先级 / Pattern Priority

- **模式按顺序匹配** / Patterns are matched in order
- **更具体的模式应该放在前面** / More specific patterns should come first
- **示例顺序** / Example order:
  1. 带完整日期的模式 / Patterns with full date
  2. 带型号的模式 / Patterns with variant
  3. 基础模式 / Base patterns

### 配置字段说明 / Configuration Fields

`ModelFamilyConfig` 包含以下字段：

`ModelFamilyConfig` contains the following fields:

| 字段 / Field | 类型 / Type | 说明 / Description |
|-------------|------------|-------------------|
| `family` | `ModelFamily` | 模型家族枚举 / Model family enum |
| `provider` | `Provider` | 提供商枚举 / Provider enum |
| `patterns` | `list[str]` | 命名模式列表 / List of naming patterns |
| `version_default` | `str` | 默认版本号 / Default version |
| `capabilities` | `ModelCapabilities` | 默认能力配置 / Default capabilities |

### 能力字段说明 / Capability Fields

| 字段 / Field | 类型 / Type | 说明 / Description |
|-------------|------------|-------------------|
| `supports_thinking` | `bool` | 是否支持思考（推理）模式 / Supports thinking (reasoning) mode |
| `supports_vision` | `bool` | 是否支持图片输入 / Supports image input |
| `supports_audio` | `bool` | 是否支持音频输入 / Supports audio input |
| `supports_video` | `bool` | 是否支持视频输入 / Supports video input |
| `supports_pdf` | `bool` | 是否支持 PDF 输入 / Supports PDF input |
| `supports_function_calling` | `bool` | 是否支持函数调用 / Supports function calling |
| `supports_streaming` | `bool` | 是否支持流式输出 / Supports streaming output |
| `max_tokens` | `int \| None` | 最大 token 数 / Maximum tokens |
| `context_window` | `int \| None` | 上下文窗口大小 / Context window size |
| `max_image_size_mb` | `float \| None` | 最大图片大小(MB) / Max image size in MB |
| `max_image_pixels` | `tuple[int, int] \| None` | 最大图片像素(宽, 高) / Max image pixels (width, height) |
| `max_video_size_mb` | `float \| None` | 最大视频大小(MB) / Max video size in MB |
| `max_video_duration_seconds` | `int \| None` | 最大视频时长(秒) / Max video duration in seconds |
| `media_count_limit` | `MediaCountLimit` | 单请求媒体数量上限 / Per-request media count caps |
| `max_inline_media_bytes` | `int \| None` | 单请求内联媒体字节总预算 / Per-request inline-media byte budget |
| `max_pdf_size_mb` | `float \| None` | PDF 大小上限(MB) / Max PDF size in MB |
| `max_pdf_pages` | `int \| None` | PDF 页数上限 / Max PDF pages per request |
| `max_document_size_mb` | `float \| None` | 非 PDF 文档大小上限(MB，预留) / Max non-PDF document size |
| `supported_document_mime_type` | `list[str]` | 支持的文档 MIME / Supported document MIME types |
| `tool_result_surfaces` | `dict[LLMApiSurface, ToolResultSurfaceCapability]` | 工具结果按 API surface 的原生媒体能力；缺键 = 未声明，空元组 = 明确不支持 / Native tool-result media capability per surface; missing = undeclared, empty tuple = unsupported |
| `file_api` | `FileApiCapability \| None` | 文件 API 能力（预留）/ File API capability (reserved) |

工具结果能力是 **provider × API surface** 维度，而不是模型维度。新增模型时应按官方文档登记 `tool_result_surfaces`，并注明来源与抓取日期；未查证的 surface 请保持缺键（内核按不支持处理），不要乐观填写。

Tool-result capability is **provider × API surface**, not per-model. When adding models, register `tool_result_surfaces` from official docs with source and fetch date; leave unverified surfaces undeclared (consumers treat them as unsupported) instead of guessing.

---

## 方式 B：动态注册 / Method B: Dynamic Registration

**完全无需修改源代码！** 第三方用户可以在运行时动态扩展枚举和注册模型家族。

**No source code modification needed!** Third-party users can dynamically extend enums and register model families at runtime.

```python
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig
from whosellm.models.registry import register_family
from whosellm.provider import Provider
from whosellm.capabilities import ModelCapabilities
from whosellm import whosellm

# 1. 动态添加 Provider 枚举成员 / Dynamically add Provider enum member
Provider.add_member('GOOGLE', 'google')

# 2. 动态添加 ModelFamily 枚举成员 / Dynamically add ModelFamily enum member
ModelFamily.add_member('GEMINI', 'gemini')

# 3. 创建配置并动态注册 / Create configuration and register dynamically
gemini_config = ModelFamilyConfig(
    family=ModelFamily.GEMINI,  # 使用动态添加的枚举成员
    provider=Provider.GOOGLE,    # 使用动态添加的枚举成员
    version_default="1.0",
    patterns=[
        "gemini-{version:d}-{variant:variant}",
        "gemini-{variant:variant}",
        "gemini",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_video=True,
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=1000000,
    ),
)

# 4. 动态注册配置 / Register configuration dynamically
register_family(gemini_config)

# 5. 现在可以使用了！/ Now you can use it!
model = whosellm("gemini-pro")
print(f"Family: {model.family}")  # ModelFamily.GEMINI
print(f"Provider: {model.provider}")  # Provider.GOOGLE
print(f"Supports vision: {model.capabilities.supports_vision}")  # True
print(f"Context window: {model.capabilities.context_window:,}")  # 1,000,000
```

**优势 / Advantages:**
- ✅ **完全无需修改源代码** / **No source code modification needed at all**
- ✅ **动态枚举扩展** / **Dynamic enum extension**
- ✅ 适合第三方用户和插件 / Suitable for third-party users and plugins
- ✅ 可以在配置文件中定义 / Can be defined in configuration files
- ✅ 支持运行时热加载 / Supports runtime hot-loading

**注意 / Note:**
- 动态注册的配置在程序重启后会丢失，需要重新注册
- Dynamically registered configurations are lost after program restart and need to be re-registered
- 建议在应用启动时统一注册所有自定义模型
- Recommended to register all custom models at application startup

---

## 步骤 3 (可选): 添加 Provider / Step 3 (Optional): Add Provider

如果新模型家族来自新的提供商，需要在 `whosellm/provider.py` 中添加：

If the new model family is from a new provider, add it to `whosellm/provider.py`:

```python
class Provider(str, Enum):
    """
    支持的模型提供商 / Supported model providers
    """
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    # ... 其他提供商
    
    # 添加新提供商 / Add new provider
    GOOGLE = "google"
    META = "meta"
    
    UNKNOWN = "unknown"
    
    @classmethod
    def from_model_name(cls, model_name: str) -> "Provider":
        """从模型名称推断提供商"""
        model_lower = model_name.lower()
        
        provider_keywords = {
            cls.OPENAI: ["gpt", "o1", "o3"],
            cls.ANTHROPIC: ["claude"],
            # ... 其他映射
            
            # 添加新映射 / Add new mapping
            cls.GOOGLE: ["gemini", "palm", "bard"],
            cls.META: ["llama"],
        }
        
        for provider, keywords in provider_keywords.items():
            match any(keyword in model_lower for keyword in keywords):
                case True:
                    return provider
        
        return cls.UNKNOWN
```

---

## 步骤 4 (可选): 添加预注册模型 / Step 4 (Optional): Add Pre-registered Models

如果需要为特定模型变体提供精确配置，可以在配置中使用 `specific_models` 字段：

If you need precise configuration for specific model variants, use the `specific_models` field in the configuration:

```python
GEMINI = ModelFamilyConfig(
    family=ModelFamily.GEMINI,
    provider=Provider.GOOGLE,
    version_default="1.0",
    patterns=[
        "gemini-{version:d}-{variant:variant}",
        "gemini-{variant:variant}",
        "gemini",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=1000000,
    ),
    # 为特定模型提供自定义配置 / Provide custom config for specific models
    specific_models={
        "gemini-1-pro": ("1.0", "pro", ModelCapabilities(
            supports_vision=True,
            supports_function_calling=True,
            supports_streaming=True,
            max_tokens=8192,
            context_window=32000,  # Pro 版本上下文窗口较小
        )),
        "gemini-1-ultra": ("1.0", "ultra", None),  # 使用默认能力
    },
)
```

**注意**：大多数情况下不需要使用 `specific_models`，自动注册已经足够。

**Note**: In most cases, `specific_models` is not needed; auto-registration is sufficient.

---

## 📝 完整示例：添加 Gemini 家族 / Complete Example: Adding Gemini Family

### 1. 在 `base.py` 中添加枚举

```python
class ModelFamily(str, Enum):
    # ... 现有家族
    GEMINI = "gemini"
    UNKNOWN = "unknown"
```

### 2. 在 `provider.py` 中添加提供商（如果需要）

```python
class Provider(str, Enum):
    # ... 现有提供商
    GOOGLE = "google"
    UNKNOWN = "unknown"

    @classmethod
    def from_model_name(cls, model_name: str) -> "Provider":
        provider_keywords = {
            # ... 现有映射
            cls.GOOGLE: ["gemini", "palm", "bard"],
        }
        # ... 其余代码
```

### 3. 创建 `families/google.py`

```python
# -*- coding: utf-8 -*-
# filename: google.py
# @Time    : 2025/11/7 17:45
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Google 模型家族配置 / Google model family configurations
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig
from whosellm.provider import Provider

GEMINI = ModelFamilyConfig(
    family=ModelFamily.GEMINI,
    provider=Provider.GOOGLE,
    version_default="1.0",
    patterns=[
        "gemini-{version:d}-{variant:variant}-{year:4d}-{month:2d}-{day:2d}",
        "gemini-{version:d}-{variant:variant}",
        "gemini-{variant:variant}",
        "gemini",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_video=True,
        supports_pdf=True,
        supports_function_calling=True,
        supports_streaming=True,
        max_tokens=8192,
        context_window=1000000,
    ),
)
```

### 4. 在 `families/__init__.py` 中导入

```python
from whosellm.models.families import (
    alibaba,
    anthropic,
    google,  # 新增
    openai,
    others,
    zhipu,
)

__all__ = [
    "openai",
    "anthropic",
    "zhipu",
    "alibaba",
    "google",  # 新增
    "others",
]
```

### 4. 测试

```python
from whosellm import whosellm

# 测试自动注册
model = whosellm("gemini-1-pro")
print(f"Family: {model.family}")  # GEMINI
print(f"Provider: {model.provider}")  # GOOGLE
print(f"Version: {model.version_default}")  # 1.0
print(f"Variant: {model.variant_default}")  # pro
print(f"Supports vision: {model.capabilities.supports_vision}")  # True

# 测试新变体自动注册
model2 = whosellm("gemini-2-flash")
print(f"Variant: {model2.variant_default}")  # flash
# 自动继承 GEMINI 家族的默认能力
```

---

## ✅ 验证清单 / Verification Checklist

添加完成后，请确认以下事项：

After adding, please verify the following:

- [ ] `ModelFamily` 枚举中已添加新家族 / New family added to `ModelFamily` enum
- [ ] `Provider` 枚举中已添加新提供商（如需要） / New provider added to `Provider` enum (if needed)
- [ ] 在 `families/` 中创建了配置文件 / Configuration file created in `families/`
- [ ] 在 `families/__init__.py` 中导入了新配置 / New configuration imported in `families/__init__.py`
- [ ] 模式顺序正确（更具体的在前） / Pattern order is correct (more specific first)
- [ ] 能力配置准确反映模型实际能力 / Capabilities accurately reflect model's actual abilities
- [ ] 运行测试确保没有破坏现有功能 / Run tests to ensure no existing functionality is broken
- [ ] 运行 `mypy` 类型检查通过 / Run `mypy` type checking passes

---

## 🧪 编写测试 / Writing Tests

建议为新模型家族添加测试用例：

It's recommended to add test cases for the new model family:

```python
# tests/test_gemini.py
import unittest
from whosellm import whosellm, ModelFamily, Provider


class TestGemini(unittest.TestCase):
    def test_gemini_auto_register(self):
        """测试 Gemini 自动注册"""
        model = whosellm("gemini-1-pro")

        assert model.family == ModelFamily.GEMINI
        assert model.provider == Provider.GOOGLE
        assert model.version_default == "1.0"
        assert model.variant_default == "pro"
        assert model.capabilities.supports_vision is True
        assert model.capabilities.context_window == 1000000

    def test_gemini_variant_comparison(self):
        """测试 Gemini 型号比较"""
        flash = whosellm("gemini-flash")
        pro = whosellm("gemini-pro")
        ultra = whosellm("gemini-ultra")

        assert flash < pro < ultra
```

---

## 💡 最佳实践 / Best Practices

1. **配置集中** / Centralized Configuration
   - 一个家族的所有信息放在一个 `ModelFamilyConfig` 对象中
   - All information for a family in one `ModelFamilyConfig` object
   - 按提供商组织文件，保持文件大小可控
   - Organize files by provider, keep file size manageable

2. **命名一致性** / Naming Consistency
   - 模型家族名称应与实际模型名称保持一致
   - Model family names should match actual model names
   - 枚举值使用小写连字符格式
   - Use lowercase-with-hyphens for enum values

3. **模式完整性** / Pattern Completeness
   - 考虑所有可能的命名变体
   - Consider all possible naming variants
   - 包含带日期和不带日期的模式
   - Include patterns with and without dates
   - 更具体的模式放在前面
   - More specific patterns come first

4. **能力准确性** / Capability Accuracy
   - 根据官方文档配置能力
   - Configure capabilities based on official documentation
   - 保守估计限制值
   - Be conservative with limit values

5. **向后兼容** / Backward Compatibility
   - 不要修改现有家族的枚举值
   - Don't modify existing family enum values
   - 新家族添加在 UNKNOWN 之前
   - Add new families before UNKNOWN

6. **代码质量** / Code Quality
   - 添加中英文双语注释
   - Add bilingual comments (Chinese and English)
   - 运行 `mypy` 和 `ruff` 检查
   - Run `mypy` and `ruff` checks
   - 确保所有测试通过
   - Ensure all tests pass

---

## 🔗 相关文件 / Related Files

- `whosellm/models/base.py` - 模型家族枚举定义
- `whosellm/models/config.py` - ModelFamilyConfig 配置类
- `whosellm/models/registry.py` - 统一注册表和查询接口
- `whosellm/models/families/` - 各提供商的家族配置
- `whosellm/provider.py` - 提供商定义
- `whosellm/capabilities.py` - 能力字段定义
- `tests/test_auto_register.py` - 自动注册测试

---

## ❓ 常见问题 / FAQ

### Q: 如何处理同一家族的多个版本？

A: 在模式中使用 `{version:d}` 捕获版本号，例如：
```python
patterns=[
    "model-{version:d}-{variant:variant}",  # model-1-pro, model-2-pro
]
```

### Q: 如何支持特殊的命名格式？

A: 添加更具体的模式，并放在列表前面：
```python
patterns=[
    "special-format-{variant:variant}",     # 特殊格式优先
    "model-{variant:variant}",              # 通用格式
]
```

### Q: 新家族的自动注册不工作怎么办？

A: 检查以下几点：
1. `ModelFamily` 枚举值是否与配置中的 `family` 字段匹配
2. 模式是否能正确匹配模型名称（可以用 `registry.match_model_pattern()` 测试）
3. 配置文件是否在 `families/__init__.py` 中导入
4. `ModelFamilyConfig` 的 `__post_init__` 是否被调用（检查导入顺序）

---

**完成！** 现在你可以使用新添加的模型家族了！🎉

**Done!** You can now use the newly added model family! 🎉
