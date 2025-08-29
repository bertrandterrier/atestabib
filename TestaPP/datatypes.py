from dataclasses import dataclass
import os
import pandas as pd
from pandas import DataFrame, Series
import pathlib
import re
from rich import print
from string import ascii_uppercase
from typing import Any, Iterable, Union, Literal, LiteralString, Pattern

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

        if inst.upper() == inst:
            inst.case = "upper"
        else:
            inst.case = "lower"
        return inst

    def upper(self) -> "Letter":
        if self.case == 'upper':
            return self
        return Letter(str(self).upper())

    def lower(self) -> "Letter":
        if self.case == 'lower':
            return self
        return Letter(str(self).lower())

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

class SignatureEntry:
    def __init__(
        self,
        letter: str|Letter,
        status: Literal['besetzt', 'reserviert', 'frei'] = 'frei',
        user: str | Literal['ANON'] | None = None,
        user_status: Literal['user', 'admin'] | None = None,
        route: str|list[str] = []
    ):
        self._letter: Letter = Letter(letter.upper())
        self._status: Literal['besetzt', 'reserviert', 'frei'] = status
        self._user: str | None = user
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

    @property
    def user(self) -> str|None:
        return self._user

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
    -> Nutzer für Signatur [yellow]{self.letter}[/yellow] ist bereits gesetzt.
        >> [green]{self.user}[/green]
    [red]-> Sitzende Nutzer können nicht überschrieben werden.[/red]
        => Ausnahme [green]ANON[/green]""")

class UserRegistry:
    """Holds dataframes for accredited users."""

    _seq: list = [Letter(l) for l in reversed(list(ascii_uppercase))]
    _names_de: list[str] = ['SIGNATUR', 'STATUS', 'NUTZER', 'NUTZERSTATUS', 'ROUTE']
    _names_en: list[str] = ['signature', 'status', 'user', 'user_status', 'route']

    def __init__(self, reg: PathStr|DataFrame):
        if isinstance(reg, DataFrame):
            self.df = reg.copy()
        else:
            self.df = pd.read_csv(reg)

        self.df.columns = UserRegistry._names_en          # Rename columns to english lower case names

        # Set DataTypes
        self.df = self._set_col_asletter(self.df.copy())
        for col in ['status', 'user_status']:
            self.df[col] = self.df[col].astype('category')

        self._reg: dict[str, SignatureEntry] = {}
        for i in range(self.df.shape[0]):
            status = self.df.iloc[i].status
            user = self.df.loc[i].user
            if not user and not self.df.loc[i].status == 'frei':
                user = "ANON"
        
            entry = SignatureEntry(
                letter = self.df.iloc[i].signature,
                status = status,
                user = user,
                user_status = self.df.iloc[i].user_status,
            )
            self._reg[str(entry.letter)] = entry

        for l in self._seq:
            if not str(l) in self._reg.keys():
                self._reg[str(l)] = SignatureEntry(letter = l, status = 'frei')

    def _get_single_routes(self, arg: str) -> list[str]:
        if not arg:
            return []
        if arg.startswith("\""):
            arg = arg[1:]
        if arg.endswith("\""):
            arg = arg[:-2]

        for sep in [';', ',']:
            if sep in arg:
                return [elem.strip() for elem in arg.split(sep)]
        return [arg]

    def _set_col_asletter(self, data: DataFrame) -> DataFrame:
        df = data.copy()
        df.signature = df['signature'].apply(Letter.safe_convert)
        df = df.dropna(subset = ['signature'])
        return df

    @property
    def data(self) -> dict[str, SignatureEntry]:
        return self._reg

    def __list__(self) -> list[SignatureEntry]:
        return [e for e in self._reg.values()]


    def asdict(self) -> dict:
        return {k: v for k, v in self._reg.items()}

    def isfree(self, arg: Letter|str) -> bool:
        if not isinstance(arg, Letter):
            arg = Letter(arg.upper())
        elif not arg.isupper():
            arg = arg.upper()


        

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
            'sequence': 'yellow',
            'user': 'red',
            'item': 'green',
            'suffix': 'cyan'
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
            'sequence': 'yellow',
            'user': 'red',
            'item': 'green',
            'suffix': 'cyan'
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
            v = f"[{colors[k]} italic]" + v + f"[/{colors[k]} italic]" + (name_len - len(v))*" " + ":: "
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
class Route:
    name: str
    short: str
    user: str|None = None

class Router:
    def __init__(
        self,
        log: PathStr,
        _entry_pttrn: Pattern | LiteralString = r"\{([^}]*)\}\{([^}]*)\}\{([^}]*)\};{0,1}"
    ):

        self._path: pathlib.Path = pathlib.Path(log)
        self._pttrn: Pattern|LiteralString = _entry_pttrn
        self._routes: list[Route] = []

    @property
    def routes(self) -> list[Route]:
        return self._routes

    def add_raw_entries(self, arg: str):
        entries = []
        for short, name, user in self.pttrn.findall(arg):
            if short and name:
                entries += [(short, name, user)]
        self.add_entries(*entries)

    def add_entries(self, *args: tuple[str, str, str]):
        for arg in args:
            if not arg[2]:
                user = "ANON"
            else:
                user = arg[2]
            entry = Route(
                name = arg[0],
                short = arg[1],
                user = user
            )
            self._routes.append(entry)
        
    @property
    def pttrn(self) -> Pattern:
        var = self._pttrn
        if not isinstance(var, Pattern):
            var = re.compile(var)
        return var

    @property
    def namelog(self) -> dict[str, dict]:
        result: dict[str, dict] = {}
        for r in self.routes:
            result[r.name] = {'short': r.short, 'user': r.user}
        return result

    @property
    def shorthandlog(self) -> dict[str, dict]:
        result: dict[str, dict] = {}
        for r in self.routes:
            result[r.short] = {'name': r.name, 'user': r.user}
        return result

    def find_short(self, shorthand: str) -> Route|None:
        for r in self.routes:
            if shorthand == r.short:
                return r
        return None

    def find_name(self, name: str, strict: bool = False) -> Route|None:
        for r in self.routes:
            if r.name == name:
                return r
        if not strict:
            for r in self.routes:
                if r.name.replace(" ", "").lower() == name.lower().replace(" ", ""):
                    return r
        return

    def find(self, arg: str, strict: bool = False) -> Route|None:
        var = self.find_short(arg)
        if not var:
            var = self.find_name(arg, strict)
        return var
