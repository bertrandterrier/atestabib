from dataclasses import dataclass
from pathlib import Path
import toml
from typing import Any

from datatypes import PathStr, Router

ROOT: Path = Path(__file__).parent.parent
print(ROOT)

@dataclass
class RegPathsData:
    user: PathStr
    routes: PathStr

@dataclass
class ConfigData:
    regs: RegPathsData

with open('docs/config.toml', 'r') as f:
    _data: dict[str, Any] = toml.load(f)

g_config = ConfigData(
    regs = RegPathsData(
        user = ROOT.joinpath(_data['registries']['user']),
        routes = ROOT.joinpath(_data['registries']['routes']),
    )
)

for reg in ['user', 'routes']:
    if not hasattr(g_config.regs, reg):
        raise FileNotFoundError(f"Missing registry path for \"{reg}\".")

g_router = Router(g_config.regs.routes)
