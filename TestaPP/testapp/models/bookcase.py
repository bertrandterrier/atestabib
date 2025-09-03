from dataclasses import dataclass
import re
from typing import Iterator, Literal, LiteralString, Pattern

@dataclass
class AddrData:
    country: str
    city: str
    street: str
    region: str|None = None
    postcode: int = -1

class BookCase:
    def __init__(
        self,
        num: int|float|str|tuple[int|str, int],
        loc0: AddrData|dict|tuple[float, float],
        loc1: AddrData|dict|tuple[float, float]|None = None,
    ):
        self._num: int = -1
        self._num_suf: str|None = None
        self._addr: AddrData|None = None
        self._geo: tuple[float, float]|None = None

        if isinstance(num, int):
            self._num = num
        elif isinstance(num, float):
            parts = str(num).split(".", 1)
            self._num = int(parts[0])
            self._num_suf = parts[1]
        elif isinstance(num, str):
            parts = re.match("([0-9]+)([a-z0-9]*)", num)
            if not parts:
                raise SyntaxError(f"Invalid number: {num}")
            self._num = int(parts[0])
            self._num_suf = parts[1]
        elif isinstance(num, tuple):
            self._num = int(num[0])
            self._num_suf = str(num[1])


        for loc in [loc0, loc1]:
            if isinstance(loc, AddrData):
                self._addr = loc
            elif isinstance(loc, tuple):
                self._geo = loc
            elif isinstance(loc, dict):
                if 'country' in loc.keys():
                    self._addr = AddrData(**loc)
                elif 'lat' in loc.keys():
                    self._geo = (loc['lat'], loc['long'])
                elif 'latitude' in loc.keys():
                    self._geo = (loc['latitude'], loc['longitude'])
                else:
                    raise KeyError("Expected address data dictionary, or dictionary with long+lat as keys.")
        @property
        def addresse(self) -> AddrData|None:
            return self._addr

        @property
        def gps(self) -> tuple[float, float]|None:
            return self._geo

        @property
        def latitude(self) -> float|None:
            if self.gps:
                return self.gps[0]
        @property
        def longitude(self) -> float|None:
            if not self.gps:
                return
            return self.gps[1]

        def loc(self, prec: Literal['gps', 'address'] = 'gps') -> tuple[AddrData|tuple[float|float]]:
            if prec == 'gps' and self.gps:
                return self.gps
            elif prec == 'address':
                return self.address
            elif self.address:
                return self.address
            return self.gps
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
