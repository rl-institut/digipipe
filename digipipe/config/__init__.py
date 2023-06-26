import logging
import os
import sys
from pathlib import Path

from digipipe.scripts.config import read_config


class LevelFilter(logging.Filter):
    """
    Filter class to exclude log records with a specific logging level.
    """

    def __init__(self, level):
        self.level = level
        super(LevelFilter, self).__init__()

    def filter(self, record):
        return record.levelno != self.level


LOGGING_LEVEL = 20  # Corresponds to the severity level "Info"

root_logger = logging.getLogger()
root_logger.handlers.clear()  # Remove the default handler
root_logger.setLevel(LOGGING_LEVEL)

stream_formatter = logging.Formatter("%(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)
stream_handler.addFilter(LevelFilter(logging.ERROR))
root_logger.addHandler(stream_handler)

DEFAULT_LOGFILE = "snake.log"


def add_snake_logger(logging_path, rulename):
    """
    Adds logging to file
    Logfile is read from sys.argv, ending with ".log"
    If this is None it is read from the logging path provided
    This is done in order to add loggers for subprocesses,
    where logfile is unknown.
    """
    logger = logging.getLogger(rulename)

    # Try to obtain logging path from sys.argv and set it to None if can't
    logfile = next((item for item in sys.argv if item.endswith(".log")), None)
    # If logging path not found in sys.argv
    if logfile is None:
        # If path provided calling function
        if logging_path:
            logfile = logging_path
        else:
            logfile = DEFAULT_LOGFILE

    handler = logging.FileHandler(logfile)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(file_formatter)
    logger.addHandler(handler)
    return logger


def locate_global_config() -> Path:
    """Returns path to global config file.

    Raises error when executing the workflow not within `digipipe/` or
    `digipipe/workflow/`.
    """
    config_dir = Path("config", "global.yml")
    cwd = Path(os.getcwd())
    if cwd.name == "digipipe":
        return (cwd / config_dir).resolve()
    elif cwd.name == "workflow":
        return (cwd.parent / config_dir).resolve()
    else:
        raise FileNotFoundError(
            "Global config file not found, make sure you execute the workflow "
            "in digipipe/ or digipipe/workflow/ ."
        )


GLOBAL_CONFIG = {"global": read_config(locate_global_config())}
