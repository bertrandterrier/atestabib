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

def safetype(
    _type: type,
    arg,
    filter: bool = False,
    mod: Literal['to_type', 'to_none']|type = 'to_type',
    err: type[Exception]|None = None
) -> Any:
    """Ensures to return a certain type be returned.

    _type: type
        The type or class.
    arg:
        The argument.
    filter: bool
        If arg list|tuple will only use first element.
        Defaults to False.
    mod: "to_type" | "to_none" | type
        If type not found will modify argument.
            "to_type": Calls an empty instance of _type.
            "to_none": Returns None.
        Any type provided will return an empty instance of that type.
    err: Exception | None 
        If an exception is provided, the safetype will raise it, if type not found.
    """
    if isinstance(arg, (list, tuple)) and filter:
        check = arg[0]
    else:
        check = arg

    if isinstance(check, _type):
        return check

    if isinstance(err, Exception):
        raise err
    elif mod == 'to_none':
        result = None
    elif isinstance(mod, type):
        result = mod(check)
    else:
        result = _type(check)
    return result
