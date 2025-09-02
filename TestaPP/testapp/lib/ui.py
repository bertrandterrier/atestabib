from typing import Any, Callable, Literal, ParamSpec, TypeVar
from rich import print

from testapp.lib.datatypes import Stringable, Truthable
from testapp.lib.helper import nil_call

P = ParamSpec("P")
X = TypeVar("X")

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


class FormatPrinter:
    g_formatter: list[Callable] = [rstyle]
    g_fallback: Callable = nil_call
    g_call_print: bool = True
    g_call_style: bool = True
    g_use_globals: bool = True

    def __call__(self, *args, **kwargs) -> str:
        result = ""
        if not 'style' in self.callmodes:
            result = self.concat(*args, sep = kwargs.get('sep', " "))
            if 'print' in self.callmodes:
                print(result)
        elif 'print' in self.callmodes:
            result = self.print(*args, **kwargs)
        else:
            result, E, *_ = self.style(self.concat(*args, sep = kwargs.get('sep', ' ')))
            if E:
                raise E 
        if not result:
            raise RuntimeError(f"Invalid result: \"{result}\"")
        return result

    def concat(self, *args, sep: str = " ") -> str:
        result = ""
        for i, arg in enumerate(args):
            if i > 0:
                result += sep
            result += arg
        return result
                

    def set(
        self,
        *fmts: Callable,
        call_print: bool|None = None,
        call_style: bool|None = None,
        use_globals: bool | None  = None,
        fallback: Callable | None = None,
    ):
        self._fmts: list[Callable] = [func for func in fmts]
        self._call_print: bool = call_print or self.g_call_print
        self._call_style: bool = call_style or self.g_call_style
        self._use_globals: bool = use_globals or FormatPrinter.g_use_globals
        self._fallback: Callable | None = fallback

    def fallback(self, *args, **kwargs) -> Any:
        if not self._fallback:
            return self.g_fallback(*args, **kwargs)
        return self._fallback(*args, **kwargs)

    def get_formatter(self, use: Literal['global', 'local', 'global_only']) -> list[Callable]:
        result = []
        if not use == 'global_only':
            result += [f for f in self._fmts]
        if not use == 'local':
            result += [f for f in self.g_formatter]
        return result

    def set_formatter(self, *fmts: Callable, reset: bool = False,  apply_to: Literal['local', 'global'] = 'local'):
        match apply_to:
            case 'local':
                if reset:
                    self._fmts = []
                for func in fmts:
                    if not func in self._fmts:
                        self._fmts.append(func)
            case 'global':
                if reset:
                    FormatPrinter.g_formatter = []
                for func in fmts:
                    if not func in self.g_formatter:
                        FormatPrinter.g_formatter.append(func)
        return

    @property
    def mode(self) -> str:
        if self._use_globals:
            return 'global'
        return 'local'

    @property
    def callmodes(self) -> list[str]:
        result: list = []
        if self._call_print:
            result.append('print')
        if self._call_style:
            result.append('style')
        result.append(self.mode)
        return result

    def style(
        self,
        arg: Stringable,
        err_react: Literal['break', 'fail', 'ignore'] = 'ignore',
        *args,
        **kwargs,
    ) -> tuple[str, None|Exception, Any]:
        var = str(arg)
        new_var = ""

        if not isinstance(
            self.mode, Literal['local', 'global', 'global_only']
        ):
            raise AttributeError(f"Invalid self.mode \"{self.mode}\".")

        for func in self.get_formatter(self.mode):
            try:
                new_var = func(var, *args, **kwargs)
                if not isinstance(new_var, str):
                    raise TypeError(f"Invalid type {type(new_var)} for '{new_var}'")
                var += new_var
            except Exception as e:
                if err_react == 'fail':
                    raise e
                elif err_react == 'break':
                    return var, e, new_var
                elif err_react == 'ignore':
                    continue
        return var, None, ""

    def print(
        self,
        *args: Stringable,
        sep: str = " ",
        fallback: Callable = nil_call,
        instant_print: bool = False,
        **kwargs,
    ) -> str|None:
        token = ""
        for arg in args:
            iter_result = self.style(arg, 'ignore', **kwargs)
            if not isinstance(iter_result, str):
                iter_result = fallback(iter_result, sep = 'sep',**kwargs)
                if not isinstance(iter_result, str):
                    continue
            if not token:
                token += sep
            token += iter_result
        if instant_print:
            print(token)
        return token
