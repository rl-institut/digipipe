"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.scripts.config import load_dataset_configs
from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("datasets", "bnetza_mastr_captions")

def get_mastr_configs() -> dict:
    return {
        k: v for k, v in load_dataset_configs().get("store")["datasets"].items()
        if k.startswith("bnetza_mastr")
    }


rule create:
    """
    Create name mapping file for MaStR dataset
    """
    input:
        mastr_configs=expand(
            get_abs_dataset_path("datasets", "{name}",) / "config.yml",
            name=get_mastr_configs().keys()
        )
    output:
        outfile=DATASET_PATH / "data" / "bnetza_mastr_attribute_captions.json",
    params:
        mastr_configs=get_mastr_configs(),
        additional_captions=config["additional_captions"]
    script:
        DATASET_PATH / "scripts" / "create.py"
