# filename: test_deepseek.py
# @Time    : 2025/11/9 16:08
# @Author  : Cascade AI
"""
DeepSeek 模型家族测试 / DeepSeek model family tests
"""

from whosellm.models.base import ModelFamily
from whosellm.models.registry import get_specific_model_config
from whosellm.provider import Provider


def test_deepseek_default_capabilities() -> None:
    """验证 DeepSeek 官方家族默认能力（V4 基线） / Validate DeepSeek official family default capabilities (V4 baseline)"""
    from whosellm import LLMeta

    # 使用官方 Provider 前缀确保获取官方配置
    model = LLMeta("deepseek::deepseek-chat")
    capabilities = model.capabilities

    assert capabilities.supports_streaming is True
    assert capabilities.supports_function_calling is True
    # V4 系列：1M 上下文，384K 最大输出
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000
    # deepseek-chat 是 v4-flash 非思考模式的别名
    assert capabilities.supports_thinking is False


def test_deepseek_chat_specific_model() -> None:
    """验证 deepseek-chat 特定模型配置 / Validate deepseek-chat specific configuration"""
    config = get_specific_model_config("deepseek-chat")

    assert config is not None
    version, variant, capabilities = config
    assert version == "4.0"
    assert variant == "chat"
    assert capabilities is not None
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_streaming is True
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000


def test_deepseek_chat_pattern_matching() -> None:
    """验证 deepseek-chat 模式匹配 / Validate deepseek-chat pattern matching"""
    from whosellm import LLMeta

    for name in ["deepseek-chat", "deepseek-chat-beta", "deepseek-chat-v3.2-exp"]:
        # 使用 Provider 前缀确保匹配官方配置
        model = LLMeta(f"deepseek::{name}")

        assert model.family == ModelFamily.DEEPSEEK
        assert model.variant == "chat"
        assert model.version == "4.0"
        assert model.provider == Provider.DEEPSEEK


def test_deepseek_reasoner_specific_model() -> None:
    """验证 deepseek-reasoner 特定模型配置 / Validate deepseek-reasoner specific configuration"""
    config = get_specific_model_config("deepseek-reasoner")

    assert config is not None
    version, variant, capabilities = config
    assert version == "4.0"
    assert variant == "reasoner"
    assert capabilities is not None
    assert capabilities.supports_thinking is True
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000


def test_deepseek_base_pattern_without_variant() -> None:
    """验证无型号名称时的默认匹配 / Validate default match without explicit variant"""
    from whosellm import LLMeta

    # 使用 Provider 前缀确保匹配官方配置
    model = LLMeta("deepseek::deepseek-chat")

    assert model.family == ModelFamily.DEEPSEEK
    assert model.variant == "chat"
    assert model.version == "4.0"
    assert model.capabilities.supports_function_calling is True


def test_deepseek_reasoner_does_not_use_chat_capabilities() -> None:
    """验证 reasoner 不会意外继承 chat 的能力 / Ensure reasoner capabilities override family defaults"""
    from whosellm import LLMeta

    model = LLMeta("deepseek::deepseek-reasoner")

    assert model.variant == "reasoner"
    assert model.capabilities.supports_function_calling is True
    assert model.capabilities.supports_thinking is True


def test_deepseek_no_structured_outputs() -> None:
    """验证 DeepSeek 官方模型不支持 structured_outputs（仅支持 json_object）"""
    from whosellm import LLMeta

    for model_id in ["deepseek-chat", "deepseek-reasoner", "deepseek-v4-flash", "deepseek-v4-pro"]:
        model = LLMeta(f"deepseek::{model_id}")
        assert model.capabilities.supports_structured_outputs is False, (
            f"{model_id}: DeepSeek API 仅支持 response_format={{type:'json_object'}}，"
            "不支持 json_schema 类型，supports_structured_outputs 应为 False"
        )
        assert model.capabilities.supports_json_outputs is True, (
            f"{model_id}: DeepSeek API 支持 response_format={{type:'json_object'}}，supports_json_outputs 应为 True"
        )


def test_deepseek_v4_flash_specific_model() -> None:
    """验证 deepseek-v4-flash 特定模型配置 / Validate deepseek-v4-flash specific configuration"""
    from whosellm import LLMeta

    model = LLMeta("deepseek::deepseek-v4-flash")

    assert model.family == ModelFamily.DEEPSEEK
    assert model.provider == Provider.DEEPSEEK
    assert model.version == "4.0"
    assert model.variant == "flash"

    caps = model.capabilities
    assert caps.supports_thinking is True
    assert caps.supports_function_calling is True
    assert caps.supports_streaming is True
    assert caps.supports_json_outputs is True
    assert caps.supports_structured_outputs is False
    assert caps.max_tokens == 384_000
    assert caps.context_window == 1_000_000


def test_deepseek_v4_pro_specific_model() -> None:
    """验证 deepseek-v4-pro 特定模型配置 / Validate deepseek-v4-pro specific configuration"""
    from whosellm import LLMeta

    model = LLMeta("deepseek::deepseek-v4-pro")

    assert model.family == ModelFamily.DEEPSEEK
    assert model.provider == Provider.DEEPSEEK
    assert model.version == "4.0"
    assert model.variant == "pro"

    caps = model.capabilities
    assert caps.supports_thinking is True
    assert caps.supports_function_calling is True
    assert caps.max_tokens == 384_000
    assert caps.context_window == 1_000_000


def test_deepseek_v4_variant_ordering() -> None:
    """验证 v4-flash < v4-pro 的排序关系 / Validate v4-flash < v4-pro ordering"""
    from whosellm import LLMeta

    flash = LLMeta("deepseek::deepseek-v4-flash")
    pro = LLMeta("deepseek::deepseek-v4-pro")

    assert flash < pro


def test_deepseek_versioned_pattern_matches_official_family() -> None:
    """验证带版本号的 DS 模型名能被官方 family 识别 / Validate versioned DS names match the official family"""
    from whosellm import LLMeta

    # V4 是 DS 官方首次开放版本号命名的系列
    model = LLMeta("deepseek::deepseek-v4-flash")
    assert model.family == ModelFamily.DEEPSEEK
    assert model.provider == Provider.DEEPSEEK
    assert model.version == "4.0"

    # 带小数版本号也能匹配 family（即使当前没有 specific_model 条目）
    model_v32 = LLMeta("deepseek::deepseek-v3.2-exp")
    assert model_v32.family == ModelFamily.DEEPSEEK
    assert model_v32.provider == Provider.DEEPSEEK
    assert model_v32.version == "3.2"
    assert model_v32.variant == "exp"


def test_deepseek_v4_flash_vision_exp_specific_model() -> None:
    """验证 deepseek-v4-flash-vision-exp 配置（多模态实验版）"""
    config = get_specific_model_config("deepseek-v4-flash-vision-exp")
    assert config is not None
    version, variant, capabilities = config
    assert version == "4.0"
    assert variant == "flash-vision-exp"
    assert capabilities is not None
    # 图像输入 / image input
    assert capabilities.supports_vision is True
    # 双模式，默认思考 / dual mode, thinking by default
    assert capabilities.supports_thinking is True
    assert capabilities.supports_function_calling is True
    assert capabilities.supports_streaming is True
    assert capabilities.supports_json_outputs is True
    assert capabilities.supports_structured_outputs is False
    # 不支持视频输入 / no video input
    assert capabilities.supports_video is False
    assert capabilities.max_tokens == 384_000
    assert capabilities.context_window == 1_000_000


def test_deepseek_v4_flash_vision_exp_llmeta() -> None:
    """验证 deepseek-v4-flash-vision-exp LLMeta 解析"""
    from whosellm import LLMeta

    model = LLMeta("deepseek-v4-flash-vision-exp")
    assert model.provider == Provider.DEEPSEEK
    assert model.family == ModelFamily.DEEPSEEK
    assert model.version == "4.0"
    assert model.variant == "flash-vision-exp"
    assert model.capabilities.context_window == 1_000_000
    assert model.capabilities.supports_vision is True


class TestDeepSeekRouting:
    """DeepSeek 旧模型名的路由实况 / Routing reality of DeepSeek legacy names.

    官方原文（2026-09-10 changelog）："旧版本模型 V4 Flash 与 V4 Flash Vision Exp 现已下线，
    出于兼容考虑，模型名 deepseek-v4-flash、deepseek-v4-flash-vision-exp 将被暂时路由到 V4.1 Flash。"
    Official: legacy V4 Flash / V4 Flash Vision Exp are offline; their model names are
    *temporarily* routed to V4.1 Flash.

    实探证据（2026-09-28，api.deepseek.com，见 /tmp/probe_deepseek.py）：
      - GET /models 仅返回 deepseek-flash 与 deepseek-v4-pro
      - deepseek-v4-flash / deepseek-v4-flash-vision-exp / deepseek-chat / deepseek-reasoner
        的响应 model 字段均回显 deepseek-flash，且能正确读出白底红方块
      - deepseek-v4-pro 回显自身，带图不报错但静默忽略并编造答案

    ⚠️ 路由是"暂时"的：官方撤销后本类测试会失败，届时需重新探针并回改配置
    （能力轴跟端点现状，版本轴跟名字血统）。/ The routing is temporary: when the vendor
    removes it these tests fail on purpose, prompting a re-probe and a config rollback.
    """

    def test_deepseek_flash_canonical_name(self) -> None:
        """deepseek-flash 为官方正式名（无版本号），对应 DeepSeek-V4.1-Flash"""
        from whosellm import LLMeta

        model = LLMeta("deepseek-flash")
        assert model.provider == Provider.DEEPSEEK
        assert model.family == ModelFamily.DEEPSEEK
        # 名字无版本号 → 按官方模型版本标注 4.1
        assert model.version == "4.1"
        assert model.variant == "flash"

        caps = model.capabilities
        assert caps.supports_vision is True
        assert caps.supports_thinking is True  # 默认开启 / on by default
        assert caps.media_count_limit.get("image") == 600
        assert caps.context_window == 1_000_000
        assert caps.max_tokens == 384_000

    def test_v4_flash_routed_to_v41_flash(self) -> None:
        """deepseek-v4-flash 已被路由到 V4.1 Flash，视觉能力随之可用"""
        from whosellm import LLMeta

        model = LLMeta("deepseek-v4-flash")
        # 版本轴仍按名字解析为 4.0 / version still parses from the name (4.0)
        assert model.version == "4.0"
        assert model.variant == "flash"
        # 能力轴跟随实际服务模型 / capabilities follow the serving model
        assert model.capabilities.supports_vision is True
        assert model.capabilities.media_count_limit.get("image") == 600

    def test_vision_exp_routed_to_v41_flash(self) -> None:
        """deepseek-v4-flash-vision-exp 同样被路由到 V4.1 Flash"""
        from whosellm import LLMeta

        model = LLMeta("deepseek-v4-flash-vision-exp")
        assert model.version == "4.0"
        assert model.capabilities.supports_vision is True
        assert model.capabilities.media_count_limit.get("image") == 600

    def test_chat_and_reasoner_routed_have_vision(self) -> None:
        """deepseek-chat / deepseek-reasoner 路由到 flash，同样可读图

        两者保留各自的默认思考模式语义（chat 非思考、reasoner 思考），
        但视觉能力跟随实际服务模型。
        """
        from whosellm import LLMeta

        chat = LLMeta("deepseek-chat")
        assert chat.capabilities.supports_thinking is False  # 默认非思考 / non-thinking by default
        assert chat.capabilities.supports_vision is True
        assert chat.capabilities.media_count_limit.get("image") == 600

        reasoner = LLMeta("deepseek-reasoner")
        assert reasoner.capabilities.supports_thinking is True
        assert reasoner.capabilities.supports_vision is True
        assert reasoner.capabilities.media_count_limit.get("image") == 600

    def test_v4_pro_not_routed_stays_text_only(self) -> None:
        """deepseek-v4-pro 未被路由，保持纯文本（带图会静默幻觉，绝不能标 True）

        实探：带图请求返回 200，图片被静默忽略，答案系编造；无图对照亦编造；
        直接追问时模型承认"看不到图片 / [Unsupported Image]"。
        来源：https://api-docs.deepseek.com/zh-cn/quick_start/pricing（图像理解 不支持）
        """
        from whosellm import LLMeta

        model = LLMeta("deepseek-v4-pro")
        assert model.version == "4.0"
        assert model.variant == "pro"
        assert model.capabilities.supports_vision is False
        assert model.capabilities.media_count_limit.get("image") == 0  # 键缺失视同不支持

    def test_version_axis_orders_flash_above_pro(self) -> None:
        """版本优先于档位：V4.1 Flash > V4 Pro（与官方"全面超越 V4 Pro"表述一致）"""
        from whosellm import LLMeta

        assert LLMeta("deepseek-flash") > LLMeta("deepseek-v4-pro")
        assert LLMeta("deepseek-v4-pro") > LLMeta("deepseek-v4-flash")
