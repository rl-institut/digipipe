<p align="left">
    <img alt="Digiplan logo" align="left" height="150" src="docs/img/logos/digiplan-logo.png">
    <img alt="RLI logo" align="right" height="140" src="docs/img/logos/rli_logo.png">
</p>
<br/><br/><br/><br/><br/><br/><br/>

----------

# Digipipe

Pipeline for data and energy system in the Digiplan project.

## Installation

**Note: Linux only, Windows is currently not supported.**

First, clone via SSH using

    git clone git@github.com:rl-institut-private/digipipe.git /local/path/to/digipipe/

### Install using pip:

Make sure you have Python >= 3.6 installed, let's create a virtual env:

    virtualenv --python=python3.8 venv
    source venv/bin/activate

Some additional system packages are required, install them by

    apt install gdal-bin python3-gdal libspatialindex-dev imagemagick osmium-tool graphviz graphviz-dev

Notes:
- Make sure you have GDAL>=3.0 as older versions will not work
- `imagemagick` is optional and only required for report creation

Install package with

    pip install -e /local/path/to/digipipe/

### Install using conda

Make sure you have conda installed, e.g. miniconda. Then create the env:

    conda create -n digipipe /local/path/to/digipipe/environment.yml
    conda activate digipipe

## Further reading on structure, pipeline and conventions

- Datasets/data flow: [DATASETS.md](digipipe/store/DATASETS.md)
- Workflow: [WORKFLOW.md](digipipe/workflow/WORKFLOW.md)
- Scenarios: [SCENARIOS.md](digipipe/scenarios/SCENARIOS.md)

## Run the pipeline

See [WORKFLOW.md](digipipe/workflow/WORKFLOW.md)

## Runtime and resources

**TO BE UPDATED**

**Warning:** A full pipeline run takes 10 hours on a Xeon E5-2690 using 14
cores and requires about 600 GB of disk space.

## Structure of this repo

```
.
├── digipipe
│   ├── config
│   │   └── global.yml                          # Global config
│   ├── logs                                    # Place for log files
│   ├── scenarios                               # Scenario definition
│   │   ├── .TEMPLATE                           # - Template
│   │   └── SCENARIOS.md
│   ├── scripts                                 # Main scripts
│   │   ├── datasets                            # - for data processing which is shared by different datasets
│   │   ├── esm                                 # - for energy system modelling
│   │   ├── config.py                           # - config-related functions
│   │   └── geo.py                              # - spatial functions
│   ├── store                                   # Data store
│   │   ├── appdata                             # - App-ready data
│   │   │   ├── data
│   │   │   ├── metadata
│   │   │   └── scenarios
│   │   ├── datasets                            # - Processed datasets
│   │   │   ├── bkg_vg250_districts_abw
│   │   │   ├── bkg_vg250_muns_abw
│   │   │   ├── bkg_vg250_region_abw
│   │   │   ├── osm_forest
│   │   │   ├── .TEMPLATE
│   │   │   └── module.smk
│   │   ├── preprocessed                        # - Preprocessed datasets
│   │   │   ├── bkg_vg250
│   │   │   ├── osm_filtered
│   │   │   ├── .TEMPLATE
│   │   │   └── module.smk
│   │   ├── raw                                 # - Raw datasets
│   │   │   ├── bkg_vg250
│   │   │   ├── destatis_gv
│   │   │   ├── osm_sachsen-anhalt
│   │   │   └── .TEMPLATE
│   │   ├── temp                                # - Temporary files
│   │   ├── DATASETS.md
│   │   └── utils.py
│   └── workflow
│       ├── Snakefile                           # Main snakefile
│       ├── utils.py
│       └── WORKFLOW.md
├── docs                                        # Documentation
│   ├── sections
│   │   ├── data.rst
│   │   ├── installation.rst
│   │   ├── scenarios.rst
│   │   ├── structure.rst
│   │   └── workflow.rst
│   ├── conf.py
│   ├── index.rst
│   └── Makefile
├── tests
├── CHANGELOG.md
├── CONTRIBUTING.md
├── environment.yml
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

(created via `tree --dirsfirst -L 4 -a -I '__*|*log|.gitkeep|PKG-INFO|*egg-info*|img|.git|.idea|venv|.snakemake' . > dirtree.txt`)
