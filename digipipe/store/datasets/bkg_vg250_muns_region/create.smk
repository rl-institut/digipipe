"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path, get_abs_store_root_path, PATH_TO_REGION_DISTRICTS_GPKG

DATASET_PATH = get_abs_dataset_path("datasets", "bkg_vg250_muns_region")
STORE_PATH = get_abs_store_root_path()

rule create:
    """
    Extract municipalities of region
    """
    input:
        muns=rules.preprocessed_bkg_vg250_create.output,
        districts=PATH_TO_REGION_DISTRICTS_GPKG
    output: DATASET_PATH / "data" / "bkg_vg250_muns_region.gpkg"
    log: STORE_PATH / "datasets" / ".log" / "bkg_vg250_muns_region.log"
    script: DATASET_PATH / "scripts" / "create.py"
