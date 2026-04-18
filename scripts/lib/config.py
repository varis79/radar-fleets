"""Carga pipeline-config.yml con cache simple."""
from __future__ import annotations
import functools
import yaml

from .paths import CONFIG_FILE


@functools.lru_cache(maxsize=1)
def load_config() -> dict:
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def config() -> dict:
    """Alias corto."""
    return load_config()
