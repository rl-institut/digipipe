import geopandas as gpd
import pandas as pd


def process() -> None:
    pop_history = pd.concat(
        [
            pd.read_csv(f, dtype={"ags": str}, index_col="ags")
            for f in snakemake.input.pop_history
        ],
        axis=1,
    )
    pop_prognosis = pd.read_csv(
        snakemake.input.pop_prognosis,
        dtype={"ags": str},
        index_col="ags",
    ).round()

    # Filter by region and get available years
    muns = gpd.read_file(snakemake.input.region_muns)

    pop_history = pop_history.loc[pop_history.index.isin(muns.ags)]
    avail_years_history = pop_history.columns.astype(int).to_list()
    print(f"Historical years: {avail_years_history}")

    prognosis_years = snakemake.config["prognosis"]["years"]
    pop_prognosis = pop_prognosis.loc[pop_prognosis.index.isin(muns.ags)]
    avail_years_prognosis = pop_prognosis.columns.astype(int).to_list()
    print(f"Prognosis years: {prognosis_years}")

    # Extrapolate population linearly for years from config
    extrapol_years = snakemake.config["extrapolation"]["years"]
    print(f"Extrapolation years: {extrapol_years}")
    for year in extrapol_years:
        # Extrapolate until 2045 using the last 2 available years
        year_delta_base = avail_years_prognosis[-1] - avail_years_prognosis[-2]
        year_delta_extrapol = year - avail_years_prognosis[-1]
        pop_prognosis[str(year)] = (
            pop_prognosis[str(avail_years_prognosis[-1])]
            + (
                pop_prognosis[str(avail_years_prognosis[-1])]
                - pop_prognosis[str(avail_years_prognosis[-2])]
            )
            / year_delta_base
            * year_delta_extrapol
        )

    # Drop not requested prognosis years and glue everything together
    pop_prognosis.drop(
        columns=[
            c
            for c in pop_prognosis.columns
            if int(c) not in prognosis_years + extrapol_years
        ],
        inplace=True,
    )
    population = pd.concat([pop_history, pop_prognosis], axis=1)

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
            + len(prognosis_years) * ["prognosis"]
            + len(extrapol_years) * ["extrapolation"],
        ],
        names=("year", "type"),
    )

    population.to_csv(snakemake.output[0])


if __name__ == "__main__":
    process()
