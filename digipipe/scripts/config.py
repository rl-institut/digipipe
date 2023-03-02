"""
Helper functions for configs
"""

import os
from pathlib import Path

import yaml

from digipipe.store.utils import get_abs_store_root_path


def read_config(file: Path) -> dict:
    """Reads a yml config and returns as dict

    Parameters
    ----------
    file : str
        Full path to config file to read

    Returns
    -------
    dict
        Config dict
    """
    with open(file, "r") as cfg_file:
        try:
            cfg = yaml.safe_load(cfg_file) or {}
        except yaml.YAMLError as exc:
            print(f"Error while reading config file: {file}")
            print(exc)
    return cfg


def load_dataset_configs() -> dict:
    """Load datasets' yml configs and merge them using the directory tree for
    naming.

    Parameters
    ----------
    config_files : list of str
        List of paths to config files
    Returns
    -------
    dict
        Config dict of format:
        {"store":
            {"category":
                {"<DATASET_NAME>": {<CONTENT_OF_DATASET_CONFIG>}, ...}
            }
        }
    """

    def search_store_configs() -> list:
        """Search for configs (*.yml) in data store, exclude templates.

        Returns
        -------
        list
            Paths to config files
        """
        cfg_files = list()
        for root, dirs, files in os.walk(get_abs_store_root_path()):
            for file in files:
                if (file == "config.yml") and ".TEMPLATE" not in str(root):
                    cfg_files.append(Path(os.path.join(root, file)))
        return cfg_files

    merged_cfg = dict()
    for file in search_store_configs():
        path = Path(file).resolve()
        section = path.parent.parent.name
        subsection = path.parent.name
        cfg = read_config(file)
        if merged_cfg.get(section, None) is None:
            merged_cfg[section] = {}
        merged_cfg[section][subsection] = cfg
    return {"store": merged_cfg}
