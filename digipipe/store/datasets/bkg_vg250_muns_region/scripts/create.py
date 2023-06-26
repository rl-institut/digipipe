import geopandas as gpd

from digipipe.config import add_snake_logger
from digipipe.scripts.geo import (
    convert_to_multipolygon,
    overlay,
    rename_filter_attributes,
    reproject_simplify,
    write_geofile,
)


def process():
    muns = gpd.read_file(snakemake.input.muns[0], layer=config["layer"])
    muns = rename_filter_attributes(
        gdf=muns,
        attrs_filter_by_values=config["attributes_filter"],
        attrs_mapping=config["attributes"],
    )
    muns = reproject_simplify(
        gdf=muns,
        add_id_column=True,
    )

    muns = overlay(
        gdf=muns.rename(columns={"id": "municipality_id"}),
        gdf_overlay=gpd.read_file(snakemake.input.districts),
        retain_rename_overlay_columns={"id": "district_id"},
        gdf_use_centroid=True,
    ).rename(columns={"municipality_id": "id"})

    muns = muns.assign(area_km2=muns.area / 1e6)

    muns = convert_to_multipolygon(muns)

    write_geofile(
        gdf=muns,
        file=snakemake.output[0],
        layer_name=config["layer"],
    )

    logger.info(f"Datapackage has been created at: {snakemake.output[0]}")


if __name__ == "__main__":
    config = snakemake.config
    logger = add_snake_logger(str(snakemake.log), "bkg_vg250_muns_region")

    process()
