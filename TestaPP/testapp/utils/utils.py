from typing import Any, Literal

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

def tl_de_en(word: str, default = None) -> str | Any:
    return transl(word, 'de', default)

def tl_en_de(word: str, default = None) -> str | Any:
    return transl(word, 'en', default)
