import sys
import geopandas as gpd
from digipipe.scripts.config import read_config
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
    infile = sys.argv[1]
    config = read_config(sys.argv[2])
    outfile = sys.argv[3]
    process()