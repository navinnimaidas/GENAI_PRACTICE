"""utility package file for the project."""

import logging
import os
import warnings

from box import Box
import yaml

warnings.filterwarnings("ignore")


# Function to read YAML file
def read_yaml_file(file_path) -> Box:  # noqa: ANN001
    """
    Read a YAML file and return its contents as a Box object.

    Parameters:
    - file_path (str): The path to the YAML file.

    Returns:
    - Box: A Box object containing the parsed YAML data.
    """
    with open(file_path) as file:
        data = yaml.safe_load(file)
    return Box(data)


def save_dataframe(df, file_path) -> None:  # noqa: ANN001
    """
    Save DataFrame to the specified file path. Create directories if they do not exist.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to be saved.
    - file_path (str): The path where the DataFrame will be saved.
    """
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the DataFrame to the specified file path
    df.to_csv(file_path, index=False)


class CustomLogger:
    """
    A custom logger class for logging messages to a file.

    Attributes:
    ----------
    logger : logging.Logger
        The logger instance used for logging messages.

    Methods:
    -------
    debug(message: str) -> None
        Log a debug message.
    info(message: str) -> None
        Log an info message.
    warning(message: str) -> None
        Log a warning message.
    error(message: str) -> None
        Log an error message with exception info.
    critical(message: str) -> None
        Log a critical message.
    """

    def __init__(self, log_file: str = "RUNNING_LOGGS.log") -> None:
        self.logger = logging.getLogger("CustomLogger")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create a console handler and set level to debug
        log_folder = "Loggings"
        if log_folder and not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file = os.path.join(log_folder, log_file)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def debug(self, message: str) -> None:  # noqa: D102
        self.logger.debug(message)

    def info(self, message: str) -> None:  # noqa: D102
        self.logger.info(message)

    def warning(self, message: str) -> None:  # noqa: D102
        self.logger.warning(message)

    def error(self, message: str) -> None:  # noqa: D102
        self.logger.error(message, exc_info=True)

    def critical(self, message: str) -> None:  # noqa: D102
        self.logger.critical(message)


logger = CustomLogger()
