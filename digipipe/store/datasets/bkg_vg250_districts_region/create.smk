"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path, get_abs_store_root_path

DATASET_PATH = get_abs_dataset_path("datasets", "bkg_vg250_districts_region")
STORE_PATH = get_abs_store_root_path()

rule create:
    """
    Extract districts of region
    """
    input: rules.preprocessed_bkg_vg250_create.output
    output: DATASET_PATH / "data" / "bkg_vg250_districts_region.gpkg"
    params:
        script=DATASET_PATH / "scripts" / "create.py",
        config_path=DATASET_PATH / "config.yml"
    log: STORE_PATH / "datasets" / ".log" / "bkg_vg250_districts_region.log"
    shell:
        "python {params.script} {input} {params.config_path} {output} {log}"
