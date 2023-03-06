"""
Helper functions for the workflow
"""


def search_data_workflows():
    """Search for snakefiles (*.smk) in data store but exclude templates.

    TODO: Used in outdated manual importing of snakemake files.
    TODO: Remove, if modularization works out.

    Returns
    -------
    list
        Paths to Snakemake files
    """
    # smk_files = []
    # for root, dirs, files in os.walk(get_abs_store_root_path()):
    #     for file in files:
    #         if file.endswith(".smk") and ".TEMPLATE" not in str(root):
    #             smk_files.append(Path(os.path.join(root, file)))
    # return smk_files
    raise NotImplementedError
