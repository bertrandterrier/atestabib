from dataclasses import dataclass
import os
import pandas as pd
from pandas import DataFrame
import pathlib
import re
from rich import print
from string import ascii_uppercase
from typing import Any, Iterable, Iterator, Union, Literal, LiteralString, Pattern, NewType

CountryCode = NewType("CountryCode", str)
PathStr = Union[str, pathlib.Path, os.PathLike]

class Letter(str):
    """Letter ensures string of length 1. Use 'case' slot for checking upper/lower case letter. 'self.upper()' and 'self.lower()' methods will create new Letter instance, if not in correct case.
    """
    __slots__ = ("case", "body")

    def __new__(cls, token) -> "Letter":
        if len(str(token)) != 1:
            print("""[red bold]:: FEHLER[/red bold]
    [red]-> Syntaxfehler[/red]
    -> *class* [cyan]Letter[blue]([/blue]str[blue])[/blue][/cyan] expects *single* character.""")
            raise SyntaxError()
        inst = super().__new__(cls, str(token))
        inst.body = str(token)

        if token.upper() == token:
            inst.case = "upper"
        else:
            inst.case = "lower"
        return inst

    @classmethod
    def up(cls, other: "Letter|str") -> "Letter|str":
        if isinstance(other, Letter):
            if other.isupper():
                return other
            return cls(str(other).upper())
        if len(other) > 1:
            return other.upper()
        return cls(other.upper())

    @classmethod
    def low(cls, other: "Letter|str") -> "Letter|str":
        if isinstance(other, Letter):
            if other.islower():
                return other
            return cls(str(other).lower())
        if len(other) > 1:
            return other.lower()
        return cls(other.lower())

    def upper(self) -> "Letter":
        if not self.isupper():
            return Letter(str(self).upper())
        return self

    def lower(self) -> "Letter":
        if not self.islower():
            return Letter(str(self).lower())
        return self

    def __str__(self) -> str:
        return self.body

    def __eq__(self, other) -> bool:
        result = False
        if isinstance(other, str):
            if len(other) == 1:
                other = Letter(other)
        if isinstance(other, Letter):
            if other.body == self.body and other.case == self.case:
                result = True
        return result

    def __gt__(self, other) -> bool:
        if not isinstance(other, (str)):
            return False
        if not len(other) == 1:
            return False
        o = Letter(other)
        if self.case == o.case:
            return ord(self.body) > ord(o.body)
        elif self.case == 'upper':
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
    def safe_convert(cls, token) -> "Letter|None":
        try:
            return cls.__new__(cls, token)
        except:
            return None

class UserData:
    def __init__(
        self,
        letter: str|Letter,
        status: Literal['besetzt', 'reserviert', 'frei'] = 'frei',
        name: str | Literal['ANON'] | None = None,
        user_status: Literal['user', 'admin'] | None = None,
        route: str|list[str] = []
    ):
        self._letter: Letter = Letter(letter.upper())
        self._status: Literal['besetzt', 'reserviert', 'frei'] = status
        self._name: str | None = name 
        self._user_status: Literal['admin', 'user'] | None = user_status
        self._route: list[str] = []

        if isinstance(route, str):
            self._route = [e.strip() for e in route.split(";")]
        else:
            self._route = [e for e in route]

    @property
    def status(self) -> str:
        return self._status

    def isfree(self) -> bool:
        return self.status == 'frei'

    def isused(self) -> bool:
        return self.status != 'frei'

    def __bool__(self) -> bool:
        if self.status != 'frei':
            return True
        return False

    def __str__(self) -> str:
        return self.name or "<ANON>"

    def __lttr__(self) -> Letter:
        return self.letter

    @property
    def name(self) -> str|None:
        return self._name

    @property
    def letter(self) -> Letter:
        return self._letter

    @property
    def route(self) -> str|list[str]|None:
        if len(self._route) <= 0:
            return
        elif len(self._route) == 1:
            return self._route[0]
        return self._route

    @user.setter
    def user(self, name: str):
        if name.lower() in ['kusanowsky', 'klaus kusanowsky', 'kk']:
            self._user_status = 'admin'
            self._user = name
            self._status = 'besetzt'
        elif not self._user or str(self._user).upper().startswith("ANON"):
            self._user = name
            self._status = 'besetzt'
            self._user_status = 'user'
        else:
            print(f"""[red][bold]:: VERBOTEN[/bold][/red]
    -> Konnte [green]{name}[/green] nicht anwenden.
    -> Nutzer für Signatur [bright_yellow]{self.letter}[/bright_yellow] ist bereits gesetzt.
        >> [green]{self.user}[/green]
    [red]-> Sitzende Nutzer können nicht überschrieben werden.[/red]
        => Ausnahme [green]ANON[/green]""")

class UserReg:
    """Holds dataframes for accredited users."""

    _seq: list = [Letter(l) for l in reversed(list(ascii_uppercase))]
    _names_de: list[str] = ['SIGNATUR', 'STATUS', 'NUTZER', 'NUTZERSTATUS', 'ROUTE']
    _names_en: list[str] = ['signature', 'status', 'user', 'user_status', 'route']

    def __init__(self, reg: PathStr|DataFrame):
        if isinstance(reg, DataFrame):
            self.df = reg.copy()
        else:
            self.df = pd.read_csv(reg)

        self.df.columns = UserReg._names_en          # Rename columns to english lower case names

        # Set DataTypes
        self.df = self._set_col_asletter(self.df.copy())
        for col in ['status', 'user_status']:
            self.df[col] = self.df[col].astype('category')

        self._reg: dict[Letter, UserData] = {}
        for i in range(self.df.shape[0]):
            status = self.df.iloc[i].status
            user = self.df.loc[i].user
            if not user and not self.df.loc[i].status == 'frei':
                user = "ANON"
        
            entry = UserData(
                letter = self.df.iloc[i].signature,
                status = status,
                name = user,
                user_status = self.df.iloc[i].user_status,
            )
            self._reg[entry.letter] = entry

        for l in self._seq:
            if not str(l) in self._reg.keys():
                self._reg[l] = UserData(letter = l, status = 'frei')

    def _set_col_asletter(self, data: DataFrame) -> DataFrame:
        df = data.copy()
        df.signature = df['signature'].apply(Letter.safe_convert)
        df = df.dropna(subset = ['signature'])
        return df

    def __getattribute__(self, name: str) -> UserData:
        if name.upper() not in [str(l) for l in self._seq]:
            raise AttributeError(f"Unknwon attribute {name}")
        try:
            l = Letter(name.upper())
            return self.data[l]
        except:
            raise AttributeError()

    @property
    def data(self) -> dict[Letter, UserData]:
        return self._reg

    def __iter__(self) -> Iterator:
        for usr in self.data.values():
            yield(usr)

    def get(self, arg: str|Letter, default: Any = None) -> UserData|Any:
        if not isinstance(arg, Letter) and len(arg) == 1:
            try:
                arg = Letter(arg.upper())
            except:
                pass
        if isinstance(arg, Letter):
            return self.data[arg.upper()]

        for usr in self.data.values():
            if (usr.name or "ANON").lower() == arg.lower():
                return usr
        return default

        

class TestaBibID:
    def __init__(self, sequence: str|int, user: str, item: str|int, suffix: str|int|None):
        self._seq: int = int(sequence)
        self._user: str = user.lower()
        self._item: int = -1
        self._suffix: str|None = str(suffix)

        if suffix:
            self._item = int(item)
            self._suffix = str(suffix)
        elif isinstance(item, int):
            self._item = item
            self._suffix = None
        else:
            if "-" in item:
                self._item = int(item.split("-", 1)[0])
                self._suffix = item.split("-", 1)[1]
            else:
                self._item = int(item)
            
    @property
    def sequence(self) -> str:
        return f"{self._seq:04d}"

    @property
    def seq(self) -> str:
        return f"{self._seq:04d}"

    @property
    def user(self) -> str:
        return f"{self._user.upper()}"

    @property
    def item(self) -> str:
        return f"{self._item:03d}"

    @property
    def suffix(self) -> str:
        if not self._suffix:
            return ""
        return f"{self._suffix}"

    def __str__(self) -> str:
        if not self._suffix:
            suf = ""
        else:
            suf = f"-{self._suffix}"
        return f"{self.seq}{self.user}{self.item}{suf}"

    def __add__(self) -> "TestaBibID":
        if self._suffix:
            if len(self._suffix) == 1:
                if self._suffix.isnumeric():
                    suffix = str(int(self._suffix) + 1)
                else:
                    suffix = chr(ord(self._suffix) + 1)
            else:
                lchar: str = self._suffix[-1]
                suffix = self._suffix[:-2]
                if lchar.isnumeric():
                    suffix += str(int(lchar) + 1)
                else:
                    suffix += chr(ord(lchar) + 1)
            item = self._item
        else:
            item, suffix = (self._item + 1, None)
        return TestaBibID(self.seq, self.user, item, suffix)

    def format(
        self,
        colors: dict[str, str] = {
            'sequence': 'deep_pink1',
            'user': 'bright_yellow',
            'item': 'deep_pink1',
            'suffix': 'green'
            }, instant: bool = False) -> str:
        clrs: dict[str, tuple[str, str]] = {k: (f"[{v}]", f"[/{v}]") for k, v in colors.items()}

        seq = f"{clrs['sequence'][0]}{{{self.sequence}}}{clrs['sequence'][1]}"
        usr = f"{clrs['user'][0]}{{{self.user}}}{clrs['user'][1]}"
        itm = f"{clrs['item'][0]}{{{self.item}}}{clrs['item'][1]}"
        if self._suffix:
            suf = f" {clrs['suffix'][0]}{{{self.suffix}}}{clrs['suffix'][1]}"
        else:
            suf = ""
        result = f"{seq} {usr} {itm}" + suf
        if instant:
            print(result)
        return result

    def table(
        self,
        colors: dict[str, str] = {
            'sequence': 'deep_pink1',
            'user': 'bright_yellow',
            'item': 'deep_pink1',
            'suffix': 'sea_green3'
        },
        names: dict[str, str] = {
            'sequence': 'Serie',
            'user': 'Nutzer',
            'item': 'Objektnummer',
            'suffix': 'Obj.-Suffix'
        },
        instant: bool = False
    ) -> list[tuple[str,str]]:
        clrs: dict[str, tuple[str, str]] = {k: (f"[{v}]", f"[/{v}]") for k, v in colors.items()}

        name_len = 0
        for v in names.values():
            if len(v) >= name_len:
                name_len = len(v) + 1
        pnames: dict[str, str] = {}
        for k, v in names.items():
            v = v + (name_len - len(v))*" " + ":: "
            pnames[k] = v

        seq = f"{clrs['sequence'][0]}{self.sequence}{clrs['sequence'][1]}"
        usr = f"{clrs['user'][0]}{self.user}{clrs['user'][1]}"
        itm = f"{clrs['item'][0]}{self.item}{clrs['item'][1]}"
        if self._suffix:
            suf = f"{clrs['suffix'][0]}{self.suffix}{clrs['suffix'][1]}"
        else:
            suf = ""

        result = [
            (pnames['sequence'], seq),
            (pnames['user'], usr),
            (pnames['item'], itm),
        ]
        if len(suf) >= 1:
            result.append((pnames['suffix'], suf))
        if instant:
            for l in result:
                print(l[0]+l[1])
        return result

    def insert(self) -> "TestaBibID":
        if self._suffix:
            if str(self._suffix[-1]).isnumeric():
                suffix = f"{self._suffix}a"
            else:
                suffix = f"{self._suffix}1"
        else:
            suffix = "1"
        return TestaBibID(self._seq, self._user, self._item, suffix)

class ItemData:
    def __init__(
        self,
        id: TestaBibID,
        name: str,
        year: int|str|None = None,
        author: str|list[str] = [],
        editor: str|list[str] = [],
        title: str|None = None,
        shorthand: str|None = None,
        subtitle: str|None = None,
        isbn: int|tuple|str|None = None,
        isbn13: int|Iterable[int]|str|None = None,
        isbn10: int|Iterable[int]|str|None = None,
    ):
        self.__id: TestaBibID = id
        self._ttl: tuple[str, str|None]= (title or name, subtitle)
        self._shorthand: str|None = shorthand
        self._year: str|int|None = year
        self._ed: list[str] = []
        self._author: list[str] = []
        self._isbn: int = -1
        self._isbn10: int = -1
        self._isbn13: int = -1

        self.author = author
        self.editor = editor

        for num, _type in zip([isbn, isbn10, isbn13], [None, 10, 13]):
            if num:
                self.scan_isbn(num, _type)

    @property
    def subtitle(self) -> str|None:
        return self._ttl[1]

    @property
    def title(self) -> str:
        return self._ttl[0]

    @title.setter
    def title(self, other: tuple[str, str]|str):
        if isinstance(other, tuple):
            self._ttl = other
        else:
            self._ttl = (other, self._ttl[1])

    @subtitle.setter
    def subtitle(self, other: str):
        self._ttl = (self.title, other)

    @property
    def author(self) -> str|list[str]|None:
        if len(self._author) < 1:
            return
        elif len(self._author) ==1:
            return self._author[0]
        return self._author

    @author.setter
    def author(self, other: str|list[str]):
        if isinstance(other, str):
            self._author.append(other)
        else:
            self._author += other


    @property
    def editor(self) -> str|list[str]|None:
        if len(self._ed) < 1:
            return
        elif len(self._ed) ==1:
            return self._ed[0]
        return self._ed

    @editor.setter
    def editor(self, other: str|list[str]):
        if isinstance(other, str):
            self._ed.append(other)
        else:
            self._ed+= other

    def scan_isbn(self, isbn: str|int|Iterable[int], isbn_type: int|None = None):
        if isinstance(isbn, str):
            if not isbn.replace("-", "").replace(" ", "").isnumeric():
                raise SyntaxError(f"Invalid ISBN: \"{isbn}\"")
            num = int(isbn.replace("-", "").replace(" ", ""))
        elif isinstance(isbn, Iterable):
            var = "".join([str(p) for p in isbn])
            if not var.isnumeric():
                raise SyntaxError(f"Invalid ISBN: None numerical.")
            num = int(var)
        else:
            num = isbn

        if isbn_type == 13 or len(str(num)) == 13:
            if not len(str(num)) == 13:
                raise SyntaxError(f"Expects 13 digits for ISBN-13. Got {len(str(num))}")
            self._isbn13 = num
            self._isbn = num
        elif isbn_type == 10 or len(str(num)) == 10:
            if not len(str(num)) == 10:
                raise SyntaxError(f"Expects 10 digits for ISBN-10. Got {len(str(num))}")
            self._isbn10 = num
            if not self._isbn13:
                self._isbn = num
        else:
            raise ValueError(f"Invalid ISBN type \"{isbn_type}\"")

    @property
    def isbn13(self) -> int|None:
        if self._isbn13 <= 0:
            return
        return self._isbn13

    @property
    def isbn10(self) -> int|None:
        if self._isbn10 <= 0:
            return
        return self._isbn10
    
    @property
    def signatur(self) -> TestaBibID:
        return self.__id

@dataclass
class AddrData:
    country: str|CountryCode
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

class RouteData:
    def __init__(
        self,
        acronym: str,
        name: str,
        *locs: AddrData|dict,
        user: UserData|None = None,
        alt_names: list[str] = [],
    ):
        self._short: str = acronym.replace("#", "")
        self._names: list[str] = [name] + [n for n in alt_names]
        self._user: None|UserData = user
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
        self._routes: list[RouteData] = []

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
                        RouteData(match[0], name, user = match[2], alt_names = names)
                    )
                else:
                    self._routes.append(
                        RouteData(match[0], name, alt_names = names)
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
    def routes(self) -> list[dict]:
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
class LocAddr:
    route: RouteData
    number: int
    number_suffix: str|None = None
