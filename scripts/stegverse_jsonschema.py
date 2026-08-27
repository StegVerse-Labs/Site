#!/usr/bin/env python3
"""Small repository-local JSON Schema validator for the Site schemas in active use.

This is intentionally a bounded implementation, not a general replacement for the
JSON Schema specification. It implements exactly the keywords exercised by the
checked-in Site schemas used by HIL/validation receipts.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ValidationError:
    message: str
    path: list[Any]


class FormatChecker:
    pass


def _resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported non-local $ref: {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"$ref does not resolve to schema object: {ref}")
    return node


def _is_type(value: Any, name: str) -> bool:
    if name == "null":
        return value is None
    if name == "boolean":
        return isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "string":
        return isinstance(value, str)
    if name == "array":
        return isinstance(value, list)
    if name == "object":
        return isinstance(value, dict)
    return False


def _matches_type(value: Any, spec: Any) -> bool:
    if isinstance(spec, str):
        return _is_type(value, spec)
    if isinstance(spec, list):
        return any(isinstance(name, str) and _is_type(value, name) for name in spec)
    return True


def _valid_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class Draft202012Validator:
    def __init__(self, schema: dict[str, Any], format_checker: Any = None):
        self.schema = schema
        self.format_checker = format_checker

    def iter_errors(self, instance: Any):
        yield from self._validate(instance, self.schema, [], self.schema)

    def _validate(self, instance: Any, schema: dict[str, Any], path: list[Any], root: dict[str, Any]):
        if "$ref" in schema:
            yield from self._validate(instance, _resolve_ref(root, schema["$ref"]), path, root)
            return

        if "type" in schema and not _matches_type(instance, schema["type"]):
            yield ValidationError(f"{instance!r} is not of type {schema['type']!r}", list(path))
            return

        if "const" in schema and instance != schema["const"]:
            yield ValidationError(f"{instance!r} was expected to equal {schema['const']!r}", list(path))

        if "enum" in schema and instance not in schema["enum"]:
            yield ValidationError(f"{instance!r} is not one of {schema['enum']!r}", list(path))

        if isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                yield ValidationError(f"{instance!r} is too short", list(path))
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                yield ValidationError(f"{instance!r} is too long", list(path))
            if "pattern" in schema and re.search(schema["pattern"], instance) is None:
                yield ValidationError(f"{instance!r} does not match {schema['pattern']!r}", list(path))
            if schema.get("format") == "date-time" and not _valid_datetime(instance):
                yield ValidationError(f"{instance!r} is not a valid date-time", list(path))

        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if "minimum" in schema and instance < schema["minimum"]:
                yield ValidationError(f"{instance!r} is less than minimum {schema['minimum']!r}", list(path))
            if "maximum" in schema and instance > schema["maximum"]:
                yield ValidationError(f"{instance!r} is greater than maximum {schema['maximum']!r}", list(path))

        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                yield ValidationError("array has too few items", list(path))
            if "maxItems" in schema and len(instance) > schema["maxItems"]:
                yield ValidationError("array has too many items", list(path))
            if schema.get("uniqueItems") is True:
                seen = set()
                for idx, item in enumerate(instance):
                    key = _canon(item)
                    if key in seen:
                        yield ValidationError("array items are not unique", path + [idx])
                        break
                    seen.add(key)
            if isinstance(schema.get("items"), dict):
                for idx, item in enumerate(instance):
                    yield from self._validate(item, schema["items"], path + [idx], root)
            if isinstance(schema.get("contains"), dict):
                if not any(not list(self._validate(item, schema["contains"], path + [idx], root))
                           for idx, item in enumerate(instance)):
                    yield ValidationError("array does not contain an item matching contains", list(path))

        if isinstance(instance, dict):
            required = schema.get("required", [])
            for key in required:
                if key not in instance:
                    yield ValidationError(f"{key!r} is a required property", list(path))

            properties = schema.get("properties", {})
            if isinstance(properties, dict):
                for key, child_schema in properties.items():
                    if key in instance and isinstance(child_schema, dict):
                        yield from self._validate(instance[key], child_schema, path + [key], root)

            if "minProperties" in schema and len(instance) < schema["minProperties"]:
                yield ValidationError("object has too few properties", list(path))

            additional = schema.get("additionalProperties", True)
            extras = [key for key in instance if key not in properties]
            if additional is False and extras:
                for key in extras:
                    yield ValidationError(f"additional property {key!r} is not allowed", path + [key])
            elif isinstance(additional, dict):
                for key in extras:
                    yield from self._validate(instance[key], additional, path + [key], root)

        for subschema in schema.get("allOf", []):
            yield from self._validate(instance, subschema, path, root)

        if "anyOf" in schema:
            branches = schema["anyOf"]
            if not any(not list(self._validate(instance, branch, path, root)) for branch in branches):
                yield ValidationError("value does not satisfy anyOf", list(path))

        if "oneOf" in schema:
            count = sum(1 for branch in schema["oneOf"] if not list(self._validate(instance, branch, path, root)))
            if count != 1:
                yield ValidationError("value does not satisfy exactly one oneOf branch", list(path))

        if "not" in schema and not list(self._validate(instance, schema["not"], path, root)):
            yield ValidationError("value matches forbidden not schema", list(path))

        if "if" in schema:
            condition_errors = list(self._validate(instance, schema["if"], path, root))
            if not condition_errors and "then" in schema:
                yield from self._validate(instance, schema["then"], path, root)
            elif condition_errors and "else" in schema:
                yield from self._validate(instance, schema["else"], path, root)


def validate(instance: Any, schema: dict[str, Any]) -> None:
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance))
    if errors:
        first = errors[0]
        location = "/".join(map(str, first.path)) or "<root>"
        raise ValueError(f"{location}: {first.message}")
