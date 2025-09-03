from pandas import DataFrame
from typing import Literal

from testapp.data.datatypes import Letter, PathStr, UpperCaseLetter

class MemberData:
    def __init__(
        self,
        key: Letter|UpperCaseLetter,
        status: Literal['besetzt', 'reserviert', 'frei'] = 'frei',
        name: str | Literal['ANON'] | None = None,
        user_status: Literal['user', 'admin'] | None = None,
        route: str|list[str] = []
    ):
        self._letter: UpperCaseLetter = UpperCaseLetter(key)
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

    @property
    def signature(self) -> UpperCaseLetter:
        return self._letter

    @signature.setter
    def user(self, lttr: str):
        if not isinstance(lttr, Letter):
            UpperCaseLetter(lttr)
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

        self._reg: dict[Letter, MemberData] = {}
        for i in range(self.df.shape[0]):
            status = self.df.iloc[i].status
            user = self.df.loc[i].user
            if not user and not self.df.loc[i].status == 'frei':
                user = "ANON"
        
            entry = MemberData(
                key = self.df.iloc[i].signature,
                status = status,
                name = user,
                user_status = self.df.iloc[i].user_status,
            )
            self._reg[entry.letter] = entry

        for l in self._seq:
            if not str(l) in self._reg.keys():
                self._reg[l] = MemberData(key = l, status = 'frei')

    def _set_col_asletter(self, data: DataFrame) -> DataFrame:
        df = data.copy()
        df.signature = df['signature'].apply(Letter.safe_convert)
        df = df.dropna(subset = ['signature'])
        return df

    def __getattribute__(self, name: str) -> MemberData:
        if name.upper() not in [str(l) for l in self._seq]:
            raise AttributeError(f"Unknwon attribute {name}")
        try:
            l = Letter(name.upper())
            return self.data[l]
        except:
            raise AttributeError()

    @property
    def data(self) -> dict[Letter, MemberData]:
        return self._reg

    def __iter__(self) -> Iterator:
        for usr in self.data.values():
            yield(usr)

    def get(self, arg: str|Letter, default: Any = None) -> MemberData|Any:
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

class MemberReg:
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

        self._reg: dict[Letter, MemberData] = {}
        for i in range(self.df.shape[0]):
            status = self.df.iloc[i].status
            user = self.df.loc[i].user
            if not user and not self.df.loc[i].status == 'frei':
                user = "ANON"
        
            entry = MemberData(
                key = self.df.iloc[i].signature,
                status = status,
                name = user,
                user_status = self.df.iloc[i].user_status,
            )
            self._reg[entry.letter] = entry

        for l in self._seq:
            if not str(l) in self._reg.keys():
                self._reg[l] = MemberData(key = l, status = 'frei')

    def _set_col_asletter(self, data: DataFrame) -> DataFrame:
        df = data.copy()
        df.signature = df['signature'].apply(Letter.safe_convert)
        df = df.dropna(subset = ['signature'])
        return df

    def __getattribute__(self, name: str) -> MemberData:
        if name.upper() not in [str(l) for l in self._seq]:
            raise AttributeError(f"Unknwon attribute {name}")
        try:
            l = Letter(name.upper())
            return self.data[l]
        except:
            raise AttributeError()

    @property
    def data(self) -> dict[Letter, MemberData]:
        return self._reg

    def __iter__(self) -> Iterator:
        for usr in self.data.values():
            yield(usr)

    def get(self, arg: str|Letter, default: Any = None) -> MemberData|Any:
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

