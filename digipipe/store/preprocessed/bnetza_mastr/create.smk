"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path, get_abs_store_root_path
from digipipe.config.__init__ import add_snake_logger

DATASET_PATH = get_abs_dataset_path("preprocessed", "bnetza_mastr")
STORE_PATH = get_abs_store_root_path()

rule create:
    input:
        get_abs_dataset_path("raw", "bnetza_mastr") / "data" / "bnetza_open_mastr_2022-12-19.zip"
    output:
        files=[DATASET_PATH / "data" / f for f in config["files_extract"]]
    params:
        outpath=DATASET_PATH / "data",
        files_extract=" ".join([f"bnetza_open_mastr_2022-12-19/{f}" for f in config["files_extract"]])
    log:
        STORE_PATH / "preprocessed" / ".log" / "bnetza_mastr.log"
    run:
        logger = add_snake_logger(f"{log}", "bnetza_mastr")
        shell(
            """
            unzip -j {input} {params.files_extract} -d {params.outpath} 2>&1 > {log}
            """
        )
        logger.info(f"Datapackage has been created at: {output}")
