"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path, create_tag_string_osmium

rule convert:
    """
    Convert OSM pbf file while filtering for all requested tags. All attributes are retained.
    """
    input: get_abs_dataset_path("raw", "osm_sachsen-anhalt") / "data" / "sachsen-anhalt-221003.osm.pbf"
    output: get_abs_dataset_path("preprocessed", "osm_filtered") / "data" / "sachsen-anhalt-221003.osm.gpkg"
    params: tags=create_tag_string_osmium(config["tags"])
    shell:
        "osmium tags-filter --remove-tags -f osm {input} {params.tags} | "
        "ogr2ogr -f GPKG -t_srs EPSG:3035 {output} /vsistdin/?buffer_limit=-1"
