import sys
import geopandas as gpd
from digipipe.scripts.geo import (
    convert_to_multipolygon,
    write_geofile,
    rename_filter_attributes,
    reproject_simplify
)


def process():
    data = gpd.read_file(infile, layer=config["layer"])
    data = rename_filter_attributes(
        gdf=data,
        attrs_filter_by_values=config["attributes_filter"],
        attrs_mapping=config["attributes"],
    )
    data = reproject_simplify(
        gdf=data,
        add_id_column=True,
    )
    data = convert_to_multipolygon(data)
    write_geofile(
        gdf=data,
        file=outfile,
        layer_name=config["layer"],
    )


if __name__ == "__main__":
    infile = snakemake.input[0]
    config = snakemake.config
    outfile = snakemake.output[0]
    process()