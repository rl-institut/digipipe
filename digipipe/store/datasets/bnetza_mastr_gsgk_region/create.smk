"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

import geopandas as gpd

from digipipe.scripts.datasets.mastr import create_stats_per_municipality
from digipipe.store.utils import (
    get_abs_dataset_path,
    get_abs_store_root_path,
    PATH_TO_REGION_MUNICIPALITIES_GPKG,
    PATH_TO_REGION_DISTRICTS_GPKG
)

DATASET_PATH = get_abs_dataset_path("datasets", "bnetza_mastr_gsgk_region")
SOURCE_DATASET_PATH = get_abs_dataset_path("preprocessed", "bnetza_mastr", data_dir=True)
STORE_PATH = get_abs_store_root_path()

rule create:
    """
    Extract gsgk units for region
    """
    input:
        units=SOURCE_DATASET_PATH / "bnetza_mastr_gsgk_raw.csv",
        locations=SOURCE_DATASET_PATH / "bnetza_mastr_locations_extended_raw.csv",
        gridconn=SOURCE_DATASET_PATH / "bnetza_mastr_grid_connections_raw.csv",
        region_muns=PATH_TO_REGION_MUNICIPALITIES_GPKG,
        region_districts=PATH_TO_REGION_DISTRICTS_GPKG
    output:
        outfile=DATASET_PATH / "data" / "bnetza_mastr_gsgk_region.gpkg",
        outfile_agg=DATASET_PATH / "data" / "bnetza_mastr_gsgk_agg_region.gpkg"
    params:
        config_file=DATASET_PATH / "config.yml"
    log: STORE_PATH / "datasets" / ".log" / "bnetza_mastr_gsgk_region.log"
    script:
        DATASET_PATH / "scripts" / "create.py"

rule create_power_stats_muns:
    """
    Create stats on installed count of units and power per mun
    """
    input:
        units=DATASET_PATH / "data" / "bnetza_mastr_gsgk_region.gpkg",
        region_muns=PATH_TO_REGION_MUNICIPALITIES_GPKG,
    output: DATASET_PATH / "data" / "bnetza_mastr_gsgk_stats_muns.csv"
    run:
        units = create_stats_per_municipality(
            units_df=gpd.read_file(input.units),
            muns=gpd.read_file(input.region_muns),
            column="capacity_net"
        )
        units["capacity_net"] = units["capacity_net"].div(1e3)  # kW to MW
        units.to_csv(output[0])
