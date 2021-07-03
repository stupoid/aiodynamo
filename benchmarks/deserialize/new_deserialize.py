import base64
from typing import Any, Callable, Dict, List, Set, TypeVar

from aiodynamo.types import Numeric

T = TypeVar("T")


def deserialize_simple_types(val: T, *_) -> T:
    return val


def deserialize_binary(val: bytes, *_) -> bytes:
    return base64.b64decode(val)


def deserialize_string_set(val: List[str], *_) -> Set[str]:
    return set(val)


def deserialize_binary_set(val: List[bytes], *_) -> Set[bytes]:
    return {base64.b64decode(v) for v in val}


def deserialize_null(*_) -> None:
    return None


def deserialize_number(val: str, numeric_type: Callable[[str], T]) -> T:
    return numeric_type(val)


def deserialize_number_set(val: List[str], numeric_type: Callable[[str], T]) -> Set[T]:
    return {numeric_type(v) for v in val}


def deserialize_list(val: List[Any], numeric_type: Callable[[str], Any]) -> List[Any]:
    return [deserialize(v, numeric_type) for v in val]


def deserialize_map(
    val: Dict[str, Any], numeric_type: Callable[[str], Any]
) -> Dict[str, Any]:
    return {k: deserialize(v, numeric_type) for k, v in val.items()}


tag_deserialize_mapping: Dict[str, Callable[..., Any]] = {
    "S": deserialize_simple_types,
    "SS": deserialize_string_set,
    "N": deserialize_number,
    "NS": deserialize_number_set,
    "B": deserialize_binary,
    "BS": deserialize_binary_set,
    "BOOL": deserialize_simple_types,
    "NULL": deserialize_null,
    "L": deserialize_list,
    "M": deserialize_map,
}


def deserialize(value: Dict[str, Any], numeric_type: Callable[[str], Numeric]) -> Any:
    if not value:
        raise TypeError(
            "Value must be a nonempty dictionary whose key " "is a valid dynamodb type."
        )
    tag, val = next(iter(value.items()))
    try:
        return tag_deserialize_mapping[tag](val, numeric_type)
    except KeyError:
        raise TypeError(f"Dynamodb type {tag} is not supported")
