import typer
from typing import Optional
from typing_extensions import Annotated

import testapp as ta
from testapp.data import g_admin, g_router
from testapp.data.items import TestaBibID
from testapp.lib import FormatPrinter as print

app = typer.Typer()

def scan_key(key: str):
    rslt = ta.fn.scanner.scan_key(key)
    success: bool = rslt[0]

    if not success:
        print(":: GESCHEITERT", 'b', 'err')
        print(f"  -> {ta.ui.rstyle(key, '')}")
        print(ta.ui.rstyle(f"  -> Keine valide Signatur der Alfred Testa Bibliothek.[/magenta]"))
        print("\n> [bold]EBNF[/bold] Form: [yellow]4*Ziffer, LetterGross, 3*Ziffer, [[ \"-\", Ziffer { Ziffer|LetterKlein } ]][/yellow]")
        print("> [bold]REGEX[/bold] Form: [yellow]\\d{4}[[A-Z]]\\d{3}-{0,1}[[0-9]]*[[0-9a-z]]*")
    elif not isinstance(rslt[1], TestaBibID):
        print("[red bold]:: FEHLER\n -> RUNTIME ERROR[/red bold]")
        print(" [red]-> Something went wrong in parsing process.[/red]")
    else:
        token: TestaBibID = rslt[1]
        clrd = token.format(instant = False)
        print(f"\n\tObjekt: [bold][yellow]{token}[/yellow][/bold]")
        print("\n\tSchlüssel (Form): "+clrd)
        print("\n\tSchlüssel (Syntax):")
        for l in token.table():
            print("\t "+l[0]+l[1])
        print()

def scan_user(token: str):
    result = g_admin.get(token)
    if result == None:
        ta.ui.
    return

_auto_scan_opts = [ 'item', 'route', 'user' ]
def _auto_scan_arg(ctx: typer.Context, args: list[str], incomplete: str):
    if len(args) < 1:
        return []
    if ta.fn.de_en(args[0], "").startswith('route'):
        return list(g_router)

@app.command("scan")
def scan(
    token: Annotated[str, typer.Argument(
        help = "[yellow]Scan-Token / Scanmodus[/yellow].",
        autocompletion = lambda: [ta.fn.en_de(e) for e in _auto_scan_opts],
    )],
    args: Annotated[Optional[list[str]], typer.Argument(
        help = "[yellow]Token Argument[/yellow]. Argument[italic]typ[/italic] abhängig vom [yellow]Scan-Token [italic]⟨token⟩[/italic][/yellow].",
        autocompletion = _auto_scan_arg,
    )] = None,
):
    token = ta.fn.de_en(token)

    if not args:
        raise RuntimeError("Mode help not yet implemented.")
        # TODO: MODE HELP

    if isinstance(args, str):
        args = [args]

    match token:
        case 'item':
            for arg in args:
                scan_key(arg)
        case 'user':
            for arg in args:
                #scan_user(arg)
                continue
        case 'route':
            pass
            # TODO Route scan

@app.command("test")
def test(arg: Annotated[Optional[str], typer.Argument()] = None):
    print("Dies ist ein Testbefehl.")
    if not arg:
        print("Hallo Welt!")
    else:
        print("Hallo", arg)

if __name__ == "__main__":
    app()
