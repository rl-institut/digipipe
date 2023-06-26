import os
import sys

import geopandas as gpd

from digipipe.config import add_snake_logger
from digipipe.scripts.geo import (
    convert_to_multipolygon,
    reproject_simplify,
    write_geofile,
)


def process():
    data = gpd.read_file(infile)
    data = gpd.GeoDataFrame(
        crs=data.crs.srs, geometry=[data.buffer(0.1).unary_union]
    )
    data = reproject_simplify(gdf=data, add_id_column=True)
    data = convert_to_multipolygon(data)

    data = data.assign(area_km2=data.area / 1e6)

    write_geofile(
        gdf=data,
        file=outfile,
        layer_name=os.path.basename(outfile).split(".")[0],
    )

    logger.info(f"Datapackage has been created at: {outfile}")


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[3]
    logger = add_snake_logger(None, "bkg_vg250_region")
    process()
