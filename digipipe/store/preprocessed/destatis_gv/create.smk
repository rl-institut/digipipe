"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("preprocessed", "destatis_gv")

rule create:
    """
    Extract municipality population data from Excel files and save to CSVs
    """
    input:
        get_abs_dataset_path("raw", "destatis_gv") / "data" / "3112{year}_Auszug_GV.xlsx"
    output:
        DATASET_PATH / "data" / "3112{year}_Auszug_GV.csv"
    script:
        DATASET_PATH / "scripts" / "create.py"
