"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("preprocessed", "stala_st_pop_prog")

rule create:
    """
    Extract municipality population data from Excel files and save to CSVs
    """
    input: get_abs_dataset_path("raw", "stala_st_pop_prog") / "data" / "1_Internettabelle_7RBP_nach_Prognosejahr_Geschlecht_alle_Ebenen.xlsx"
    output: DATASET_PATH / "data" / "population_prognosis_st_muns.csv"
    script: DATASET_PATH / "scripts" / "create.py"
