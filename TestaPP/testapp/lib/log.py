from datetime import datetime as dt
import logging
from logging import Logger
from pathlib import Path

from testapp.lib.datatypes import PathStr

def mklogger(
    name: str,
    file: PathStr,
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
