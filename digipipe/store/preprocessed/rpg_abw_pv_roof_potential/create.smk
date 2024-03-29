"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

import geopandas as gpd

from digipipe.scripts.geo import (
    rename_filter_attributes,
    reproject_simplify,
    write_geofile
)
from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("preprocessed", "rpg_abw_pv_roof_potential")

rule create:
    input:
        get_abs_dataset_path(
            "raw", "rpg_abw_pv_roof_potential"
        ) / "data" / "rpg_abw_pv_roof_potential.gpkg"
    output:
        DATASET_PATH / "data" / "rpg_abw_pv_roof_potential.gpkg"
    run:
        data = reproject_simplify(
            rename_filter_attributes(
                gdf=gpd.read_file(input[0]),
                attrs_mapping=config["attributes"]
            )
        )
        write_geofile(
            gdf=data,
            file=output[0],
            layer_name=config["layer"],
        )
