import typer
from typing import Optional
from typing_extensions import Annotated

from testapp import g_router
import testapp as ta

app = typer.Typer()

OPTS_AUTOCOMPLETE = {
    'scan': [ 'signature', 'index', 'id', 'name', 'address', '*' ],
    'show': [ 'locs', 'locations', 'items', 'routes', 'demands', '*' ],
}

def _autocomplete(ctx: typer.Context, args: list[str], incomplete: str):
    if len(args) < 1:
        return []

@app.command("inspect")
def inspect(
    signature: Annotated[Optional[str], typer.Argument(
        help = """The item signature. Format: \"0000A000\" or \"0000A000-1a23b\". If you are not sure about signature, use '--search' flag. If signature is not known, use 'search' command with '--inspect' flag. If signature stays empty, at least one segment has to be provided.""",
    )] = None,
    search: Annotated[Optional[bool], typer.Option(
        '-s', '--search',
        help = "Searches for similar or partly correct signatures. for more complex search use 'search' command."
    )] = False,
):
    pass

@app.command("test")
def test(arg: Annotated[Optional[str], typer.Argument()] = None):
    print("Dies ist ein Testbefehl.")
    if not arg:
        print("Hallo Welt!")
    else:
        print("Hallo", arg)

if __name__ == "__main__":
    app()
