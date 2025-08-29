from rich import print
import typer
from typing import Optional
from typing_extensions import Annotated

import scanner
from datatypes import TestaBibID

app = typer.Typer()

@app.command("scan")
def scan(key: Annotated[str, typer.Argument(help = "Signatur (Alfred Testa Bibliotheks Objekt-Signatur)")]):
    rslt = scanner.scan(key)
    success: bool = rslt[0]

    if not success:
        print("[magenta bold]:: NEGATIV[/magenta bold]")
        print(f"[magenta] ->[/magenta] [green]{key}[/green]")
        print(f"[magenta] -> Keine valide Signatur der Alfred Testa Bibliothek.[/magenta]")
        print("\n> [bold]EBNF[/bold] Form: [yellow]4*Ziffer, LetterGross, 3*Ziffer, [[ \"-\", Ziffer { Ziffer|LetterKlein } ]][/yellow]")
        print("> [bold]REGEX[/bold] Form: [yellow]\\d{4}[[A-Z]]\\d{3}-{0,1}[[0-9]]*[[0-9a-z]]*")
    elif not isinstance(rslt[1], TestaBibID):
        print("[red bold]:: FEHLER\n -> RUNTIME ERROR[/red bold]")
        print(" [red]-> Something went wrong in parsing process.[/red]")
    else:
        token: TestaBibID = rslt[1]
        clrd = token.format(instant = False)
        print(f"\n\tObjekt: {token}")
        print("\n\tSchlüssel (Form): "+clrd)
        print("\n\tSchlüssel (Syntax):")
        for l in token.table():
            print("\t "+l[0]+l[1])
        print()

@app.command("what")
def what():
    print("what")

if __name__ == "__main__":
    app()
