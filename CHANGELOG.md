# Changelog
All notable changes to this project will be documented in this file.

The format is inspired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versioning aim to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Setup initial structure and files
- Add first bunch of datasets for testing the data flow
- Modularize datasets
- Add first draft of RTD docs
- Add dataset: BNetzA MaStR
- Add Nominatim geocoder
- Add dataset: population
- Clean rule
- Datasets attribute captions
- Create list of region-specific datasets in the docs
- pyproject.toml and poetry.lock file have been added with the conversion to poetry
- Add pre-commit in order to check for errors and linting bugs before commits
- Add types-pyyaml package
- Add dataset: employees and companies
- Add dataset: demandregio electricity demand
- Add dataset: BMWK long-term scenarios
- Add rules to download raw data (zipped) from cloud, extract and copy to 'store/raw'
- Add module 'data_io', containing relevant helper functions (downloading, extracting, copying, cleaning)
- Create metadata
- Add script to generate dataset md files for documentation
- Add dataset: demand_heat_region
- Add dataset: heatpump_cop
- Add dataset: stala_st_energy
- Add dataset: eurostat_lau
- Add dataset: regstat_energy
- Add dataset: dwd_temperature
- Add dataset: ageb_energy_balance
- Add dataset: seenergies_peta5
- Add dataset: renewables.ninja_feedin
- Add dataset: renewable_feedin
- Add dataset: bnetza_mastr_correction_region and correct wrong units
- Integrate building of energy system for appdata in pipeline via dir *esys*
- Update store with dir structure for *esys* data
- Add creation of empty time series for the *esys*
- Add dataset: rpg_abw_regional_plan
- Add dataset: potentialarea_wind_region
- Add writing of default values to *esys* raw scalar data
- Add datasets: rli_pv_wfr and rli_pv_wfr_region
- Add module appdata to workflow
- Add dataset: geodata_infolayers
- Add dataset: potentialarea_pv_ground_region
- Add dataset: app datapackage
- Add dataset: potentialarea_pv_roof_region
- Add Logging

### Changed

- Move dataset docs from config to md files
- Retain mastr_id in MaStR datasets
- Fix loading of empty yml files
- Fix loading of global config when in workflow dir
- Integrate esys Snakefile in workflow Snakefile and update clean rule
- Fix shapely deprecation warning
- Fix ogr2ogr conversion with recent GDAL version (v3.6.2)
- Fix conda installation by removing python-gdal from environment.yml
- The package management in digipipe has been changed to poetry.
- The installation of a virtual environment is done only from the environment.yml file and via conda.
- Apply linters on repo among others: black, isort, check-json and end-of-file-fixer
- Update population with prognoses from demandregio dataset
- Fix C419 flake8 error
- Switch to mkdocs for documentation (Sphinx deleted)
- Normalize renewable feedin timeseries
- Fix instruction to obtain raw files
- Translate all dataset.md files to German
- Exchange *Test_scenario* with *2045_scenario* in *digipipe/esys/scenarios*
- Split each demand per sector in *esys*
- File .gitignore again includes ignoring of esys appdata

### Removed

- setup.py and requirements.txt files are omitted with the conversion to poetry
- sphinx from poetry environment
