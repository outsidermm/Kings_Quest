import json
import os


def read_json(file_path):
    """Reads a dictionary from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    else:
        return {}


def write_json(file_path, data):
    """Writes a dictionary to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def write_default_if_not_exist(file_path, default_data):
    """Writes a default dictionary to a JSON file if it does not exist."""
    if not os.path.exists(file_path):
        write_json(file_path, default_data)
