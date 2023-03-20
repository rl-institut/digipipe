import geopandas as gpd
import pandas as pd

from digipipe.scripts.datasets import mastr
from digipipe.scripts.geo import (
    overlay,
    rename_filter_attributes,
    write_geofile,
)


def process() -> None:
    # Read units
    units = pd.read_csv(
        snakemake.input.units,
        usecols=(
            set(snakemake.config["unit_attributes"].keys())
            | set(snakemake.config["unit_attributes_filter"].keys())
        ),
        dtype={"Postleitzahl": str},
    )
    units = rename_filter_attributes(
        gdf=units,
        attrs_filter_by_values=snakemake.config["unit_attributes_filter"],
        attrs_mapping=snakemake.config["unit_attributes"],
    ).set_index("mastr_id")

    # Read plants (for storage capacity)
    plants = pd.read_csv(
        snakemake.input.units_capacity,
        usecols=snakemake.config["plant_attributes"].keys(),
    )
    plants = rename_filter_attributes(
        gdf=plants,
        attrs_mapping=snakemake.config["plant_attributes"],
    )

    # Merge storage capacity
    units = units.merge(
        plants,
        left_on="mastr_id",
        right_on="unit_mastr_id",
        how="left",
    )
    units_count_wo_capacity = len(units.loc[units.plant_mastr_id.isna()])
    if units_count_wo_capacity > 0:
        print(
            f"{units_count_wo_capacity} storages have no plant associated and "
            f"hence no storage capacity assigned."
        )
    units.drop(columns=["unit_mastr_id", "plant_mastr_id"], inplace=True)

    units = mastr.add_voltage_level(
        units_df=units,
        locations_path=snakemake.input.locations,
        gridconn_path=snakemake.input.gridconn,
    )

    # Add geometry and drop units without coords and
    # add column to indicate that location from original data was used
    units_with_geom = mastr.add_geometry(units)
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
            columns_agg_functions={
                "capacity_net": ("capacity_net", "sum"),
                "unit_count": ("capacity_net", "count"),
                "capacity_gross": ("capacity_gross", "sum"),
                "storage_capacity": ("storage_capacity", "sum"),
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
    write_geofile(
        gdf=units_agg,
        file=snakemake.output.outfile_agg,
        layer_name=snakemake.config["layer"],
    )


process()
