"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path, get_abs_store_root_path, create_tag_string_ogr
from digipipe.config.__init__ import add_snake_logger

rule extract_tags:
    """
    Create layers from converted OSM file using requested tags per layer. Only requested attributes are retained.
    """
    input: rules.preprocessed_osm_filtered_convert.output
    output: get_abs_dataset_path("datasets", "osm_forest") / "data" / "osm_forest.gpkg"
    params:
        tags=create_tag_string_ogr(config["tags"]),
        geom_type=config["geom_type"]
    log:
         get_abs_store_root_path() / "datasets" / ".log" / "osm_forest.log"
    run:
        logger = add_snake_logger(f"{log}", "osm_forest")

        shell(
            f"ogr2ogr -f GPKG -select {params.tags['tags']} "
            f"{params.tags['conditions']} {output} {input} {params.geom_type} 2>&1 > {log}"
        )

        logger.info(f"Datapackage has been created at: {output}")
