import geopandas as gpd
import pandas as pd

from digipipe.config import add_snake_logger


def process() -> None:
    # pylint: disable=R0914
    # Get muns and their NUTS3 code
    muns = gpd.read_file(snakemake.input.region_muns)
    districts = gpd.read_file(snakemake.input.region_districts)
    muns = muns.merge(
        districts[["id", "nuts"]].rename(columns={"id": "district_id"}),
        left_on="district_id",
        right_on="district_id",
    )

    # Historical data: load, get available years and filter by region
    pop_history = pd.concat(
        [
            pd.read_csv(f, dtype={"ags": str}, index_col="ags")
            for f in snakemake.input.pop_history
        ],
        axis=1,
    )
    pop_history = pop_history.loc[pop_history.index.isin(muns.ags)]
    avail_years_history = pop_history.columns.astype(int).to_list()
    logger.info(f"Historical years: {avail_years_history}")

    # Prognosis: load state data on municipal level and filter by region
    pop_prognosis_years_mun = snakemake.config["prognosis_fstate_munlevel"][
        "years"
    ]
    if len(pop_prognosis_years_mun) > 0:
        pop_prognosis_mun = pd.read_csv(
            snakemake.input.prognosis_fstate_munlevel,
            dtype={"ags": str},
            index_col="ags",
        ).round()
        pop_prognosis_mun = pop_prognosis_mun.loc[
            pop_prognosis_mun.index.isin(muns.ags)
        ]
        avail_years_prognosis = pop_prognosis_mun.columns.astype(int).to_list()
        logger.info(
            f"Prognosis years (state data on municipal level): "
            f"{pop_prognosis_years_mun}"
        )
        pop_reference = pop_prognosis_mun
        pop_reference_years = pop_prognosis_years_mun
    else:
        pop_reference = pop_history
        pop_reference_years = avail_years_history
        logger.warning(
            "No years for prognosis with state data on municipal level "
            "provided, skipping..."
        )

    # Prognosis: load country data on district (NUTS 3) level
    pop_prognosis_years_district = snakemake.config[
        "prognosis_germany_districtlevel"
    ]["years"]
    if len(pop_prognosis_years_district) > 0:
        pop_prognosis_district = pd.read_csv(
            snakemake.input.prognosis_germany_districtlevel,
            index_col="nuts3",
        )
        pop_prognosis_district = pop_prognosis_district.loc[muns.nuts.unique()][
            [str(y) for y in pop_prognosis_years_district]
        ]
        avail_years_prognosis = pop_prognosis_district.columns.astype(
            int
        ).to_list()
        logger.info(
            f"Prognosis years (country data on district level): "
            f"{pop_prognosis_years_district}"
        )

        # Merge prognoses: create municipal prognosis from NUTS 3 level data by
        # using municipal shares from the last available state's municipal
        # prognosis.
        pop_reference_lastyear = pd.concat(
            [
                pop_reference[str(pop_reference_years[-1])],
                muns[["ags", "nuts"]].set_index("ags"),
            ],
            axis=1,
        )
        pop_reference_lastyear = (
            pop_reference_lastyear.assign(
                share=(
                    pop_reference_lastyear[str(pop_reference_years[-1])]
                    / pop_reference_lastyear.groupby("nuts")[
                        str(pop_reference_years[-1])
                    ].transform("sum")
                )
            )
            .drop(columns=[str(pop_reference_years[-1])])
            .reset_index()
        )
        pop_prognosis_district = pop_reference_lastyear.merge(
            pop_prognosis_district.reset_index(),
            left_on="nuts",
            right_on="nuts3",
        ).set_index("ags")
        for year in pop_prognosis_years_district:
            pop_reference[str(year)] = (
                pop_prognosis_district["share"]
                .mul(pop_prognosis_district[str(year)])
                .round()
            )
    else:
        logger.warning(
            "No years for prognosis with country data on district level "
            "provided, skipping..."
        )

    # Extrapolate population linearly for years from config
    extrapol_years = snakemake.config["extrapolation"]["years"]
    if len(extrapol_years) > 0:
        logger.info(f"Extrapolation years: {extrapol_years}")
        for year in extrapol_years:
            # Extrapolate using the last 2 available years
            year_delta_base = (
                avail_years_prognosis[-1] - avail_years_prognosis[-2]
            )
            year_delta_extrapol = year - avail_years_prognosis[-1]
            pop_reference[str(year)] = (
                pop_reference[str(avail_years_prognosis[-1])]
                + (
                    pop_reference[str(avail_years_prognosis[-1])]
                    - pop_reference[str(avail_years_prognosis[-2])]
                )
                / year_delta_base
                * year_delta_extrapol
            )
    else:
        logger.warning(
            "No extrapolation years provided, skipping extrapolation..."
        )

    # Drop not requested years
    pop_reference.drop(
        columns=[
            c
            for c in pop_reference.columns
            if int(c)
            not in (
                avail_years_history
                + pop_reference_years
                + pop_prognosis_years_district
                + extrapol_years
            )
        ],
        inplace=True,
    )

    # Extra-include historic data depending on if first prognosis was used
    if not all(
        str(year) in pop_reference.columns for year in avail_years_history
    ):
        population = pd.concat([pop_history, pop_reference], axis=1)
    else:
        population = pop_reference

    # Add municipality_id and data origin
    population = (
        pd.concat(
            [muns.set_index("ags")["id"].rename("municipality_id"), population],
            axis=1,
        )
        .sort_index()
        .set_index("municipality_id", drop=True)
    )
    population.columns = pd.MultiIndex.from_arrays(
        [
            population.columns,
            len(avail_years_history) * ["historic"]
            + (len(pop_prognosis_years_mun) + len(pop_prognosis_years_district))
            * ["prognosis"]
            + len(extrapol_years) * ["extrapolation"],
        ],
        names=("year", "type"),
    )

    population.to_csv(snakemake.output[0])

    logger.info(f"Datapackage has been created at: {snakemake.output[0]}")


if __name__ == "__main__":
    logger = add_snake_logger(str(snakemake.log), "population_region")
    process()
