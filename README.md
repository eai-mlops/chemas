# eai-schemas

Reusable Pydantic input models for generative-AI task types.

One model class per task — all model providers of the same task type share
the same input schema. Model-specific extras are accepted via `extra="allow"`.

## Install

```bash
pip install eai-schemas
```

## Use

```python
from eai_schemas import TextToImageInput, TASK_INPUT_MODELS

payload = TextToImageInput(prompt="a sunset over mountains", num_images=2)
payload.model_dump(exclude_none=True)

# dispatch by task name
cls = TASK_INPUT_MODELS["text-to-video"]
payload = cls(prompt="a drone shot of a forest at dawn", duration="6")
```

## Supported task types

`text-to-image`, `image-to-image`, `image-inpainting`, `image-upscaling`,
`background-removal`, `text-to-video`, `image-to-video`, `video-to-video`,
`text-to-speech`, `speech-to-text`, `text-to-music`, `image-to-3d`,
`text-to-3d`, `vision`.
