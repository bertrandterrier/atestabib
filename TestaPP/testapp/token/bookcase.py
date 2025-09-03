from dataclasses import dataclass
from datetime import datetime as dt
import re
from typing import Iterator, Literal, LiteralString, Pattern

from testapp.lib.datatypes import TimeStamp, Letter, PathStr


@dataclass
class AddrData:
    country: str
    city: str
    postcode: int|str|None = None
    region: str|None = None
    street: str|tuple[str, int]|None = None

@dataclass
class MapData:
    _type: Literal['text', 'img', 'link', 'file']
    source: str|bytes|PathStr
    label: str|None = None
    outdated: bool = False

class BookCase:
    def __init__(
        self,
        active: bool,
        *locs: MapData,
        discovery: Literal['new']|TimeStamp = 'new',
        visits: list[TimeStamp] = [],
        comments: list[tuple[Literal['*']|TimeStamp, str]],
        **states,
    ):
        self._active: bool = active
        self._addr: AddrData|None = None
        self._gps: tuple[float, float]|None = None
        self._maps: list[MapData] = []

        self._states: dict = { k: v for k, v in states.items()}



class Route:
    def __init__(
        self,
        acronym: str,
        name: str,
        *locs: AddrData|dict,
        user: MemberData|None = None,
        alt_names: list[str] = [],
    ):
        self._short: str = acronym.replace("#", "")
        self._names: list[str] = [name] + [n for n in alt_names]
        self._user: None|MemberData = user
        self._locs: dict[str, AddrData] = {}

        for l in locs:
            if not isinstance(l, AddrData):
                l = AddrData(**l)

    @property
    def name(self) -> str:
        return self._names[0]
    @name.setter
    def name(self, token: str|int, del_first: bool = False):
        if isinstance(token, str):
            new = token
        elif not token < len(self._names):
            return
        else:
            new = self._names[token]
            del self._names[token]
        if del_first:
            self._names[0] = new
        else:
            self._names = [new] + [n for n in self._names]
        return

class RouteReg:
    def __init__(
        self,
        log: PathStr,
        _entry_pttrn: Pattern | LiteralString = r"^([^;]+);*$",
        _field_pttrn: Pattern | LiteralString = r"\{([^}]+)\}"
    ):
        self._pttrn: dict[Literal['field', 'entry'], LiteralString|Pattern] = {
            'entry': _entry_pttrn,
            'field': _field_pttrn
        }
        self._routes: list[Route] = []

        with open(log, 'r') as f:
            raw = f.read()
        for entry in self.pattern('entry').findall(raw):
            if not entry:
                continue
            match = self.pattern('field').findall(entry)

            if len(match) >= 2:
                name, names = RouteReg.split_routes(match[1])
                if len(match) >= 3:
                    self._routes.append(
                        Route(match[0], name, user = match[2], alt_names = names)
                    )
                else:
                    self._routes.append(
                        Route(match[0], name, alt_names = names)
                    )
            else:
                print(f"""[red][bold]:: FEHLER[/bold]
    -> Syntaxfehler[/red]
    -> Min. []""")


    @classmethod
    def split_routes(cls, route) -> tuple[str, list[str]]:
        result: list[str] = []
        if "\"" in route:
            for r in re.findall(r'"[^"]+?"', route):
                result.append(r)
        elif ";" in route:
            for r in re.findall(r"[^ ][^;]+", route):
                result.append(r)
        elif " " in route:
            for r in re.findall(r"[^ ]+", route):
                result.append(r)
        if len(result) <= 0:
            return route, []
        elif len(result) == 1:
            return result[0], []
        else:
            return result[0], result[1:]

    @property
    def routes(self) -> list[Route]:
        return self._routes

    def __iter__(self) -> Iterator:
        for r in self.routes:
            yield r

    def pattern(self, which: Literal['field', 'entry']) -> Pattern:
        pttrn = self._pttrn[which]
        if not isinstance(pttrn, Pattern):
            return re.compile(pttrn)
        return pttrn

@dataclass
class BookCaseAddr:
    routes: Route|list[Route]
    number: int
    number_suffix: str|None = None
