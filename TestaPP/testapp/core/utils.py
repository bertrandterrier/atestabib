# TODO Has to be moved to more fitting place; like lib/
from typing import Any, Literal

SYNDICT: dict[str, list[str]] = {
    'key': ['schlüssel', 'schluessel', 'signatur', 'objektnummer', 'id'],
    'free': ['frei'],
    'occupied': ['besetzt'],
    'reserved': ['reserviert'],
    'user': ['nutzer'],
    'admin': ['administrator'],
    'lib': ['bib', 'bibliothek', 'library'],
}

TRNSLDICT: dict[str, dict[str, str]] = {
    'de': {},
    'en': {
        'user': 'Nutzer',
        'free': 'frei',
        'occupied': 'besetzt',
        'admin': 'Admin',
        'reserved': 'reserviert',
        'route': 'Route',
        'signature': 'Signatur',
        'key': 'Schluessel',
        'id': 'Kennnummer',
        'item': 'Objekt',
    },
}
for k, v in TRNSLDICT['en'].items():
    TRNSLDICT['de'][v] = k

def transl(
    arg: str,
    srclang: Literal['de', 'en']|None = None,
    default = None,
) -> str | Any:
    if srclang:
        return TRNSLDICT[srclang].get(arg, None)
    if arg in TRNSLDICT['de'].keys():
        return TRNSLDICT['de'][arg]
    elif arg in TRNSLDICT['en'].keys():
        return TRNSLDICT['en'][arg]
    return default

def de_en(arg: str, default = None) -> str | Any:
    return transl(arg, 'de', default)

def en_de(arg: str, default = None) -> str | Any:
    return transl(arg, 'en', default)

def syn(arg: str) -> str:
    check = arg.lower()
    if check in SYNDICT.keys():
        return check
    for key, scope in SYNDICT.items():
        if check in scope:
            return key
    return arg
