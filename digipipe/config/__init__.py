import os
from pathlib import Path

from digipipe.scripts.config import read_config


def locate_global_config() -> Path:
    """Returns path to global config file.

    Raises error when executing the workflow not within `digipipe/` or
    `digipipe/workflow/`.
    """
    config_dir = Path("config", "global.yml")
    cwd = Path(os.getcwd())
    if cwd.name == "digipipe":
        return (cwd / config_dir).resolve()
    elif cwd.name == "workflow":
        return (cwd.parent / config_dir).resolve()
    else:
        raise FileNotFoundError(
            "Global config file not found, make sure you execute the workflow "
            "in digipipe/ or digipipe/workflow/ ."
        )


GLOBAL_CONFIG = {"global": read_config(locate_global_config())}
