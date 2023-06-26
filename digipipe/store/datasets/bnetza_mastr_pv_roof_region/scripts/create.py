import geopandas as gpd
import pandas as pd

from digipipe.config import add_snake_logger
from digipipe.scripts.datasets import mastr
from digipipe.scripts.geo import (
    overlay,
    rename_filter_attributes,
    write_geofile,
)


def process() -> None:
    attrs = snakemake.config["attributes"]
    attrs_filter = snakemake.config["attributes_filter"]

    units = pd.read_csv(
        snakemake.input.units,
        usecols=set(attrs.keys()) | set(attrs_filter.keys()),
        dtype={"Postleitzahl": str},
        index_col="EinheitMastrNummer",
    )

    # Apply corrections
    unit_correction = pd.read_csv(
        snakemake.input.unit_correction,
        delimiter=";",
        index_col="mastr_id",
    )
    units = mastr.apply_manual_corrections(
        units_df=units,
        units_correction_df=unit_correction,
    )

    units = rename_filter_attributes(
        gdf=units,
        attrs_filter_by_values=attrs_filter,
        attrs_mapping=attrs,
    ).set_index("mastr_id")

    units = mastr.add_voltage_level(
        units_df=units,
        locations_path=snakemake.input.locations,
        gridconn_path=snakemake.input.gridconn,
    )

    # Add geometry and drop units without coords and
    # add column to indicate that location from original data was used
    units_with_geom = mastr.add_geometry(units, logger)
    units_with_geom = units_with_geom.assign(
        geometry_approximated=0,
    )

    units_without_geom = units.loc[(units.lon.isna() | units.lat.isna())].drop(
        columns=["lon", "lat"]
    )

    # Add geometry for all units without coords (<=30 kW) and
    # add column to indicate that location was inferred by geocoding
    if len(units_without_geom) > 0:
        (
            units_with_inferred_geom_gdf,
            units_with_inferred_geom_agg_gdf,
        ) = mastr.geocode_units_wo_geometry(
            units_without_geom,
            logger,
            columns_agg_functions={
                "capacity_net": ("capacity_net", "sum"),
                "unit_count": ("capacity_net", "count"),
                "capacity_gross": ("capacity_gross", "sum"),
            },
        )

        # Merge both GDFs
        units = pd.concat([units_with_geom, units_with_inferred_geom_gdf])

        units_agg = pd.concat(
            [
                units_with_geom.assign(unit_count=1),
                units_with_inferred_geom_agg_gdf,
            ]
        )
    else:
        units = units_with_geom
        units_agg = units_with_geom.assign(unit_count=1)

    # Clip to region and add mun and district ids
    units = overlay(
        gdf=units,
        gdf_overlay=gpd.read_file(snakemake.input.region_muns),
        retain_rename_overlay_columns={"id": "municipality_id"},
    )
    units = overlay(
        gdf=units,
        gdf_overlay=gpd.read_file(snakemake.input.region_districts),
        retain_rename_overlay_columns={"id": "district_id"},
    )
    units_agg = overlay(
        gdf=units_agg,
        gdf_overlay=gpd.read_file(snakemake.input.region_muns),
        retain_rename_overlay_columns={"id": "municipality_id"},
    )
    units_agg = overlay(
        gdf=units_agg,
        gdf_overlay=gpd.read_file(snakemake.input.region_districts),
        retain_rename_overlay_columns={"id": "district_id"},
    )

    write_geofile(
        gdf=units,
        file=snakemake.output.outfile,
        layer_name=snakemake.config["layer"],
    )

    logger.info(f"Datapackage has been created at: {snakemake.output.outfile}")

    write_geofile(
        gdf=units_agg,
        file=snakemake.output.outfile_agg,
        layer_name=snakemake.config["layer"],
    )
    logger.info(
        f"Datapackage has been created at: {snakemake.output.outfile_agg}"
    )


if __name__ == "__main__":
    logger = add_snake_logger(str(snakemake.log), "bnetza_mastr_pv_roof_region")
    process()
