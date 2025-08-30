from typing import Literal

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
    },
}
for k, v in TRNSLDICT['en'].items():
    TRNSLDICT['de'][v] = k

def transl(
    arg: str,
    _from: Literal['de', 'en']|None = None,
) -> str | None:
    if _from:
        return TRNSLDICT[_from].get(arg, None)
    if arg in TRNSLDICT['de'].keys():
        return TRNSLDICT['de'][arg]
    elif arg in TRNSLDICT['en'].keys():
        return TRNSLDICT['en'][arg]
    return

def de_en(arg: str) -> str | None:
    return transl(arg, 'de')

def en_de(arg: str) -> str | None:
    return transl(arg, 'en')

def syn(arg: str) -> str:
    check = arg.lower()
    if check in SYNDICT.keys():
        return check
    for key, scope in SYNDICT.items():
        if check in scope:
            return key
    return arg
