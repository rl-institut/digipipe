"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("datasets", "bkg_vg250_muns_abw")

rule create:
    """
    Extract municipalities of ABW region
    """
    input: rules.preprocessed_bkg_vg250_create.output
    output: DATASET_PATH / "data" / "bkg_vg250_muns_abw.gpkg"
    script: DATASET_PATH / "scripts" / "create.py"