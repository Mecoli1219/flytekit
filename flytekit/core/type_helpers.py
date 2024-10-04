import importlib
import typing

T = typing.TypeVar("T")


def load_type_from_tag(tag: str) -> typing.Type[T]:
    """
    Loads python type from tag
    """

    if "." not in tag:
        raise ValueError(
            f"Protobuf tag must include at least one '.' to delineate package and object name got {tag}",
        )

    module, name = tag.rsplit(".", 1)
    try:
        pb_module = importlib.import_module(module)
    except ImportError:
        raise ValueError(f"Could not resolve the protobuf definition @ {module}.  Is the protobuf library installed?")

    if not hasattr(pb_module, name):
        raise ValueError(f"Could not find the protobuf named: {name} @ {module}.")

    return getattr(pb_module, name)


def is_namedtuple(t: typing.Type[T]) -> bool:
    if hasattr(t, "__bases__") and (
        isinstance(t, typing.Type) or isinstance(t, typing.TypeVar)  # type: ignore
    ):
        bases = t.__bases__
        if len(bases) == 1 and bases[0] == tuple and hasattr(t, "_fields"):
            return True

    return False
