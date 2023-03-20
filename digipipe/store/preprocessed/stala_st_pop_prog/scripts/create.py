import pandas as pd


def process() -> None:
    data = pd.read_excel(
        snakemake.input[0],
        **snakemake.config["excel_file"],
        engine="openpyxl",
    ).rename(columns={"AGS": "ags"})

    # Rename columns
    data.set_index("ags", inplace=True)
    data.columns = [int(col[1]) for col in data.columns.str.split("\n")]

    # Select desired years
    print(f"Available years for population prognosis: {data.columns.to_list()}")
    years = snakemake.config["years"]
    if len(years) > 0:
        data = data[years]
        print(f"  Selected: {years}")

    # Rename columns
    data.reset_index(inplace=True)

    # Drop non-municipal data
    data = data.loc[data.ags.str.len() > 2]
    data = data.assign(
        ags=data.ags.str.pad(width=8, side="right", fillchar="0")
    ).set_index("ags")

    data.to_csv(snakemake.output[0])


if __name__ == "__main__":
    process()
