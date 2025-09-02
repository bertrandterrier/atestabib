import os
import pathlib
from typing import NewType, Union, Protocol, runtime_checkable

@runtime_checkable
class Stringable(Protocol):
    def __str__(self) -> str:
        ...

@runtime_checkable
class Truthable(Protocol):
    def __bool__(self) -> bool:
        ...

PathStr = Union[str, pathlib.Path, os.PathLike]
StrArgs = NewType("StrArgs", *tuple[Stringable,...])
