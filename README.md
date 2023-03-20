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

Prerequisite:
* _conda_ ([Anaconda](https://docs.anaconda.com/anaconda/install/)
/[Miniconda](https://conda.io/en/latest/miniconda.html))
* `python <https://www.python.org/downloads/>`_

Enter repo folder. Set up a conda environment and activate it with:

```
conda env create -f environment.yml
conda activate digiplan
```

Install [poetry](https://python-poetry.org/) (python dependency manager used
in this project) and dependencies for the project (Note: Installing poetry via
pip into same environment is not recommended and can cause trouble! Instead it
should be installed system-wide via command below or
[pipx](https://python-poetry.org/docs/#installing-with-pipx)):

```
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

Some additional system packages are required, install them by

    apt install gdal-bin python3-gdal libspatialindex-dev imagemagick osmium-tool graphviz graphviz-dev

Notes:
- Make sure you have GDAL>=3.0 as older versions will not work
- `imagemagick` is optional and only required for report creation

## Contributing to digipipe

You can write `issues <https://github.com/rl-institut-private/digipipe/issues>`_ to announce bugs or to propose enhancements.

If you want to participate in the development of digipipe, please make sure you use pre-commit.

You activate it with:

    pre-commit install

To trigger a check manually, execute:

    pre-commit run -a

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
