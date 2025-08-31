from typing import Any, Callable, Literal, ParamSpec, TypeVar
from rich import print

from testapp.lib.datatypes import StrArgs

_rich_stldict: dict[str, str] = {
    'i': 'italic',
    'u': 'underline',
    'b': 'bold',
    'int': 'deep_pink3',
    'str': 'bright_green',
    'tkn': 'yellow',
    'list': 'bright_blue',
    'tuple': 'bright_blue',
    'float': 'deep_pink3',
    'err': 'bright_red',
}

class Printer:
    g_styler: list[Callable[[*tuple[str, ...]], Literal[0,1]|Any]] = []
    g_fallback: Callable[[*tuple[str, ...]], Literal[0,1]|Any] | None = None
    def __init__(
        self,
        *styler: Callable[[*tuple[str, ...]], Literal[0,1]|Any],
        after: Callable[[*tuple[str, ...]], Literal[0,1]|Any] | None = None,
        mode: Literal['global', 'local'] = 'local'
    ):
        self._styler: list[Callable] = []
        self._after: Callable[[StrArgs], Any]|None = None

        self.set_styler(*styler, after = after, mode = mode)

    @property
    def styler(self) -> list[Callable[[*tuple[str, ...]], Literal[0,1]|Any]]:
        funcs = [func for func in self._styler]
        g_funcs = [func for func in Printer.g_styler if not func in funcs]
        return funcs + g_funcs

    def set_styler(
        self,
        *styler: Callable[[*tuple[str, ...]], Literal[0,1]|Any],
        after: Callable[[StrArgs], Literal[0,1]|Any] | None = None,
        mode: Literal['local', 'global'] = 'local'
    ):
        if mode == 'global':
            Printer.g_styler = [f for f in styler]
            if after:
                Printer.after = after
        else:
            self._styler = [f for f in styler]
            if after:
                self._after = after
        return


def rstyle(token: str, *opts: str) -> str:
    """Styling via `rich` markdown."""
    result = token
    for opt in opts:
        if not opt in _rich_stldict.keys():
            var = opt
        else:
            var = _rich_stldict[opt]
        result = f"[{var}]{result}[/{var}]"
    return result
