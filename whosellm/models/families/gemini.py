# filename: gemini.py
# @Time    : 2025/12/12 13:17
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: PyCharm
"""
Google Gemini 模型家族配置 / Google Gemini model family configurations
"""

from whosellm.capabilities import ModelCapabilities
from whosellm.models.base import ModelFamily
from whosellm.models.config import ModelFamilyConfig, SpecificModelConfig
from whosellm.provider import Provider

# ==========================================================================
# Gemini 系列 / Gemini Series
# 注意Image系列模型。当前虽然标记为不支持thinking，在实际调试中发现 image 系列也会有思考内容产生，但需要注意接口并不支持配置thinking行为，
# 因此权当不支持处理
# ==========================================================================

GEMINI = ModelFamilyConfig(
    family=ModelFamily.GEMINI,
    provider=Provider.GOOGLE,
    version_default="3.0",
    variant_default="flash",
    variant_priority_default=(1,),  # flash 的默认优先级 / default priority for flash
    patterns=[
        "gemini-{major:d}.{minor:d}-{variant}",
        "gemini-{major:d}.{minor:d}-{variant}-{suffix}",
        "gemini-{major:d}.{minor:d}-{variant}-preview-{date}",
        "gemini-{major:d}.{minor:d}-{variant}-preview",
        "gemini-{major:d}.{minor:d}-{variant}-image",
        "gemini-{major:d}.{minor:d}-{variant}-lite",
        "gemini-{major:d}.{minor:d}-{variant}-live",
        "gemini-{major:d}.{minor:d}-{variant}-native-audio-preview-{date}",
        "gemini-{major:d}.{minor:d}-preview-tts",
        "gemini-{major:d}.{minor:d}-preview-{date}",
        "gemini-{major:d}.{minor:d}-preview",
        "gemini-{major:d}.{minor:d}",
        "gemini-{variant}",
        "gemini-{variant}-preview",
        "gemini-{variant}-latest",
    ],
    capabilities=ModelCapabilities(
        supports_vision=True,
        supports_audio=True,
        supports_video=True,
        supports_pdf=True,
        supports_thinking=True,
        supports_function_calling=True,
        supports_streaming=True,
        supports_structured_outputs=True,
        supports_json_outputs=True,
        supports_web_search=True,
        supports_file_search=True,
        supports_code_interpreter=True,
        max_tokens=65536,
        context_window=1048576,
    ),
    specific_models={
        # Gemini 3 Pro 系列 - 最智能的多模态模型
        # ⚠️ gemini-3-pro / gemini-3-pro-preview 已于 2026-03-09 关停，请迁移至 gemini-3.1-pro-preview
        "gemini-3-pro": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3-pro"],
        ),
        "gemini-3-pro-preview": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro",
            variant_priority=(5,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3-pro-preview"],
        ),
        # ⚠️ gemini-3-pro-image-preview 已于 2026-06-25 关停，请迁移至 gemini-3-pro-image
        "gemini-3-pro-image-preview": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro-image",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                max_tokens=32768,
                context_window=65536,
            ),
            patterns=["gemini-3-pro-image-preview"],
        ),
        # Nano Banana Pro GA 版：2026-05-28 发布，替代已关停的 gemini-3-pro-image-preview
        # 官方规格：输入 Image/Text，输出 Image/Text；ctx 65536 / max 32768；
        # image_generation ✓、search grounding ✓、structured ✗、function calling ✗
        "gemini-3-pro-image": SpecificModelConfig(
            version_default="3.0",
            variant_default="pro-image",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                supports_web_search=True,
                max_tokens=32768,
                context_window=65536,
            ),
            patterns=["gemini-3-pro-image"],
        ),
        # Gemini 2.5 Flash 系列 - 性价比最高的模型
        "gemini-2.5-flash": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash"],
        ),
        # ⚠️ gemini-2.5-flash-preview-09-2025 已于 2026-02-17 关停，官方建议迁移至 gemini-3.6-flash
        "gemini-2.5-flash-preview-09-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash-preview-09-2025"],
        ),
        # ⚠️ gemini-2.5-flash-image（Nano Banana）计划于 2026-10-02 关停，建议迁移至 gemini-3.1-flash-image（Nano Banana 2）
        "gemini-2.5-flash-image": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-image",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_pdf=False,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                max_tokens=32768,
                context_window=65536,
            ),
            patterns=["gemini-2.5-flash-image"],
        ),
        # ⚠️ gemini-2.5-flash-native-audio-preview-09-2025 已被 12-2025 版取代，
        # 官方当前 Live 旗舰为 gemini-2.5-flash-native-audio-preview-12-2025
        "gemini-2.5-flash-native-audio-preview-09-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-live",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_audio=True,
                supports_video=True,
                supports_pdf=False,
                supports_audio_generation=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_web_search=True,
                max_tokens=8192,
                context_window=131072,
            ),
            patterns=["gemini-2.5-flash-native-audio-preview-09-2025"],
        ),
        # 当前 Live API 旗舰（2.5 Flash Live 12-2025 版，官方规格卡 2026-08 采集）：
        # 输入 Audio/Video/Text，输出 Audio/Text；ctx 131072 / max 8192；
        # audio generation ✓、function calling ✓（支持异步）、search grounding ✓、thinking ✓
        "gemini-2.5-flash-native-audio-preview-12-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-live",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_audio=True,
                supports_video=True,
                supports_pdf=False,
                supports_audio_generation=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_web_search=True,
                max_tokens=8192,
                context_window=131072,
            ),
            patterns=["gemini-2.5-flash-native-audio-preview-12-2025"],
        ),
        "gemini-2.5-flash-preview-tts": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-tts",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_audio_generation=True,
                supports_pdf=False,
                supports_streaming=True,
                max_tokens=16384,
                context_window=8192,
            ),
            patterns=["gemini-2.5-flash-preview-tts"],
        ),
        # Gemini 2.5 Flash-Lite 系列 - 最快的模型
        "gemini-2.5-flash-lite": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash-lite"],
        ),
        # ⚠️ gemini-2.5-flash-lite-preview-09-2025 已于 2026-03-31 关停，官方建议迁移至 gemini-3.1-flash-lite
        "gemini-2.5-flash-lite-preview-09-2025": SpecificModelConfig(
            version_default="2.5",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-flash-lite-preview-09-2025"],
        ),
        # Gemini 2.5 Pro 系列 - 高级思考模型
        "gemini-2.5-pro": SpecificModelConfig(
            version_default="2.5",
            variant_default="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-2.5-pro"],
        ),
        "gemini-2.5-pro-preview-tts": SpecificModelConfig(
            version_default="2.5",
            variant_default="pro-tts",
            variant_priority=(3,),
            capabilities=ModelCapabilities(
                supports_audio_generation=True,
                supports_streaming=True,
                max_tokens=16384,
                context_window=8192,
            ),
            patterns=["gemini-2.5-pro-preview-tts"],
        ),
        # gemini-3-flash-preview 是 gemini-3.5-flash 的 Preview 别名，官方建议迁移至 gemini-3.6-flash
        "gemini-3-flash-preview": SpecificModelConfig(
            version_default="3.0",
            variant_default="flash",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_streaming=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3-flash-preview"],
        ),
        # Gemini 3.5 / 3.6 / 3.7 Flash 系列（GA）- 2026 年 Flash 迭代主线
        # 官方规格（2026-08 采集）：输入 Text/Image/Video/Audio/PDF，输出 Text；
        # 1M 上下文 / 65536 输出；支持 thinking、结构化输出、代码执行、文件搜索、
        # 搜索接地、URL context（Computer use 为 Preview）
        "gemini-3.5-flash": SpecificModelConfig(
            version_default="3.5",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.5-flash"],
        ),
        # gemini-3.6-flash：2026-07-21 GA，擅长代码生成与智能体执行循环
        "gemini-3.6-flash": SpecificModelConfig(
            version_default="3.6",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.6-flash"],
        ),
        # gemini-3.7-flash：2026-08 GA，当前最新 Flash；thinking 仅支持 low/medium/high（不支持 minimal）
        "gemini-3.7-flash": SpecificModelConfig(
            version_default="3.7",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.7-flash"],
        ),
        # gemini-3.5-flash-lite：2026-07-21 GA，面向高吞吐子智能体与文档解析
        "gemini-3.5-flash-lite": SpecificModelConfig(
            version_default="3.5",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.5-flash-lite"],
        ),
        # Gemini 3.1 系列 / Gemini 3.1 Series
        # 注意：官方 API ID 使用点号格式 gemini-3.1-*（而非短横线 gemini-3-1-*）
        "gemini-3.1-pro-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="pro",
            variant_priority=(4,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_streaming=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            # gemini-3.1-pro-preview-customtools：面向 bash + 自定义工具的智能体端点
            patterns=["gemini-3.1-pro-preview", "gemini-3.1-pro-preview-customtools"],
        ),
        # ⚠️ gemini-3.1-flash-lite-preview 已于 2026-05-25 关停，GA 版为 gemini-3.1-flash-lite（计划 2027-05-07 关停）
        "gemini-3.1-flash-lite-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_thinking=True,
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_function_calling=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_streaming=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.1-flash-lite-preview"],
        ),
        # gemini-3.1-flash-lite：2026-05-07 GA（官方详情页未附规格卡，
        # 能力与 token 上限沿用其 preview 版官方公布值：1M ctx / 65536 out）
        "gemini-3.1-flash-lite": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_pdf=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_file_search=True,
                supports_code_interpreter=True,
                max_tokens=65536,
                context_window=1048576,
            ),
            patterns=["gemini-3.1-flash-lite"],
        ),
        # Nano Banana 2（GA）：2026-05-28 发布
        # 官方规格：输入 Text/Image/PDF，输出 Image/Text；ctx 131072 / max 32768；
        # image_generation ✓、search grounding ✓；caching/code execution/function calling/structured ✗
        "gemini-3.1-flash-image": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-image",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_pdf=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                supports_web_search=True,
                max_tokens=32768,
                context_window=131072,
            ),
            patterns=["gemini-3.1-flash-image"],
        ),
        # Nano Banana 2 Lite（GA）：仅 1K 分辨率、14 种宽高比
        # 官方规格：输入 Text/Image，输出 Image/Text；ctx 65536 / max 4096；
        # image_generation ✓、function calling ✓；search grounding/structured ✗
        "gemini-3.1-flash-lite-image": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-lite-image",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_image_generation=True,
                supports_thinking=False,
                supports_audio=False,
                supports_streaming=True,
                supports_function_calling=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_tokens=4096,
                context_window=65536,
            ),
            patterns=["gemini-3.1-flash-lite-image"],
        ),
        # ==========================================================================
        # 实时/语音/视频特化模型（2026 新增）
        # ==========================================================================
        # Gemini 3.1 Flash Live：2026-03-11 发布的 A2A 实时对话模型
        # 官方详情页未附规格卡；ctx 取 Live API 官方约束（原生音频输出模型 128k），
        # max_tokens 参照官方指定的迁移源 gemini-2.5-flash-native-audio-preview-12-2025（8192）。
        # thinking 经 thinkingLevel 控制（minimal 默认）；function calling 仅同步（async 不支持）
        "gemini-3.1-flash-live-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-live",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_audio=True,
                supports_video=True,
                supports_pdf=False,
                supports_audio_generation=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_web_search=True,
                max_tokens=8192,
                context_window=131072,
            ),
            patterns=["gemini-3.1-flash-live-preview"],
        ),
        # Gemini 3.1 Flash TTS：2026-04-13 发布，新增表现力音频标记
        # 官方规格：输入 Text，输出 Audio；ctx 8192 / max 16384；仅 audio generation
        "gemini-3.1-flash-tts-preview": SpecificModelConfig(
            version_default="3.1",
            variant_default="flash-tts",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_audio_generation=True,
                supports_pdf=False,
                supports_thinking=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_tokens=16384,
                context_window=8192,
            ),
            patterns=["gemini-3.1-flash-tts-preview"],
        ),
        # Gemini 3.5 实时翻译：双向实时口语翻译，70+ 语言
        # 官方规格：输入 Audio(speech)，输出 Audio(翻译语音)+Text(转写)；
        # ctx 131072 / max 65536；仅 live API 与 audio generation
        "gemini-3.5-live-translate-preview": SpecificModelConfig(
            version_default="3.5",
            variant_default="live-translate",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_audio=True,
                supports_audio_generation=True,
                supports_thinking=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                max_tokens=65536,
                context_window=131072,
            ),
            patterns=["gemini-3.5-live-translate-preview"],
        ),
        # Gemini Omni Flash：对话式视频生成/编辑模型（Preview，走 Interactions API）
        # 官方规格：输入 Text/Image/Video（编辑 ≤10s），输出 Video（3-10s 720p 24FPS）；
        # ctx 1048576；输出为视频无 token 上限数据。官方文档 model code 存在
        # gemini-omni-flash（总览页）与 gemini-omni-flash-preview（详情页）两种写法，均收录。
        # 注：官方未标注版本号，按家族默认 3.0 处理
        "gemini-omni-flash": SpecificModelConfig(
            version_default="3.0",
            variant_default="omni-flash",
            variant_priority=(6,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_video=True,
                supports_thinking=False,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=False,
                context_window=1048576,
            ),
            patterns=["gemini-omni-flash", "gemini-omni-flash-preview"],
        ),
        # Gemini 2.0 Flash 系列 - 第二代主力模型
        # ⚠️ gemini-2.0-flash 已于 2026-06-01 关停，官方建议迁移至 gemini-3.6-flash
        "gemini-2.0-flash": SpecificModelConfig(
            version_default="2.0",
            variant_default="flash",
            variant_priority=(1,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_thinking=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                supports_web_search=True,
                supports_code_interpreter=True,
                max_tokens=8192,
                context_window=1048576,
            ),
            patterns=["gemini-2.0-flash", "gemini-2.0-flash-001", "gemini-2.0-flash-exp"],
        ),
        "gemini-2.0-flash-preview-image-generation": SpecificModelConfig(
            version_default="2.0",
            variant_default="flash-image",
            variant_priority=(2,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_thinking=False,
                supports_audio=False,
                supports_image_generation=True,
                supports_streaming=True,
                supports_structured_outputs=False,
                supports_json_outputs=True,
                max_tokens=8192,
                context_window=32768,
            ),
            patterns=["gemini-2.0-flash-preview-image-generation"],
        ),
        # Gemini 2.0 Flash-Lite 系列 - 第二代快速模型
        # ⚠️ gemini-2.0-flash-lite 已于 2026-06-01 关停，官方建议迁移至 gemini-3.1-flash-lite
        "gemini-2.0-flash-lite": SpecificModelConfig(
            version_default="2.0",
            variant_default="flash-lite",
            variant_priority=(0,),
            capabilities=ModelCapabilities(
                supports_vision=True,
                supports_audio=True,
                supports_video=True,
                supports_function_calling=True,
                supports_streaming=True,
                supports_structured_outputs=True,
                supports_json_outputs=True,
                max_tokens=8192,
                context_window=1048576,
            ),
            patterns=["gemini-2.0-flash-lite", "gemini-2.0-flash-lite-001"],
        ),
    },
)
