from datetime import datetime as dt
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Literal

def mklogger(
    name: str,
    file: str|Path,
    level: int = logging.WARN,
    fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    dtsuffix: bool = True,
) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fpath = Path(file)
    suf = fpath.suffix
    fname = fpath.name.replace(suf, "")
    prefix = str(file).replace(fname, "")
    if dtsuffix:
        fname = fname + "_" + dt.now().strftime("%Y-%m-%d-%H-%M-%S")  

    fpath = Path(prefix).joinpath(fname + suf)
    count: int = 0
    while fpath.exists():
        count += 1
        if count == 1:
            fname = fname + "(1)"
        else:
            fname = fname[:-3] + f"({count})"
        fpath = Path(prefix).joinpath(fname + suf)

    file_handler = logging.FileHandler(fpath)
    file_handler.setLevel(level)
    
    formatter = logging.Formatter(fmt)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

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
