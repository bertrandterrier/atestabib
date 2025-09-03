from dataclasses import dataclass
import logging
import os
from pathlib import Path
import toml
from typing import Any

from testapp.lib.log import mklogger
from testapp.models.bookcase import RouteReg
from testapp.models.datatypes import PathStr
from testapp.models.member import *

################################################################################ ROOT Path
G_ROOT: Path = Path(__file__).parent.parent
print(G_ROOT)

def root(*parts) -> Path:
    return G_ROOT.joinpath(*parts)


################################################################################ CONFIG 
@dataclass
class RegPathsData:
    user: PathStr
    routes: PathStr

@dataclass
class ConfigData:
    regs: RegPathsData
    log_dir: PathStr

_conf = Path(__file__).parent.parent.joinpath("docs", "config.toml")

with open(_conf, 'r') as f:
    _data: dict[str, Any] = toml.load(f)
_data_locs = _data['locs']

g_config = ConfigData(
    regs = RegPathsData(
        user = root(_data_locs['registries']['user']),
        routes = root(_data_locs['registries']['route'])
    ),
    log_dir = _data_locs['logs']
)

################################################################################ LOGGER
LOGLEVEL = logging.DEBUG

_log_file = Path(
    os.path.expandvars(g_config.log_dir)
).joinpath("run_.log")
g_logger = mklogger("TestaPP Logger", _log_file, LOGLEVEL)

################################################################################ ROUTE 
for reg in ['user', 'routes']:
    if not hasattr(g_config.regs, reg):
        raise FileNotFoundError(f"Missing registry path for \"{reg}\".")

g_router = RouteReg(g_config.regs.routes)

################################################################################ USER
g_admin: MemberReg = MemberReg(g_config.regs.user)
