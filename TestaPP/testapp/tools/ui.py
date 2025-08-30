MDFMT: dict[str, str] = {
    'int': 'deep_pink3',
    'str': 'green',
    'obj': 'yellow',
    'suf': 'deep_pink1',
}

def fmt(*opts, token: str) -> str:
    for opt in opts:
        if opt in MDFMT.keys():
            pre, suf = (f"[{MDFMT[opt]}]", f"[/{MDFMT[opt]}]")
        else:
            pre, suf = (f"[{opt}]", f"[/{opt}]")
        
