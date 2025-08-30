SYNONYMS: dict[str, list[str]] = {
    'key': ['schlüssel', 'schluessel', 'signatur', 'objektnummer', 'id'],
    'free': ['frei'],
    'occupied': ['besetzt'],
    'reserved': ['reserviert'],
    'user': ['nutzer'],
    'admin': ['administrator'],
    'lib': ['bib', 'bibliothek', 'library'],
}

def syn(arg: str) -> str:
    check = arg.lower()
    if check in SYNONYMS.keys():
        return check
    for key, scope in SYNONYMS.items():
        if check in scope:
            return key
    return arg
