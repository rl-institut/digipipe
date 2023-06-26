"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import (
    get_abs_dataset_path,
    get_abs_store_root_path,
    PATH_TO_REGION_MUNICIPALITIES_GPKG,
    PATH_TO_REGION_DISTRICTS_GPKG
)

DATASET_PATH = get_abs_dataset_path("datasets", "population_region")
STORE_PATH = get_abs_store_root_path()

rule create:
    """
    Create full population dataset for region
    """
    input:
        pop_history=expand(
            get_abs_dataset_path("preprocessed", "destatis_gv") / "data" / "3112{year}_Auszug_GV.csv",
            year=[2010, 2015, 2020, 2021, 2022]
        ),
        prognosis_fstate_munlevel=get_abs_dataset_path(
            "preprocessed", "stala_st_pop_prog") / "data" /
            "population_prognosis_st_muns.csv",
        prognosis_germany_districtlevel=get_abs_dataset_path(
            "preprocessed", "demandregio") / "data" / "dr_hh_population.csv",
        region_muns=PATH_TO_REGION_MUNICIPALITIES_GPKG,
        region_districts=PATH_TO_REGION_DISTRICTS_GPKG
    output:
        DATASET_PATH / "data" / "population.csv"
    log:
        STORE_PATH / "datasets" / ".log" / "population_region.log"
    script:
        DATASET_PATH / "scripts" / "create.py"
