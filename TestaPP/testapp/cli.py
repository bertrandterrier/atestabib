import typer
from typing import Optional
from typing_extensions import Annotated

from testapp import g_router
from testapp.lib.utils import 

app = typer.Typer()

OPTS_AUTOCOMPLETE = {
    'scan': [ 'Signature', 'Route', 'Nutzer', 'Adresse' ]
}
def _auto_scan_arg(ctx: typer.Context, args: list[str], incomplete: str):
    if len(args) < 1:
        return []
    key = 
        return list(g_router)

@app.command("scan")
def scan(
    token: Annotated[str, typer.Argument(
        help = "Type token.",
        autocompletion = lambda: [],
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
