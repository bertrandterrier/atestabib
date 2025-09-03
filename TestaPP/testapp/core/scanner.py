from testapp.data.bibtypes import *
from testapp.data import item

def scan(arg, get_all: bool) -> TokenType|list[TokenType]|None:
    result = None
    if item.Signature.isvalid(arg):
        result = item.Signature(arg)
    return result
