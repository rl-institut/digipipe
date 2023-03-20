"""
Helper functions for datasets
"""

import inspect
import os
from pathlib import Path

import pandas as pd

from digipipe import store


def get_abs_store_root_path():
    """Get absolute path to data store

    Returns
    -------
    PosixPath
        Path to data store
    """
    return Path(os.path.dirname(inspect.getfile(store)))


def get_abs_dataset_path(category, name, data_dir=False):
    """Get absolute path to a dataset

    Parameters
    ----------
    category : str
        Category in data store, one of
        ["raw", "preprocessed", "dataset", "appdata"]
    name : str
        Name of dataset (subdir)
    data_dir : bool
        If True, the subdir "data" where data lives is added to the path

    Returns
    -------
    PosixPath
        Path to dataset
    """
    if category not in ["raw", "preprocessed", "datasets", "appdata"]:
        raise ValueError(f"Category '{category}' not found.")
    p = Path(get_abs_store_root_path()) / category / name
    if data_dir is True:
        p = p / "data"
    return p


def create_tag_string_osmium(taglist):
    """Create tag string required by osmium for extraction of OSM data.

    Parameters
    ----------
    taglist : list of lists
        List of tags, format: [[key_1, value_1], ... [key_n, value_n]]

    Returns
    -------
    str
        String with tags
    """
    tag_string = ""
    for k, v in taglist:
        tag_string += "=".join([k, str(v)]) + " "
    tag_string = tag_string[:-1]
    return tag_string


def create_tag_string_ogr(taglist):
    """Create tag string required by ogr2ogr for extraction of OSM data.

    Parameters
    ----------
    taglist : list of lists
        List of tags, format: [[key_1, value_1], ... [key_n, value_n]]

    Returns
    -------
    dict
        Tags (key: "tags") and filter conditions (key: "conditions")
    """
    tag_conditions = (
        '-where "'
        + " OR ".join(
            [
                "=".join(['\\"' + tag + '\\"', '\\"' + str(val) + '\\"'])
                for tag, val in taglist
            ]
        )
        + '"'
    )
    tags = ",".join([tag for tag, _ in taglist])
    return {"tags": tags, "conditions": tag_conditions}


PATH_TO_REGION_MUNICIPALITIES_GPKG = (
    get_abs_dataset_path("datasets", "bkg_vg250_muns_region", data_dir=True)
    / "bkg_vg250_muns_region.gpkg"
)
PATH_TO_REGION_DISTRICTS_GPKG = (
    get_abs_dataset_path(
        "datasets", "bkg_vg250_districts_region", data_dir=True
    )
    / "bkg_vg250_districts_region.gpkg"
)


def df_merge_string_columns(
    df: pd.DataFrame, source_delimiter: str = ";", target_delimiter: str = "; "
) -> pd.Series:
    """
    Merge delimiter-separated strings in columns of DataFrame into new column
    with unique values. Empty values are dropped.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with columns to be merged
    source_delimiter : str
        Delimiter in original strings of all columns
    target_delimiter : str
        Desired delimiter in resulting Series

    Returns
    -------
    pd.Series
        Column with joined strings
    """
    df_result = df.copy()
    for col in df.columns:
        df_result[col] = df[col].apply(
            lambda f: "|".join(
                [_ for _ in set(f.split(source_delimiter)) if _ != ""]
            )
        )
    s = df_result.agg("|".join, axis=1)

    return s.apply(
        lambda f: target_delimiter.join(
            [_ for _ in set(f.split("|")) if _ != ""]
        )
    )
