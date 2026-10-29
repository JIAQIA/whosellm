# filename: test_tool_result_surfaces.py
"""
工具结果能力与文档限制测试 / Tool-result capability and document-limit tests

覆盖 W2–W5 新增字段：
- LLMApiSurface 词表与 ToolResultSurfaceCapability
- ModelCapabilities.tool_result_surfaces / max_inline_media_bytes
- max_pdf_size_mb / max_pdf_pages / supported_document_mime_type
- FileApiCapability（预留）

数据来源与抓取日期见 whosellm/models/families 下各配置文件的注释。
Data sources and fetch dates are documented in the family config modules.
"""

import json
from dataclasses import FrozenInstanceError

import pytest

from whosellm import (
    FileApiCapability,
    LLMApiSurface,
    LLMeta,
    ModelCapabilities,
    ToolResultSurfaceCapability,
)

REQUIRED_SURFACES = {
    "claude_messages",
    "openai_chat_completions",
    "openai_responses",
    "gemini",
    "dashscope",
    "glm",
    "deepseek",
    "deepseek_responses",
}


class TestLLMApiSurface:
    """API surface 词表 / API surface vocabulary"""

    def test_required_members_exist(self) -> None:
        assert {surface.value for surface in LLMApiSurface} == REQUIRED_SURFACES

    def test_str_enum_serializes_as_plain_string(self) -> None:
        """str 枚举可直接作为 dict 键并 JSON 序列化 / str enum works as a dict key and serializes"""
        assert LLMApiSurface.CLAUDE_MESSAGES == "claude_messages"
        assert json.dumps({LLMApiSurface.CLAUDE_MESSAGES: "ok"}) == '{"claude_messages": "ok"}'

    def test_value_lookup(self) -> None:
        """可用字符串值还原枚举成员 / Members can be reconstructed from their string values"""
        assert LLMApiSurface("claude_messages") is LLMApiSurface.CLAUDE_MESSAGES
        assert str(LLMApiSurface.GEMINI) == "gemini"


class TestDefaults:
    """新增字段的空默认值 / Empty defaults for the new fields"""

    def test_tool_result_surface_defaults(self) -> None:
        surface = ToolResultSurfaceCapability()
        assert surface.modalities == ()
        assert surface.max_inline_bytes is None
        assert surface.mime_types is None
        assert surface.supports("image") is False

    def test_model_capabilities_defaults(self) -> None:
        caps = ModelCapabilities()
        assert caps.tool_result_surfaces == {}
        assert caps.max_inline_media_bytes is None
        assert caps.max_inline_file_bytes is None
        assert caps.max_pdf_size_mb is None
        assert caps.max_pdf_pages is None
        assert caps.max_document_size_mb is None
        assert caps.supported_document_mime_type == []
        assert caps.file_api is None

    def test_file_api_defaults(self) -> None:
        file_api = FileApiCapability()
        assert file_api.supports_upload is False
        assert file_api.max_file_size_mb is None
        assert file_api.supported_mime_types == []

    def test_surface_is_frozen(self) -> None:
        surface = ToolResultSurfaceCapability(modalities=("image",))
        with pytest.raises(FrozenInstanceError):
            surface.modalities = ("audio",)  # type: ignore[misc]


class TestClaudeToolResults:
    """Claude Messages：工具结果原生支持 image + document / Claude Messages tool results"""

    @pytest.mark.parametrize(
        ("model_name", "expected_pages"),
        [
            ("claude-opus-5-5", 600),
            ("claude-fable-5", 600),
            ("claude-sonnet-5", 600),
            ("claude-opus-4-8", 600),
            ("claude-sonnet-4-6", 600),
            ("claude-sonnet-4-5", 100),
            ("claude-haiku-4-5", 100),
            ("claude-opus-4-1", 100),
        ],
    )
    def test_claude_4x_5x(self, model_name: str, expected_pages: int) -> None:
        caps = LLMeta(model_name).capabilities
        surface = caps.tool_result_surfaces[LLMApiSurface.CLAUDE_MESSAGES]

        assert surface.modalities == ("image", "document")
        assert surface.supports("image") is True
        assert surface.supports("document") is True
        assert surface.supports("audio") is False
        assert surface.supports("video") is False
        assert surface.mime_types is not None
        assert surface.mime_types["document"] == ["application/pdf"]
        assert surface.mime_types["image"] == ["image/jpeg", "image/png", "image/gif", "image/webp"]

        # W3 文档上限 / W3 document limits
        # 官方只公布请求级 128 MB，没有单文件上限 → max_pdf_size_mb 保持 None
        # Only a request-level 128 MB cap is documented, so the per-file size stays None
        assert caps.supports_pdf is True
        assert caps.max_pdf_size_mb is None
        assert caps.max_pdf_pages == expected_pages
        assert caps.supported_document_mime_type == ["application/pdf"]
        assert caps.max_inline_media_bytes == 128_000_000
        assert caps.max_inline_file_bytes is None  # 官方无文件合计上限 / no combined file cap

    def test_claude_3x_is_undeclared(self) -> None:
        """Claude 3.x 未登记工具结果 surface 数据 / Claude 3.x leaves surfaces undeclared"""
        caps = LLMeta("claude-3-7-sonnet").capabilities
        assert LLMApiSurface.CLAUDE_MESSAGES not in caps.tool_result_surfaces
        assert caps.max_pdf_size_mb is None
        assert caps.max_pdf_pages is None


class TestOpenAIToolResults:
    """OpenAI：Chat Completions text-only；Responses 支持 image / document"""

    @pytest.mark.parametrize("model_name", ["gpt-4o", "gpt-5.4-mini", "gpt-6-astra", "o3"])
    def test_chat_completions_unsupported_responses_supported(self, model_name: str) -> None:
        caps = LLMeta(model_name).capabilities
        chat = caps.tool_result_surfaces[LLMApiSurface.OPENAI_CHAT_COMPLETIONS]
        responses = caps.tool_result_surfaces[LLMApiSurface.OPENAI_RESPONSES]

        assert chat.modalities == ()
        assert chat.supports("image") is False
        assert responses.modalities == ("image", "document")
        assert responses.supports("image") is True
        assert responses.supports("document") is True
        assert responses.mime_types is not None
        assert responses.mime_types["document"] == ["application/pdf"]

        assert caps.supports_pdf is True
        assert caps.max_pdf_size_mb == 50.0
        assert caps.max_pdf_pages is None  # 官方未公布页数上限 / no documented page cap
        assert caps.supported_document_mime_type == ["application/pdf"]
        assert caps.max_inline_media_bytes == 512_000_000
        assert caps.max_inline_file_bytes == 50_000_000  # 所有文件合计 <50 MB / combined files

    @pytest.mark.parametrize("model_name", ["o3-mini", "gpt-4o-audio-preview"])
    def test_non_vision_chat_only(self, model_name: str) -> None:
        caps = LLMeta(model_name).capabilities
        assert caps.tool_result_surfaces[LLMApiSurface.OPENAI_CHAT_COMPLETIONS].modalities == ()
        assert LLMApiSurface.OPENAI_RESPONSES not in caps.tool_result_surfaces

    def test_gpt_3_5_chat_only(self) -> None:
        caps = LLMeta("gpt-3.5-turbo").capabilities
        assert caps.tool_result_surfaces[LLMApiSurface.OPENAI_CHAT_COMPLETIONS].modalities == ()
        assert caps.max_pdf_size_mb is None


class TestGeminiToolResults:
    """Gemini：仅 3 系支持多模态 function response；2.x 必须显式标不支持"""

    @pytest.mark.parametrize(
        "model_name",
        ["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-3-flash-preview", "gemini-3-pro"],
    )
    def test_gemini_3_supports_multimodal(self, model_name: str) -> None:
        caps = LLMeta(model_name).capabilities
        surface = caps.tool_result_surfaces[LLMApiSurface.GEMINI]
        # 2026-10-29 实测 gemini-3-flash-preview：image/pdf/audio/video 均被读取
        # Probe on gemini-3-flash-preview: image/pdf/audio/video are all consumed
        assert surface.modalities == ("image", "document", "audio", "video")
        for modality in ("image", "document", "audio", "video"):
            assert surface.supports(modality) is True  # type: ignore[arg-type]
        assert surface.mime_types is not None
        assert surface.mime_types["document"] == ["application/pdf"]
        assert surface.mime_types["audio"] == ["audio/wav"]
        assert surface.mime_types["video"] == ["video/mp4"]

        # 官方未公布单文件 PDF 上限（inline payload 100 MB / PDF 50 MB 均为请求级）
        # No per-file PDF cap is documented; the inline payload caps are request-level
        assert caps.max_pdf_size_mb is None
        assert caps.max_pdf_pages == 1000
        assert caps.supported_document_mime_type == ["application/pdf"]
        assert caps.max_inline_media_bytes == 100_000_000
        assert caps.max_inline_file_bytes == 50_000_000

    @pytest.mark.parametrize(
        "model_name",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash"],
    )
    def test_gemini_2x_explicitly_unsupported(self, model_name: str) -> None:
        """2.x 明确标为不支持（空元组），而非缺键 / 2.x is explicitly unsupported, not undeclared"""
        caps = LLMeta(model_name).capabilities
        surface = caps.tool_result_surfaces[LLMApiSurface.GEMINI]
        assert surface.modalities == ()
        assert surface.supports("image") is False
        # 用户消息仍可看图；工具结果不支持是独立维度 / User-message vision is unaffected
        assert caps.supports_vision is True

    @pytest.mark.parametrize("model_name", ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"])
    def test_gemini_2_5_pdf_limits(self, model_name: str) -> None:
        """用户消息的 PDF 能力不受工具结果限制影响 / User-message PDF capability is unaffected"""
        caps = LLMeta(model_name).capabilities
        assert caps.supports_pdf is True
        assert caps.max_pdf_pages == 1000
        assert caps.max_pdf_size_mb is None
        assert caps.max_inline_file_bytes == 50_000_000

    def test_image_only_model_has_no_surface(self) -> None:
        """无 function calling 的模型不登记 surface / Models without function calling declare no surface"""
        caps = LLMeta("gemini-2.5-flash-image").capabilities
        assert LLMApiSurface.GEMINI not in caps.tool_result_surfaces


class TestDeepSeekToolResults:
    """DeepSeek：Chat Completions text-only；Responses 图片可用、PDF 静默丢失"""

    @pytest.mark.parametrize(
        "model_name",
        ["deepseek-flash", "deepseek-v4-pro", "deepseek-chat", "deepseek-reasoner"],
    )
    def test_chat_completions_text_only(self, model_name: str) -> None:
        caps = LLMeta(model_name).capabilities
        surface = caps.tool_result_surfaces[LLMApiSurface.DEEPSEEK]
        assert surface.modalities == ()
        assert surface.supports("image") is False

        # 实测 2026-10-29：PDF input_file 被接受但内容不投递 / PDF is silently dropped
        assert caps.supports_pdf is False
        assert caps.supported_document_mime_type == []
        assert caps.max_pdf_size_mb is None
        assert caps.max_pdf_pages is None
        assert caps.max_inline_file_bytes is None

    @pytest.mark.parametrize(
        "model_name",
        ["deepseek-flash", "deepseek-chat", "deepseek-reasoner"],
    )
    def test_responses_supports_image_not_document(self, model_name: str) -> None:
        caps = LLMeta(model_name).capabilities
        surface = caps.tool_result_surfaces[LLMApiSurface.DEEPSEEK_RESPONSES]
        assert surface.modalities == ("image",)
        assert surface.supports("image") is True
        assert surface.supports("document") is False
        assert surface.max_inline_bytes == 32 * 1024 * 1024
        assert surface.mime_types is not None
        assert surface.mime_types["image"] == ["image/jpeg", "image/png", "image/gif", "image/webp"]
        assert caps.max_inline_media_bytes == 48 * 1024 * 1024

    def test_responses_text_only_model(self) -> None:
        caps = LLMeta("deepseek-v4-pro").capabilities
        surface = caps.tool_result_surfaces[LLMApiSurface.DEEPSEEK_RESPONSES]
        assert surface.modalities == ()
        assert caps.max_inline_media_bytes is None


class TestExplicitlyUnsupportedSurfaces:
    """官方明确不支持：显式空元组 / Officially unsupported: explicit empty tuple"""

    @pytest.mark.parametrize(
        ("model_name", "surface"),
        [
            ("qwen3-vl-plus", LLMApiSurface.DASHSCOPE),
            ("qwen-plus", LLMApiSurface.DASHSCOPE),
            ("glm-4.6v", LLMApiSurface.GLM),
            ("glm-5v-turbo", LLMApiSurface.GLM),
        ],
    )
    def test_dashscope_and_glm_text_only(self, model_name: str, surface: LLMApiSurface) -> None:
        """官方 API 参考将 tool 消息 content 定义为字符串 / Official API defines tool content as string"""
        caps = LLMeta(model_name).capabilities
        assert caps.tool_result_surfaces[surface].modalities == ()
        assert caps.tool_result_surfaces[surface].supports("image") is False
