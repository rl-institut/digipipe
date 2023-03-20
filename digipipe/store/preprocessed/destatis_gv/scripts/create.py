import pandas as pd


def process() -> None:
    # Get Excel config and set sheet name
    excel_cfg = snakemake.config["excel_file"]
    excel_cfg["sheet_name"] = excel_cfg["sheet_name"][snakemake.wildcards.year]

    data = pd.read_excel(
        snakemake.input[0],
        **excel_cfg,
        engine="openpyxl",
    )

    # Drop non-municipal data
    data = data.loc[~data.isnull().any(axis=1)]
    data = data.assign(population=data.population.astype(int)).rename(
        columns={"population": snakemake.wildcards.year}
    )

    # Create AGS and drop old cols
    data = data.assign(ags=data.Land + data.RB + data.Kreis + data.Gem)

    data[["ags", snakemake.wildcards.year]].to_csv(
        snakemake.output[0], index=None
    )


if __name__ == "__main__":
    process()
