"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
Please add a docstring with a short description to each rule.
"""
from pathlib import Path
from digipipe.store.utils import get_abs_dataset_path, get_abs_store_root_path

#configfile: get_abs_dataset_path("preprocessed", ".TEMPLATE", data_dir=False) / "config.yml"


# Use function `get_abs_dataset_path()` to get path to dataset
rule template_simple_copy_file1:
    input: get_abs_dataset_path("raw", ".TEMPLATE") / "some_timeseries.csv"
    output: get_abs_dataset_path("preprocessed", ".TEMPLATE") / "some_timeseries.csv"
    log:
        get_abs_store_root_path() / "preprocessed" / ".log" / "TEMPLATE.log"
    shell: "cp -p {input} {output}"

# Or you can use relative paths which may break as snakemake can be invoked
# from directories digipipe/ or digipipe/workflow/.
rule template_simple_copy_file2:
    input: Path(".") / "store" / "raw" / ".TEMPLATE" / "data" /  "some_timeseries.csv"
    output: Path(".") / "store" / "preprocessed" / ".TEMPLATE" / "data" / "some_timeseries.csv"
    log:
        get_abs_store_root_path() / "preprocessed" / ".log" / "TEMPLATE.log"
    shell: "cp -p {input} {output}"
