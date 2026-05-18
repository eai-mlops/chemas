"""
Pydantic input models for generation task types.
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
import uuid

# ---------------------------------------------------------------------------
# shared enums / reusable literal types
# ---------------------------------------------------------------------------

ImageSize = Literal[
    "square_hd",
    "square",
    "portrait_4_3",
    "portrait_16_9",
    "landscape_4_3",
    "landscape_16_9",
    "auto",
]

ImageAspectRatio = Literal[
    "auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1",
    "4:5", "3:4", "2:3", "9:16", "4:1", "1:4", "8:1", "1:8",
]

VideoAspectRatio = Literal["auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]

ImageOutputFormat = Literal["jpeg", "png", "webp"]
Acceleration = Literal["none", "regular", "high"]


class EAIBase(BaseModel):
    """Shared base: every dgenration endpoint accepts `sync_mode` and model-specific
    extras the schema docs don't always enumerate."""

    model_config = ConfigDict(extra="allow")

    request_id: str = Field(
        default_factory=lambda: f'req-{uuid.uuid4().hex}',
        description="Request ID for tracking the request.",
    )

    sync_mode: bool | None = Field(
        default=None,
        description="If true, return media as a data URI without storing request history.",
    )


class LoraWeight(BaseModel):
    """A single LoRA adapter applied at inference time.

    Used by FLUX-LoRA, SDXL-LoRA, and most LoRA-enabled image/video pipelines.
    """

    model_config = ConfigDict(extra="allow")

    path: HttpUrl = Field(
        ...,
        description="URL of the LoRA weights file (.safetensors), or a HF repo path "
                    "the backend resolves.",
    )
    scale: float = Field(
        default=1.0,
        ge=0.0,
        le=4.0,
        description="Application strength multiplier. 1.0 = full strength.",
    )


# ---------------------------------------------------------------------------
# IMAGE
# ---------------------------------------------------------------------------

class TextToImageInput(EAIBase):
    """Common input for text-to-image (FLUX, FLUX-LoRA, Z-Image, nano-banana, SDXL, ...)."""

    prompt: str = Field(..., description="Prompt to generate the image from.")
    image_size: ImageSize | None = "landscape_4_3"
    num_inference_steps: int | None = None
    seed: int | None = None
    guidance_scale: float | None = 3.5
    num_images: int = Field(default=1, ge=1)
    enable_safety_checker: bool = True
    output_format: ImageOutputFormat = "jpeg"
    acceleration: Acceleration | None = "none"
    negative_prompt: str | None = None
    loras: list[LoraWeight] = Field(
        default_factory=list,
        description="LoRA adapters to apply. Ignored by non-LoRA backbones.",
    )


class ImageToImageInput(EAIBase):
    """Common input for image-to-image / image-edit (nano-banana edit, FLUX
    img2img, Qwen-Image-Edit, ...). Accepts either a single image_url or a
    list image_urls — both are widely used across generation models."""

    prompt: str = Field(..., description="Edit instruction or new prompt.")
    image_url: HttpUrl | None = None
    image_urls: list[HttpUrl] | None = None
    num_images: int = Field(default=1, ge=1)
    seed: int | None = None
    aspect_ratio: ImageAspectRatio | None = "auto"
    output_format: ImageOutputFormat = "png"
    strength: float | None = Field(default=None, ge=0.0, le=1.0)
    enable_safety_checker: bool = True
    loras: list[LoraWeight] = Field(default_factory=list)


class ImageInpaintingInput(EAIBase):
    """Common input for inpainting models (z-image-turbo-inpaint, FLUX-fill, ...)."""

    prompt: str
    image_url: HttpUrl
    mask_image_url: HttpUrl
    image_size: ImageSize | None = "auto"
    num_inference_steps: int | None = None
    num_images: int = Field(default=1, ge=1)
    seed: int | None = None
    strength: float = Field(default=1.0, ge=0.0, le=1.0)
    output_format: ImageOutputFormat = "png"
    enable_safety_checker: bool = True
    acceleration: Acceleration | None = "regular"
    loras: list[LoraWeight] = Field(default_factory=list)


class ImageUpscalingInput(EAIBase):
    """Common input for upscaling models (Topaz, ESRGAN, clarity-upscaler, ...)."""

    image_url: HttpUrl
    upscale_factor: float = Field(default=2.0, ge=1.0, le=8.0)
    model: str | None = None
    output_format: Literal["jpeg", "png"] = "jpeg"
    prompt: str | None = Field(default=None, description="Optional guidance prompt.")
    face_enhancement: bool | None = None
    creativity: float | None = Field(default=None, ge=0.0, le=1.0)


class BackgroundRemovalInput(EAIBase):
    """Common input for background-removal models (BiRefNet v1/v2, RemBG, ...)."""

    image_url: HttpUrl
    model: str | None = None
    output_format: Literal["webp", "png", "gif"] = "png"
    output_mask: bool = False
    refine_foreground: bool = True
    mask_only: bool = False


# ---------------------------------------------------------------------------
# VIDEO
# ---------------------------------------------------------------------------

VideoResolution = Literal["480p", "540p", "720p", "1080p"]
VideoDuration = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]


class TextToVideoInput(EAIBase):
    """Common input for text-to-video (Seedance, Kling, Sora, Veo, ...)."""

    prompt: str
    aspect_ratio: VideoAspectRatio = "16:9"
    resolution: VideoResolution = "1080p"
    duration: VideoDuration = "5"
    seed: int | None = None
    num_frames: int | None = None
    camera_fixed: bool | None = None
    enable_safety_checker: bool = True
    negative_prompt: str | None = None


class ImageToVideoInput(EAIBase):
    """Common input for image-to-video (Kling i2v, Seedance i2v, Sora i2v, ...)."""

    prompt: str
    image_url: HttpUrl
    duration: VideoDuration = "5"
    aspect_ratio: VideoAspectRatio | None = None
    resolution: VideoResolution | None = None
    negative_prompt: str = "blur, distort, and low quality"
    cfg_scale: float | None = Field(default=0.5, ge=0.0, le=1.0)
    seed: int | None = None


class VideoToVideoInput(EAIBase):
    """Common input for video-to-video / video-edit (Kling O1 v2v, ...)."""

    prompt: str
    video_url: HttpUrl
    aspect_ratio: VideoAspectRatio = "auto"
    duration: VideoDuration = "5"
    keep_audio: bool = False
    image_urls: list[HttpUrl] | None = None  # reference images
    seed: int | None = None


# ---------------------------------------------------------------------------
# AUDIO / SPEECH / MUSIC
# ---------------------------------------------------------------------------

class TextToSpeechInput(EAIBase):
    """Common input for TTS models (xai-tts, ElevenLabs, Kokoro, ...)."""

    text: str = Field(..., description="Text to synthesize (often <= 15k chars).")
    voice: str = "default"
    language: str = "auto"
    output_format: dict | str | None = Field(
        default=None,
        description="Either a format name (e.g. 'mp3_44100_128') or a structured "
                    "{format, sample_rate, bitrate} object.",
    )


class SpeechToTextInput(EAIBase):
    """Common input for STT models (Whisper, Wizper, ...)."""

    audio_url: HttpUrl
    task: Literal["transcribe", "translate"] = "transcribe"
    language: str | None = None
    diarize: bool = False
    chunk_level: Literal["none", "segment", "word"] = "segment"
    batch_size: int = Field(default=64, ge=1, le=64)
    num_speakers: int | None = None
    prompt: str = ""


class TextToMusicInput(EAIBase):
    """Common input for text-to-music models (CassetteAI, Stable Audio, MMAudio, ...)."""

    prompt: str
    duration: int = Field(..., ge=1, description="Duration of generated music, seconds.")
    seed: int | None = None
    negative_prompt: str | None = None


# ---------------------------------------------------------------------------
# 3D
# ---------------------------------------------------------------------------

TextureQuality = Literal["no", "standard", "HD"]


class ImageTo3DInput(EAIBase):
    """Common input for image-to-3D models (Trellis, Hunyuan3D, Tripo i2-3d, ...)."""

    image_url: HttpUrl
    seed: int | None = None
    texture: TextureQuality = "standard"
    pbr: bool = True
    face_limit: int | None = None
    auto_size: bool = False
    quad: bool = False


class TextTo3DInput(EAIBase):
    """Common input for text-to-3D models (Tripo t2-3d, ...)."""

    prompt: str = Field(..., max_length=1024)
    negative_prompt: str | None = Field(default=None, max_length=255)
    seed: int | None = None
    image_seed: int | None = None
    texture_seed: int | None = None
    texture: TextureQuality = "standard"
    pbr: bool = True
    face_limit: int | None = None
    auto_size: bool = False
    quad: bool = False


# ---------------------------------------------------------------------------
# VISION (image understanding)
# ---------------------------------------------------------------------------

class VisionInput(EAIBase):
    """Common input for vision / image-understanding models (Gemini, Florence-2,
    NSFW filter, OpenRouter vision, ...)."""

    image_urls: list[HttpUrl] = Field(..., min_length=1)
    prompt: str
    model: str | None = Field(
        default=None,
        description="Backing vision model id, e.g. 'google/gemini-2.5-flash'. "
                    "Required for the OpenRouter-style router endpoint; ignored otherwise.",
    )


# ---------------------------------------------------------------------------
# Task-type registry — handy when you want to dispatch by task name.
# ---------------------------------------------------------------------------

TASK_INPUT_MODELS: dict[str, type[EAIBase]] = {
    "text-to-image":      TextToImageInput,
    "image-to-image":     ImageToImageInput,
    "image-inpainting":   ImageInpaintingInput,
    "image-upscaling":    ImageUpscalingInput,
    "background-removal": BackgroundRemovalInput,
    "text-to-video":      TextToVideoInput,
    "image-to-video":     ImageToVideoInput,
    "video-to-video":     VideoToVideoInput,
    "text-to-speech":     TextToSpeechInput,
    "speech-to-text":     SpeechToTextInput,
    "text-to-music":      TextToMusicInput,
    "image-to-3d":        ImageTo3DInput,
    "text-to-3d":         TextTo3DInput,
    "vision":             VisionInput,
}
