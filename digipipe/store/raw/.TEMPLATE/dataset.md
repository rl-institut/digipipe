# Name of the dataset

Here comes a short description of the dataset.
This is helpful for documentation and report generation purposes.

# Notes (just for information, must not be part of the dataset.md file)

Naming convention: `<source_datasetname>` (lower case), e.g. for a dataset on
natural reserves by the Bundesamt für Naturschutz (BfN) you would name the dir
`bfn_natural_reserves` or similar.

What is a dataset? Well, there are different definitions around but in the
workflow of this pipeline a dataset is a collection of data treated as a
single unit which can consist of multiple files and identified by a single
metadata file.

Examples:
- [OSM Germany](https://download.geofabrik.de/europe/germany-latest.osm.pbf)
- [ERA5 weather dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview)
- [BKG administrative areas](https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html)

Put raw files into dir `data` and, if possible, do not rename the file(s).

## Description

Please provide at least a brief description:

- What is this dataset about?
- Are there any specific things worth to know? (apart from metadata that MUST
  be created, see below)

A quick and dirty description is better than no description.

## Metadata

Add a metadata for every raw/original dataset you put here for describing data
with machine-readable information. Adhere to the
[OEP](https://openenergy-platform.org/about/) Metadata v1.5.1. You can make
use of the [Metadata creator](https://meta.rl-institut.de/meta_creator/151).

See the [metadata.json](metadata.json) file in this directory.

Alternatively, you can create them manually: follow
[this example](https://github.com/OpenEnergyPlatform/oemetadata/blob/develop/metadata/latest/example.json)
to understand how the fields are used. Field are described in detail in the
[Open Energy Metadata Description](https://github.com/OpenEnergyPlatform/oemetadata/blob/develop/metadata/v141/metadata_key_description.md).
Please verify that your metadata string is in compliance with the OEP Metadata
standard using the [OMI tool](https://github.com/OpenEnergyPlatform/omi).
If your metadata string is compliant, OMI puts the keys in the correct order
and  prints the full string (use `-o` option for export).
