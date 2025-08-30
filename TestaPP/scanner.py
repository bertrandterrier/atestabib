from rich import print
import re
from string import ascii_uppercase, digits, ascii_lowercase
import sys
from typing import Pattern

from datatypes import TestaBibID, Route

PTTRN: dict[str, Pattern] = {
    'valid.0': re.compile(r"^(\d{4})([A-Z]{1})(\d{3})$"),
    'valid.1': re.compile(r"^[0-9a-z]+"),
    'numtpl': re.compile(r"[0-9]+"),
    'lttrtpl': re.compile(r"[a-z]+"),
    'tag.0': re.compile(r"#([^ ]+?)(\d{4}[a-zA-Z]\d{3})"),
    'tag.1': re.compile(r"#([^ ]+?)(\d{4}[a-zA-Z]\d{3}-[0-9][a-zA-Z0-9]*)")
}

def scan_key(token: str) -> tuple[bool, str|TestaBibID]:
    key = token.replace(" ", "")
    suffix = ""
    if "-" in key:
        key, suffix = key.split("-", 1)
        if not PTTRN['valid.1'].match(suffix):
            if PTTRN['valid.1'].match(suffix.lower()):
                print(f"""[orange bold]:: VORSICHT![/orange bold]
    -> [cyan]Objektnummern-Suffix[/cyan] mit Kleinbuchstaben!
:: Verwende Gruppe [green]{ascii_lowercase}[/green]
    -> Mache weiter mit [yellow]{suffix.lower()}[/yellow]""")
                suffix = suffix.lower()
            else:
                print(f"""[red bold]:: FEHLER![/red bold]
    [red]-> Syntaxfehler für Objektnummern-Suffix[/red] [yellow]\"{suffix}\"[/yellow].""")
                response = ""
                while not response.lower() in ['j', 'y', 'yes', 'ja', 'ok', 'nein', 'no', 'nope', 'n']:
                    response = input("[magenta]>> Suffix verwerfen und mit Schlüsselanalyse fortfahren? [j/N]: [/magenta]")
                if response.lower().startswith('n'):
                    print(":: ABBRUCH")
                    return False, token
                else:
                    suffix = ""
    item, user, serial = ("", "", "")
    if not len(key) == 8:
        print(f"""[red bold]:: FEHLER[/red bold]
    [red]-> Syntaxfehler[/red]
    [red]-> Falsche Länge.[/red]
    -> [magenta]8[/magenta] Stellen erwartet, [magenta]{len(key)}[/magenta] Stellen gefunden.
:: ABBRUCH""")
        return False, key
    serial, user, item = (key[:4], key[4], key[5:])
    if not serial.isnumeric():
        try:
            serial = str(int(serial))
        except:
            print(f"""[red bold]:: FEHLER[/red bold]
    -> Für SERIE [magenta]4[/magenta] [italic]Ziffern[/italic] erwartet.
    -> Fand [yellow]{serial}[/yellow].
:: ABBRUCH""")
            sys.exit(4)
    if not user in ascii_uppercase:
        if user in ascii_lowercase:
            print(f"""[orange bold]:: VORSICHT![/orange bold]
    -> [cyan]Nutzersignatur[/cyan] in Großbuchstaben.
    -> Verwende aus [green]{ascii_uppercase}[/green]
    -> Formatiere und nutze [yellow]{user.upper()}[/yellow]..
    """)
            user = user.upper()
        elif user in digits:
            print(f""":: FEHLER!
    -> Syntax Fehler.
    -> Nutzersignatur [A-Z] erwartet.""")
            return False, token
        else:
            print(f""":: FEHLER!
    -> Syntax Fehler.
    -> Unbekannt. Unerlaubtes Zeichen.
    -> Nutze aus:\n\t{ascii_uppercase}""")
            return False, token
    if not re.match(r"[0-9]{3}", item):
        print(f""":: FEHLER
    -> Syntax Fehler. 
    -> 3 Ziffern erwartet. Nicht \"{item}\".""")
        return False, token 

    return True, TestaBibID(serial, user, item, suffix)
