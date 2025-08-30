from dataclasses import dataclass
from pathlib import Path
import toml
from typing import Any

from datatypes import PathStr, RouteReg, UserReg

################################################################################ ROOT Path
G_ROOT: Path = Path(__file__).parent.parent
print(G_ROOT)

def root(*parts: PathStr) -> Path:
    return G_ROOT.joinpath(*parts)


################################################################################ CONFIG 
@dataclass
class RegPathsData:
    user: PathStr
    routes: PathStr

@dataclass
class ConfigData:
    regs: RegPathsData

_conf = Path(__file__).parent.parent.joinpath("docs", "config.toml")

with open(_conf, 'r') as f:
    _data: dict[str, Any] = toml.load(f)
_data_locs = _data['locs']

g_config = ConfigData(
    regs = RegPathsData(
        user = root(_data_locs['registries']['user']),
        routes = root(_data_locs['registries']['route'])
    )
)

################################################################################ ROUTE 
for reg in ['user', 'routes']:
    if not hasattr(g_config.regs, reg):
        raise FileNotFoundError(f"Missing registry path for \"{reg}\".")

g_router = RouteReg(g_config.regs.routes)

################################################################################ USER
g_admin: UserReg = UserReg(g_config.regs.user)
