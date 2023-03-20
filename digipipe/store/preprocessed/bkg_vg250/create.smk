"""
Snakefile for this dataset

Note: To include the file in the main workflow, it must be added to the respective module.smk .
"""

from digipipe.store.utils import get_abs_dataset_path

DATASET_PATH = get_abs_dataset_path("preprocessed", "bkg_vg250")

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
    shell:
        """
        unzip -j {input} {params.file_path_in_zip} -d {params.outpath}
        ogr2ogr -f GPKG -t_srs EPSG:3035 {output} {params.original_file} {params.layers}
        rm {params.original_file}
        """
