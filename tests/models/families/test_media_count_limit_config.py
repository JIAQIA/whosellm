# filename: test_media_count_limit_config.py
"""
各家族媒体数量限制的集成断言（官方文档来源见配置注释）
Per-family media count limit integration tests (official docs cited in config comments)
"""

import math

from whosellm import UNLIMITED
from whosellm.model_version import LLMeta

OFFICIAL = (
    # (模型名, 官方图片数量上限/请求, 计数模式)
    # 来源 / Sources:
    # Anthropic: platform.claude.com/docs/en/build-with-claude/vision (600/1M ctx, 100/200k ctx)
    # OpenAI:    developers.openai.com/api/docs/guides/images-vision (1,500)
    # Gemini:    ai.google.dev/gemini-api/docs/image-understanding (3,600)
    # Zhipu:     docs.bigmodel.cn（GLM-5.3-Flash 未公开上限）/ zai-org/GLM-skills（GLM-4.6v ≤50）
    # DeepSeek:  api-docs.deepseek.com/guides/vision (600)
    # Alibaba:   help.aliyun.com/zh/model-studio/vision (256 URL / 250 base64)
    ("claude-fable-5-1", 600, "per_type"),
    ("claude-mythos-5-1", 600, "per_type"),
    ("claude-opus-5", 600, "per_type"),
    ("claude-sonnet-5", 600, "per_type"),
    ("claude-opus-4-8", 600, "per_type"),
    ("claude-sonnet-4-6", 600, "per_type"),
    ("gpt-5.6", 1500, "per_type"),
    ("gpt-5.5", 1500, "per_type"),
    ("gemini-3.8-flash", 3600, "per_type"),
    ("gemini-3.7-flash", 3600, "per_type"),
    ("glm-4.6v", 50, "combined"),
    ("glm-4.6v-flash", 50, "combined"),
    ("deepseek-v4-flash-vision-exp", 600, "per_type"),
    ("qwen3-vl-plus", 256, "per_type"),
    ("qwen3-vl-flash", 256, "per_type"),
)


class TestLatestModels:
    """最新/次新模型的官方图片数量上限 / Official image count caps for latest models"""

    def test_official_image_caps(self):
        for model_name, expected, mode in OFFICIAL:
            mcl = LLMeta(model_name).capabilities.media_count_limit
            assert mcl.get("image") == expected, f"{model_name}: {mcl.get('image')} != {expected}"
            assert mcl.count_mode == mode, f"{model_name}: count_mode mismatch"
            assert mcl.is_supported("image") is True

    def test_glm_combined_shared_pool(self):
        """GLM 系列为合并计数：图片/视频等素材共享 50 的总池"""
        for model_name in ("glm-4.6v", "glm-4.6v-flash"):
            mcl = LLMeta(model_name).capabilities.media_count_limit
            assert mcl.count_mode == "combined"
            assert mcl.combined == 50

    def test_glm_5v_turbo_no_documented_cap(self):
        """GLM-5.3-Flash（glm-5v-turbo）官方未公开数量上限 → UNLIMITED"""
        mcl = LLMeta("glm-5v-turbo").capabilities.media_count_limit
        assert mcl.get("image") is math.inf
        assert mcl.get("image") is UNLIMITED


class TestUnmeasuredModels:
    """未实测模型：键缺失视同不支持 / Unmeasured models: missing keys treated as unsupported"""

    def test_200k_claude_without_specific_cap(self):
        """老代模型未采集 → image 为 0（视同不支持），不误报为无上限"""
        mcl = LLMeta("claude-3-5-haiku").capabilities.media_count_limit
        assert mcl.get("image") == 0
        assert bool(mcl.get("image")) is False

    def test_text_only_model(self):
        mcl = LLMeta("deepseek-v4-flash").capabilities.media_count_limit
        assert mcl.get("image") == 0
