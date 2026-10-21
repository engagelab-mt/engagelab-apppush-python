"""Internal serialization utilities for converting between Python objects and JSON-compatible dicts."""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, Type, TypeVar, Union, get_args, get_origin, get_type_hints

T = TypeVar("T")


def to_dict(obj: Any) -> Any:
    """Recursively convert a dataclass instance (or dict/list) to a JSON-serializable dict.

    ``None`` values are omitted, mirroring Go's ``omitempty`` JSON tag behaviour.
    """
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items() if v is not None}
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        result: Dict[str, Any] = {}
        field_map: Dict[str, str] = getattr(type(obj), "_FIELD_MAP", {})
        for f in dataclasses.fields(obj):
            val = getattr(obj, f.name)
            if val is None:
                continue
            key = field_map.get(f.name, f.name)
            result[key] = to_dict(val)
        return result
    if isinstance(obj, (list, tuple)):
        return [to_dict(v) for v in obj]
    return obj


def from_dict(cls: Type[T], data: Any) -> T:  # type: ignore[return]
    """Create a dataclass instance from a dict, mapping JSON keys back to field names."""
    if data is None:
        return None  # type: ignore[return-value]
    if not dataclasses.is_dataclass(cls):
        return data  # type: ignore[return-value]
    field_map: Dict[str, str] = getattr(cls, "_FIELD_MAP", {})
    type_hints = get_type_hints(cls)
    kwargs: Dict[str, Any] = {}
    for f in dataclasses.fields(cls):
        json_key = field_map.get(f.name, f.name)
        if json_key in data:
            kwargs[f.name] = _from_value(type_hints.get(f.name, f.type), data[json_key])
        elif f.name in data:
            kwargs[f.name] = _from_value(type_hints.get(f.name, f.type), data[f.name])
    return cls(**kwargs)


def _from_value(annotation: Any, value: Any) -> Any:
    """Recursively materialize nested dataclasses declared by a response model."""
    if value is None or annotation is Any:
        return value
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is Union:
        target = next((arg for arg in args if arg is not type(None)), Any)
        return _from_value(target, value)
    if origin is list and args:
        return [_from_value(args[0], item) for item in value]
    if origin is dict and len(args) == 2:
        return {key: _from_value(args[1], item) for key, item in value.items()}
    if dataclasses.is_dataclass(annotation) and isinstance(value, dict):
        return from_dict(annotation, value)
    return value
