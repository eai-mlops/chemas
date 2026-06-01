"""Tests ensuring the TASK_INPUT_MODELS registry stays consistent with the
`type` discriminator declared on each request model."""

import typing

import pytest

from eai_schemas import tasks
from eai_schemas.tasks import EAIBase, TASK_INPUT_MODELS


def _type_literals(model: type[EAIBase]) -> list[str]:
    """Return the allowed values of a model's `type` Literal field."""
    field = model.model_fields["type"]
    return list(typing.get_args(field.annotation))


def _all_request_models() -> list[type[EAIBase]]:
    """Every EAIBase subclass in tasks.py that declares a `type` field."""
    return [
        obj
        for obj in vars(tasks).values()
        if isinstance(obj, type)
        and issubclass(obj, EAIBase)
        and obj is not EAIBase
        and "type" in obj.model_fields
    ]


@pytest.mark.parametrize(
    "key, model",
    TASK_INPUT_MODELS.items(),
    ids=list(TASK_INPUT_MODELS),
)
def test_registry_key_matches_model_type(key: str, model: type[EAIBase]) -> None:
    """The registry key must equal the model's `type` literal and its default."""
    literals = _type_literals(model)

    # The `type` field is a single-valued Literal pinned to the task name.
    assert literals == [key], (
        f"{model.__name__}.type literal {literals} does not match "
        f"registry key {key!r}"
    )

    # The `type` field defaults to the registry key, so an instance created
    # without overriding it reports the right task name.
    assert model.model_fields["type"].default == key


def test_every_request_model_is_registered() -> None:
    """No request model with a `type` field is left out of the registry."""
    registered = set(TASK_INPUT_MODELS.values())
    missing = [m.__name__ for m in _all_request_models() if m not in registered]
    assert not missing, f"models missing from TASK_INPUT_MODELS: {missing}"


def test_no_duplicate_registered_models() -> None:
    """Each model is registered under exactly one key."""
    models = list(TASK_INPUT_MODELS.values())
    assert len(models) == len(set(models))
