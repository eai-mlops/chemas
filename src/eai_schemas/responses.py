"""
Pydantic output models for generation task responses.
"""

from pydantic import BaseModel, ConfigDict, Field, AnyUrl

# ---------------------------------------------------------------------------
# Base / file primitives
# ---------------------------------------------------------------------------

Timings = dict[str, float]


class EAIResponseBase(BaseModel):
    """Shared base: every response echoes the request_id and allows extras."""

    model_config = ConfigDict(extra="allow")

    request_id: str = Field(description="Request ID echoed from the request.")


class File(BaseModel):
    """A generated file artifact returned by reference URL."""

    model_config = ConfigDict(extra="allow")

    # can be base64 data uri
    url: AnyUrl = Field(description="URL to download the file.")
    content_type: str | None = Field(default=None, description="MIME type.")
    file_name: str | None = None
    file_size: int | None = Field(default=None, description="Size in bytes.")


class ImageFile(File):
    """A generated image with pixel dimensions."""

    width: int | None = None
    height: int | None = None


# ---------------------------------------------------------------------------
# IMAGE
# ---------------------------------------------------------------------------

class _ImagesOutput(EAIResponseBase):
    """Family base for tasks that return N generated images."""

    images: list[ImageFile] = Field(default_factory=list)
    seed: int | None = None
    has_nsfw_concepts: list[bool] | None = Field(
        default=None,
        description="Per-image NSFW flag, when a safety checker ran.",
    )
    prompt: str | None = None
    timings: Timings | None = None


class TextToImageOutput(_ImagesOutput):
    """Pairs with `TextToImageInput`."""


class ImageToImageOutput(_ImagesOutput):
    """Pairs with `ImageToImageInput`."""


class ImageInpaintingOutput(_ImagesOutput):
    """Pairs with `ImageInpaintingInput`."""


class ImageUpscalingOutput(EAIResponseBase):
    """Pairs with `ImageUpscalingInput` — single upscaled image."""

    image: ImageFile
    timings: Timings | None = None


class BackgroundRemovalOutput(EAIResponseBase):
    """Pairs with `BackgroundRemovalInput` — cut-out plus optional mask."""

    image: ImageFile
    mask_image: ImageFile | None = Field(
        default=None,
        description="Foreground mask, returned when output_mask=True.",
    )


# ---------------------------------------------------------------------------
# VIDEO
# ---------------------------------------------------------------------------

class _VideoOutput(EAIResponseBase):
    """Family base for tasks that return a single generated video."""

    video: File
    seed: int | None = None
    has_nsfw_concepts: bool | None = None
    prompt: str | None = None
    timings: Timings | None = None


class TextToVideoOutput(_VideoOutput):
    """Pairs with `TextToVideoInput`."""


class ImageToVideoOutput(_VideoOutput):
    """Pairs with `ImageToVideoInput`."""


class VideoToVideoOutput(_VideoOutput):
    """Pairs with `VideoToVideoInput`."""


# ---------------------------------------------------------------------------
# AUDIO / SPEECH / MUSIC
# ---------------------------------------------------------------------------

class TextToSpeechOutput(EAIResponseBase):
    """Pairs with `TextToSpeechInput`."""

    audio: File
    timings: Timings | None = None


class TextToMusicOutput(EAIResponseBase):
    """Pairs with `TextToMusicInput`."""

    audio: File
    seed: int | None = None
    timings: Timings | None = None


class TranscriptionChunk(BaseModel):
    """A single timestamped segment/word in a transcription."""

    model_config = ConfigDict(extra="allow")

    text: str
    timestamp: tuple[float | None, float | None] | None = Field(
        default=None,
        description="(start, end) in seconds.",
    )
    speaker: str | None = None


class DiarizationSegment(BaseModel):
    """A speaker-diarization segment (Whisper-style)."""

    model_config = ConfigDict(extra="allow")

    speaker: str
    timestamp: tuple[float | None, float | None] | None = Field(
        default=None,
        description="(start, end) in seconds.",
    )


class SpeechToTextOutput(EAIResponseBase):
    """Pairs with `SpeechToTextInput`."""

    text: str = Field(description="Full transcription.")
    chunks: list[TranscriptionChunk] = Field(default_factory=list)
    inferred_languages: list[str] = Field(default_factory=list)
    diarization_segments: list[DiarizationSegment] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# 3D
# ---------------------------------------------------------------------------

class _Mesh3DOutput(EAIResponseBase):
    """Family base for tasks that return a 3D mesh asset."""

    model_mesh: File = Field(description="Primary mesh asset (glb / obj / usdz / ...).")
    model_textures: list[File] = Field(
        default_factory=list,
        description="Texture maps, when the backend returns them separately.",
    )
    preview_image: ImageFile | None = None
    seed: int | None = None
    timings: Timings | None = None


class ImageTo3DOutput(_Mesh3DOutput):
    """Pairs with `ImageTo3DInput`."""


class TextTo3DOutput(_Mesh3DOutput):
    """Pairs with `TextTo3DInput`."""


# ---------------------------------------------------------------------------
# VISION (image understanding)
# ---------------------------------------------------------------------------

class VisionOutput(EAIResponseBase):
    """Pairs with `VisionInput` — free-form text response.

    `results` matches the Florence-2 convention; chat-completion-style
    extras (usage, finish_reason, ...) flow through via `extra="allow"`.
    """

    results: str = Field(description="Model's text response.")


# ---------------------------------------------------------------------------
# Task-type registry — mirrors `TASK_INPUT_MODELS` in tasks.py.
# ---------------------------------------------------------------------------

TASK_OUTPUT_MODELS: dict[str, type[EAIResponseBase]] = {
    "text-to-image":      TextToImageOutput,
    "image-to-image":     ImageToImageOutput,
    "image-inpainting":   ImageInpaintingOutput,
    "image-upscaling":    ImageUpscalingOutput,
    "background-removal": BackgroundRemovalOutput,
    "text-to-video":      TextToVideoOutput,
    "image-to-video":     ImageToVideoOutput,
    "video-to-video":     VideoToVideoOutput,
    "text-to-speech":     TextToSpeechOutput,
    "speech-to-text":     SpeechToTextOutput,
    "text-to-music":      TextToMusicOutput,
    "image-to-3d":        ImageTo3DOutput,
    "text-to-3d":         TextTo3DOutput,
    "vision":             VisionOutput,
}
