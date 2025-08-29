from dataclasses import dataclass
from pathlib import Path
import toml
from typing import Any

from datatypes import PathStr, Router

ROOT: Path = Path(__file__).parent.parent

@dataclass
class ConfigData:
    registries: dict[str, PathStr]
    logs: dict[str, PathStr]


with open('docs/config.py', 'r') as f:
    _data: dict[str, Any] = toml.load(f)

g_config = ConfigData(**_data)

for reg in ['user', 'routes']:
    if not g_config.registries.get(reg):
        raise FileNotFoundError(f"Missing registry path for \"{reg}\".")

g_router = Router(g_config.registries['routes'])
