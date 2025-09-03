from datetime import datetime
from dateutil import parser as dtparser
from typing import Any, Iterable, Literal

def issubset(subset: Iterable, superset: Iterable, empty_set_fail: bool = False) -> bool:
    """Checks if x is subset of y. True if all elements in x are elements of y."""
    child = [e for e in subset]
    par = [e for e in superset]

    if not child and empty_set_fail:
        return False
    for elem in child:
        if not elem in par:
            return False
    return True

def filter(
    src: Iterable,
    filter: Iterable,
    mode: Literal['pos', 'neg', '+', '-'] = 'pos'
) -> list:
    match mode:
        case '+'|'pos'|'positive':
            return [e for e in src if e in filter]
        case '-'|'neg'|'negative':
            return [e for e in src if e not in filter]

EN_DE: dict[str, str] = {
    'user': 'user',
    'member': 'Nutzer',
    'free': 'frei',
    'occupied': 'besetzt',
    'admin': 'Admin',
    'reserved': 'reserviert',
    'route': 'Route',
    'signature': 'Signatur',
    'id': 'Kennnummer',
    'item': 'Objekt',
    'library': 'Bibliothek',
    'lib': 'Bib',
    'bookcase': 'Bücherschrank',
    'address': 'Adresse',
    'location': 'Ort',
}
DE_EN: dict[str, str] = {}

for k, v in EN_DE.items():
    DE_EN[v] = k

def transl(
    arg: str,
    src_lang: Literal['de', 'en', 'german', 'english']|None = None,
    default = None,
) -> str | Any:
    result = None
    if src_lang:
        if src_lang.lower() in ['de', 'german']: 
            return DE_EN.get(arg, default)
        elif src_lang.lower().startswith('en'):
            return EN_DE.get(arg, default)
        elif src_lang:
            raise NameError(f"Invalid name \"{src_lang}\" for source language.")

    for src, mods in [
        (EN_DE, [str.lower]),
        (DE_EN, [str.title, str.lower])
    ]:
        for func in mods:
            result = src.get(func(arg))
            if result:
                return result
    return default

def de_en(word: str, default = None) -> str | Any:
    return transl(word, 'de', default)

def en_de(word: str, default = None) -> str | Any:
    return transl(word, 'en', default)

def timestamp(
    stamp: datetime|str|tuple[int, ...]|dict,
) -> datetime|None:
    if isinstance(stamp, datetime):
        return stamp
    if isinstance(stamp, str):
        return dtparser.parse(stamp)
    if isinstance(stamp, tuple):
        var = {}
        for i, key in enumerate(['year', 'month', 'day', 'hour', 'minute', 'second']):
            if i >= len(stamp):
                break
            var[key] = str(stamp[i])
        return datetime(**var)
    return datetime(**stamp)
