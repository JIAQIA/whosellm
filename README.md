# LLMVer

一个统一的大语言模型版本和能力管理库 / A unified LLM model version and capability management library

## 背景 / Background

当前大模型的厂商（provider）/版本(3.5/4.0/4)/型号(flash/mini/o)混乱不堪，不同厂商、不同版本、不同型号其能力又不尽相同。

比如以智谱AI的GLM-4V来讲，它支持视觉多模态，但其接口中传入的视频有如下要求：
- GLM-4V-Plus视频大小限制为20M以内，视频时长不超过 30s
- GLM-4V-Plus-0111视频大小限制为 200M 以内
- 图片url或者base64编码
- 图像大小上传限制为每张图像 5M以下，且像素不超过 6000*6000
- 支持jpg、png、jpeg格式
- GLM-4V-Flash 不支持base64编码

这些要求非常细碎，开发者将非常难以处理这些"变态"的要求。一个不小心就会触发警告，同时如果开发者有适配多个模型的需求，这些不同厂商API之间的要求将是恶梦。

## 特性 / Features

1. **简单初始化** - 仅需要一个字符串即可完成模型配置的初始化
2. **版本比较** - 自动匹配到厂商/版本/型号，支持同一厂商下不同版本/型号的大小比较和运算符比较
3. **能力范围说明** - 提供模型能力范围说明：
   - 是否支持 thinking（reasoning）模式
   - 是否支持图片
   - 是否支持音频
   - 是否支持视频
   - 是否支持 PDF
4. **参数验证** - 针对具体模型，提供请求参数验证的可选实现，基于 VRL 脚本语言自动整改参数

## 安装 / Installation

```bash
# 使用 uv
uv add llmver

# 使用 pip
pip install llmver
```

## 快速开始 / Quick Start

```python
from llmver import ModelVersion

# 初始化模型版本
model = ModelVersion("glm-4v-plus")

# 检查能力
print(model.capabilities.supports_vision)  # True
print(model.capabilities.supports_video)   # True

# 版本比较
model1 = ModelVersion("gpt-4")
model2 = ModelVersion("gpt-3.5-turbo")
print(model1 > model2)  # True

# 参数验证（可选）
validated_params = model.validate_params(your_params)
```

## 开发 / Development

本项目使用以下工具：
- **uv** - 依赖管理
- **ruff** - 代码格式化和检查
- **mypy** - 类型检查
- **bump-my-version** - 版本管理

### 安装开发依赖 / Install Development Dependencies

```bash
# 使用 uv 直接安装
uv sync --extra dev --extra test

# 或使用 poe 命令
poe dev
```

### 常用开发命令 / Common Development Commands

#### 代码格式化 / Code Formatting
```bash
poe fmt          # 格式化代码 / Format code
poe format       # 同上 / Same as above
```

#### 代码检查 / Code Linting
```bash
poe lint         # 检查并自动修复 / Check and auto-fix
poe check        # 仅检查不修复 / Check only without fixing
```

#### 类型检查 / Type Checking
```bash
poe typecheck    # 运行 mypy 类型检查 / Run mypy type checking
poe mypy         # 同上 / Same as above
```

#### 测试 / Testing
```bash
poe test              # 运行单元测试和集成测试 / Run unit and integration tests
poe test-unit         # 仅运行单元测试 / Run unit tests only
poe test-integration  # 仅运行集成测试 / Run integration tests only
poe test-cov          # 运行测试并生成覆盖率报告 / Run tests with coverage report
poe test-e2e          # 运行端到端测试 / Run end-to-end tests
poe test-all          # 运行所有测试 / Run all tests
```

#### 代码质量全套检查 / Full Quality Assurance
```bash
poe qa           # 运行格式化、检查、类型检查和测试 / Run format, lint, typecheck and test
```

#### 其他命令 / Other Commands
```bash
poe example      # 运行示例代码 / Run example code
poe clean        # 清理所有缓存和构建文件 / Clean all cache and build files
```

### 版本管理 / Version Management

```bash
# 升级补丁版本
bump-my-version bump patch

# 升级次版本
bump-my-version bump minor

# 升级主版本
bump-my-version bump major
```

## 许可证 / License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者 / Author

JQQ <jqq1716@gmail.com>
