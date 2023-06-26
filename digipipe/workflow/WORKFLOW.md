# Workflow

## Download and update RAW dataset

To run the pipeline the input dataset is required.
To download, extract and copy a current set of raw data into `store/raw`, type

    snakemake -j<NUMBER_OF_CPU_CORES> update_raw

A zip file from the specified URL
([Wolke](https://wolke.rl-institut.de/s/w8WKwXT3f9ZzZQJ/download))
is downloaded and unzipped to `store/temp`. The raw data files are copied to
the corresponding folders in `store/raw`.
A prompt asks if an already existing file should be updated. Confirm with "y"
or type "n" to skip.


## Run

To run the pipeline, go to Digipipe's root `digipipe/` or to
`digipipe/workflow/` and type

    snakemake -j<NUMBER_OF_CPU_CORES>

while `NUMBER_OF_CPU_CORES` is the number of CPU cores to be used for the
pipeline execution.  You can also make a dry-run (see what snakemake would do
but without actually really doing anything) by typing

    snakemake -n

To clean all produced data, use

    snakemake -j1 -p clean

## Pipeline visualization / DAG

The entire pipeline can be visualized as a directed acyclic graph (DAG).
The following command creates the DAG as an svg file in the current directory:

    snakemake --dag | dot -Tsvg > dag_rules_full.svg

As the full graph is too packed with information and therefore hardly to grasp,
consider to show only certain parts by disabling some target files in the `all`
rule. Also, a simple rule graph (the one shown above) can be created and saved
in the current directory using

    snakemake --rulegraph | dot -Tsvg > dag_rules_simple.svg

To create a graph in the current directory showing the file dependencies, type

    snakemake --filegraph | dot -Tsvg > dag_files.svg

The graphs also provide information on the completed (solid lines) and pending
(dashed lines) processing steps. For further details see
[Snakemake CLI docs](https://snakemake.readthedocs.io/en/stable/executing/cli.html).

## Snakefiles and config

- The global workflow is defined in the main
  [Snakefile](../workflow/Snakefile).
- It includes the module Snakefiles from the data store located at
  - [store/preprocessed/module.smk](../store/preprocessed/module.smk) and
  - [store/datasets/module.smk](../store/datasets/module.smk)
- In each of these modules, the rules as well as the config from the contained
  datasets are imported.
- These rules include a logging, where further information is collected during
  processing a rule. The log file is located in the same directory as the
  dataset created by the corresponding rule.
