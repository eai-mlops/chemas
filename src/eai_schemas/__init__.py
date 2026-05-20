"""eai-schemas: Pydantic input models for generative-AI task types."""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

from eai_schemas.tasks import (
    # base
    EAIBase,
    LoraWeight,
    ModelCard,
    ModelList,
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
from eai_schemas.responses import (
    # base / file primitives
    EAIResponseBase,
    File,
    ImageFile,
    Timings,
    # image
    TextToImageOutput,
    ImageToImageOutput,
    ImageInpaintingOutput,
    ImageUpscalingOutput,
    BackgroundRemovalOutput,
    # video
    TextToVideoOutput,
    ImageToVideoOutput,
    VideoToVideoOutput,
    # audio / speech / music
    TextToSpeechOutput,
    SpeechToTextOutput,
    TextToMusicOutput,
    TranscriptionChunk,
    DiarizationSegment,
    # 3d
    ImageTo3DOutput,
    TextTo3DOutput,
    # vision
    VisionOutput,
    # registry
    TASK_OUTPUT_MODELS,
)

try:
    __version__ = _pkg_version("eai-schemas")
except PackageNotFoundError:  # package not installed (editable source checkout)
    __version__ = "0.0.0+local"

__all__ = [
    "__version__",
    # inputs
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
    "ModelCard",
    "ModelList",
    # outputs
    "EAIResponseBase",
    "File",
    "ImageFile",
    "Timings",
    "TextToImageOutput",
    "ImageToImageOutput",
    "ImageInpaintingOutput",
    "ImageUpscalingOutput",
    "BackgroundRemovalOutput",
    "TextToVideoOutput",
    "ImageToVideoOutput",
    "VideoToVideoOutput",
    "TextToSpeechOutput",
    "SpeechToTextOutput",
    "TextToMusicOutput",
    "TranscriptionChunk",
    "DiarizationSegment",
    "ImageTo3DOutput",
    "TextTo3DOutput",
    "VisionOutput",
    "TASK_OUTPUT_MODELS",
]
