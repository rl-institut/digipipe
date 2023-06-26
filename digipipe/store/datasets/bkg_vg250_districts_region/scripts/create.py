import sys

import geopandas as gpd

from digipipe.config import add_snake_logger
from digipipe.scripts.config import read_config
from digipipe.scripts.geo import (
    convert_to_multipolygon,
    rename_filter_attributes,
    reproject_simplify,
    write_geofile,
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

    data = data.assign(area_km2=data.area / 1e6)

    write_geofile(
        gdf=data,
        file=outfile,
        layer_name=config["layer"],
    )

    logger.info(f"Datapackage has been created at: {outfile}")


if __name__ == "__main__":
    infile = sys.argv[1]
    config = read_config(sys.argv[2])
    outfile = sys.argv[3]
    logger = add_snake_logger(None, "bkg_vg250_districts_region")
    process()
