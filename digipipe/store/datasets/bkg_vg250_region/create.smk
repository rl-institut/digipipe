"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("datasets", "bkg_vg250_region")

rule create:
    """
    Create region polygon from districts
    """
    input: rules.datasets_bkg_vg250_districts_region_create.output
    output: DATASET_PATH / "data" / "bkg_vg250_region.gpkg"
    params:
        script=DATASET_PATH / "scripts" / "create.py",
        config_path=DATASET_PATH / "config.yml"
    shell:
        "python {params.script} {input} {params.config_path} {output}"
