import json
import os
from typing import Any, Dict


def read_json(file_path: str) -> Dict[str, Any]:
    """
    Reads a dictionary from a JSON file.

    :param file_path: Path to the JSON file.
    :return: Dictionary with the data read from the JSON file.
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    else:
        return {}


def write_json(file_path: str, data: Dict[str, Any]) -> None:
    """
    Writes a dictionary to a JSON file.

    :param file_path: Path to the JSON file.
    :param data: Dictionary to write to the JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def write_default_if_not_exist(file_path: str, default_data: Dict[str, Any]) -> None:
    """
    Writes a default dictionary to a JSON file if it does not exist.

    :param file_path: Path to the JSON file.
    :param default_data: Default dictionary to write if the file does not exist.
    """
    if not os.path.exists(file_path):
        write_json(file_path, default_data)
