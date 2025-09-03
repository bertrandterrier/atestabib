from typing import Any, Literal, Pattern
import re
from warnings import warn

from testapp.lib.datatypes import Letter, UpperCaseLetter
from testapp.lib.functions import safetype, issubset

class Signature:
    """Item signature of the Alfred Testa Library."""
    _serial: int
    _user: UpperCaseLetter
    _base: int
    _suffix: str|None = None

    _pttrn_short: Pattern = re.compile(r"([0-9]{4})([a-zA-Z])([0-9]{3})")
    _pttrn_full: Pattern = re.compile(r"([0-9]{4})([a-zA-Z])([0-9]{3})-([0-9][0-9a-zA-Z]*)")

    def __new__(cls, *args, **kwargs) -> "Signature | list[Signature] | None":
        NEED = ['serial', 'user_id', 'id']
        result: list[Signature] = []

        if issubset(kwargs, NEED):
            result.append(Signature.create(**kwargs))

        for arg in args:
            item = None
            if isinstance(arg, dict):
                if len(arg) < 0:
                    continue
                elif issubset(arg, NEED):
                    item = Signature.create(**arg)
            elif isinstance(arg, str):
                item = Signature.tokenize(arg)
            elif isinstance(arg, Signature):
                item = arg
            else:
                warn(f"[Signature] Invalid argument type \"{type(arg)}\".")

            if isinstance(item, Signature):
                result.append(item)

        if len(result) <= 0:
            return None
        elif len(result) == 1:
            return result[0]
        return result

    @classmethod
    def create(
        cls,
        serial: int|str,
        user_id: UpperCaseLetter|Letter|str,
        base: int|str,
        suffix: int|str|None = None,
    ) -> "Signature":
        inst = super().__new__(cls)

        inst._serial = int(serial)
        inst._user = UpperCaseLetter(user_id)
        inst._base = int(base)

        if suffix:
            inst._suffix = str(suffix)

        return inst

    @classmethod
    def tokenize(cls, arg: str, asdict: bool = False) -> "Signature|dict|None":
        match = cls._pttrn_full.search(arg)
        if match:
            ser, usr, base, suf = match.groups()
        else:
            match = cls._pttrn_short.search(arg)
            if not match:
                return
            ser, usr, base = match.groups()
            suf = None
        result: dict[str, int|str|None] = {
           'serial': int(ser),
           'user': UpperCaseLetter(usr),
           'base': int(base),
           'suffix': suf 
        }
        if asdict:
            return result
        inst = super().__new__(cls)
        for key, val in result.items():
            setattr(inst, f"_{key}", val)
        return inst

    @property
    def serial(self) -> str:
        return f"{self._serial:04d}"

    @property
    def user(self) -> UpperCaseLetter:
        return self._user

    @property
    def base(self) -> str:
        return f"{self._base:03d}"

    @property
    def suffix(self) -> str|None:
        return self._suffix

    @suffix.setter
    def suffix(self, other: int|str|None):
        if other:
            self._suffix = str(other)
        else:
            self._suffix = None

    @property
    def number(self) -> str:
        if self.suffix:
            return f"{self.base}-{self.suffix}"
        return self.base

    @classmethod
    def insert(cls, item: "Signature") -> "Signature":
        if not item.suffix:
            suf = "1"
        elif item.suffix[-1].isnumeric():
            suf = item.suffix + "a"
        else:
            suf = item.suffix + "1"
        new = Signature(item._suffix, item._user, item._base, suf)
        if not isinstance(new, Signature):
            raise RuntimeError()
        return new

    def next(self, lvmode: Literal['same', 'deeper', 'higher', 'base'] = 'same', steps: int = 1) -> "Signature|None":
        """Will provide the next Signature number.

        lvmode: str
            The level on which to count. For example '0000A001-1a2':
                "same"      :: 0000A001-1a3
                "deeper"    :: 0000A001-1a2a
                "higher"    :: 0000A001-1b
                "base"      :: 0000A002
        steps: int
            '0' provides itself. Does not provide negative integers yet.
        """
        item: Signature|None = self
        for s in range(steps):
            if item == None:
                return item
            item = item._next_one(lvmode)

    def _next_suffix(self, suf: str | None = None) -> str:
        if not suf:
            suf = self.suffix
        if not suf:
            return ""
        last_char: str = suf[-1]
        if last_char.isnumeric():
            new_last = str(int(last_char) + 1)
        else:
            new_last = chr(ord(last_char) + 1)

        if len(suf) == 1:
            return new_last
        return suf[-2] + new_last

    def _next_one(self, lvmode: str) -> "Signature|None":
        result: dict = {
            'serial': self._serial,
            'user': self._user,
            'base': self._base
        }
        match lvmode:
            case 'deeper':
                return Signature.insert(self)
            case 'higher':
                if not self.suffix:
                    return None
                elif len(self.suffix) == 1:
                    result['base'] = self._base + 1
                else:
                    result['suffix'] = self._next_suffix(self.suffix[:-2])
            case 'same':
                if self.base == '999':
                    return Signature.insert(self)
                elif not self._suffix:
                    result['base'] = self._base + 1
            case 'base':
                if self.base == '999':
                    return Signature.insert(self)
                result['base'] = self._base + 1
            case _:
                raise NameError(f"Invalid level mode {lvmode}")
        return safetype(Signature, Signature(
            result['serial'],
            result['user'],
            result['base'],
            result.get('suffix')
        ), filter = True, err = RuntimeError)

    def __str__(self) -> str:
        return f"{self.serial}{self.user}{self.base}{self.suffix}"

    @classmethod
    def isvalid(cls, arg, strict: bool = False) -> bool:
        if not strict:
            if cls._pttrn_full.search(arg):
                result = True
            elif cls._pttrn_short.search(arg):
                result = True
            else:
                result = False
        elif cls._pttrn_full.match(arg):
            result = True
        elif cls._pttrn_short.match(arg):
            result = True
        else:
            result = False
        return result
