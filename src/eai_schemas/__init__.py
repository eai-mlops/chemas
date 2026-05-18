"""eai-schemas: Pydantic input models for generative-AI task types."""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

from eai_schemas.tasks import (
    # base
    EAIBase,
    LoraWeight,
    # image
    TextToImageInput,
    ImageToImageInput,
    ImageInpaintingInput,
    ImageUpscalingInput,
    BackgroundRemovalInput,
    # video
    TextToVideoInput,
    ImageToVideoInput,
    VideoToVideoInput,
    # audio / speech / music
    TextToSpeechInput,
    SpeechToTextInput,
    TextToMusicInput,
    # 3d
    ImageTo3DInput,
    TextTo3DInput,
    # vision
    VisionInput,
    # registry & shared enums
    TASK_INPUT_MODELS,
    ImageSize,
    ImageAspectRatio,
    VideoAspectRatio,
    VideoResolution,
    VideoDuration,
    ImageOutputFormat,
    Acceleration,
    TextureQuality,
)

try:
    __version__ = _pkg_version("eai-schemas")
except PackageNotFoundError:  # package not installed (editable source checkout)
    __version__ = "0.0.0+local"

__all__ = [
    "__version__",
    "EAIBase",
    "LoraWeight",
    "TextToImageInput",
    "ImageToImageInput",
    "ImageInpaintingInput",
    "ImageUpscalingInput",
    "BackgroundRemovalInput",
    "TextToVideoInput",
    "ImageToVideoInput",
    "VideoToVideoInput",
    "TextToSpeechInput",
    "SpeechToTextInput",
    "TextToMusicInput",
    "ImageTo3DInput",
    "TextTo3DInput",
    "VisionInput",
    "TASK_INPUT_MODELS",
    "ImageSize",
    "ImageAspectRatio",
    "VideoAspectRatio",
    "VideoResolution",
    "VideoDuration",
    "ImageOutputFormat",
    "Acceleration",
    "TextureQuality",
]
