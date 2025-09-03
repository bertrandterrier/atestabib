import os
import pathlib
from string import ascii_lowercase, ascii_uppercase
from typing import Literal, Protocol, runtime_checkable, Union

PathStr = Union[os.PathLike, pathlib.Path, str]

@runtime_checkable
class Stringable(Protocol):
    def __str__(self) -> str:
        ...

class Letter(str):
    """Letter ensures string of length 1. Use 'case' slot for checking upper/lower 
    case letter. 'self.upper()' and 'self.lower()' methods will create new Letter 
    instance, if not in correct case.
    """
    __slots__ = ("case", "body", "_proxy")
    
    @classmethod
    def proxy(cls, mode: Literal['upper', 'lower', 'joker'] = 'joker') -> "Letter":
        match mode:
            case 'upper':
                l = "*"
            case 'lower':
                l = "_"
            case 'joker':
                l = "&"
        inst = super().__new__(cls, l)
        inst.case = mode
        inst.body = l
        return inst

    def __new__(cls, token) -> "Letter":
        if len(str(token)) != 1:
            raise SyntaxError("Has to be of length 1.")
        elif isinstance(token, Letter):
            return token
        elif hasattr(token, "__lttr__"):
            return token.__lttr__()
        elif isinstance(token, int):
            token = chr(token)

        if not token in ['_', '&', '*'] + list(ascii_uppercase) + list(ascii_lowercase):
            raise SyntaxError("Needs to be letter character or proxy symbol.")
        inst = super().__new__(cls, str(token))
        inst.body = str(token)

        if token in list(ascii_lowercase) + ['_', '&']:
            inst.case = 'lower'
        elif token in list(ascii_uppercase) + ['*', '&']:
            inst.case = 'upper'

        if token in ['*', '_', '&']:
            inst._proxy = True
        else:
            inst._proxy = False

        return inst

    def isproxy(self) -> bool:
        return self._proxy

    def isalpha(self) -> bool:
        return self._proxy == False

    def upper(self) -> "Letter":
        """Returns self or creates Letter with self.case == 'upper'."""
        if not self.isupper():
            tkn = self.body
            if tkn == '*':
                tkn = '_'
            elif tkn == '_':
                tkn = '*'
            return Letter(tkn.upper())
        return self

    def lower(self) -> "Letter":
        """Returns self or creates Letter with self.case == 'lower'."""
        if not self.islower():
            return Letter(str(self).lower())
        return self

    def __str__(self) -> str:
        return self.body

    def __eq__(self, other) -> bool:
        result = False
        if isinstance(other, Stringable):
            var = str(other)
            if len(var) == 1:
                var = Letter(other)
        else:
            var = other
        if isinstance(var, Letter):
            if self.isproxy():
                result = (var.case == self.case) or (self.case == 'joker')
            else:
                result = (var.body == self.body) and (var.case == self.case)
        return result

    def __gt__(self, other) -> bool:
        if not isinstance(other, (str)):
            return False
        if not len(other) == 1:
            return False
        o = Letter(other)
        if self.case == o.case:
            return ord(self.body) > ord(o.body)
        elif self.case in ['upper', 'joker']:
            return True
        else:
            return False

    def __mul__(self, other) -> "str":
        if not isinstance(other, int):
            raise TypeError("Expected integer")
        result = []
        for i in range(other):
            result.append(Letter(self.body))
        return "".join(result)

    def isupper(self) -> bool:
        return self.case == "upper"

    def islower(self) -> bool:
        return self.case == 'lower'

    def __iadd__(self, other) -> "Letter|str":
        if not isinstance(other, int):
            if not isinstance(other, Stringable):
                raise TypeError(f"Invalid type {type(other)}")
            if not isinstance(other, Letter):
                return self.body 
            mod = ord(other.body)
        else:
            mod = other
        return Letter(chr(ord(self.body) + mod))

    def __add__(self, other) -> "Letter|str":
        if isinstance(other, str):
            return str(self) + other
        elif isinstance(other, int):
            var = chr(ord(self) + 1)
            l = Letter(var)
            if l == None:
                raise RuntimeError()
            return l
        raise TypeError()

    def __subtract__(self, other) -> "Letter":
        if not isinstance(other, int):
            raise TypeError()
        l = Letter(chr(ord(self) + 1))
        if not l:
            raise RuntimeError()
        return l

    @classmethod
    def convert(cls, token) -> "Letter|None":
        try:
            return cls.__new__(cls, token)
        except:
            return None

    @classmethod
    def dismantle(cls, token: Stringable) -> "list[Letter|str]":
        result = []
        if len(str(token)) <= 0:
            return []
        for c in list(str(token)):
            var = Letter.convert(c)
            if var in result or not var:
                continue
            result.append(var)
        result.sort()
        return result

class LowerCaseLetter(Letter):
    def __new__(cls, token) -> "LowerCaseLetter":
        var = super().__new__(cls, token)
        inst = str.__new__(cls, var.upper())
        return inst

    def upper(self) -> "LowerCaseLetter":
        return self
    def lower(self) -> "LowerCaseLetter":
        return self
    def freecase(self) -> Letter:
        return Letter(self.body)

class UpperCaseLetter(Letter):
    def __new__(cls, token) -> "UpperCaseLetter":
        var = super().__new__(cls, token)
        inst = str.__new__(cls, var.upper())
        return inst

    def lower(self) -> "UpperCaseLetter":
        return self

    def upper(self) -> "UpperCaseLetter":
        return self

    def freecase(self) -> Letter:
        return Letter(self.body)
