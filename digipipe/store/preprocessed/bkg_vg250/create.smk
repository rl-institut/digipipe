"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path, get_abs_store_root_path
from digipipe.config.__init__ import add_snake_logger

DATASET_PATH = get_abs_dataset_path("preprocessed", "bkg_vg250")
STORE_PATH = get_abs_store_root_path()

rule create:
    input:
        get_abs_dataset_path("raw", "bkg_vg250") / "data" / "vg250_01-01.utm32s.gpkg.ebenen.zip"
    output:
        DATASET_PATH / "data" / "bkg_vg250.gpkg"
    params:
        outpath=DATASET_PATH / "data",
        original_file=DATASET_PATH / "data" / "DE_VG250.gpkg",
        file_path_in_zip=str("vg250_01-01.utm32s.gpkg.ebenen/vg250_ebenen_0101/DE_VG250.gpkg"),
        layers=" ".join(config["layers"])
    log:
        STORE_PATH / "preprocessed" / ".log" / "bkg_vg250.log"
    run:
        logger = add_snake_logger(f"{log}", "bkg_vg250")
        shell(
            """
            unzip -j {input} {params.file_path_in_zip} -d {params.outpath} 2>&1 > {log}
            ogr2ogr -f GPKG -t_srs EPSG:3035 {output} {params.original_file} {params.layers} 2>&1 > {log}
            rm {params.original_file} 2>&1 > {log}
            """
        )
        logger.info(f"Datapackage has been created at: {output}")
