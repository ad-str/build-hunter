import json
import re
import sys
import os
import logging


def load_json(file_path):
    """
    Load and return data from a JSON file.
    """
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        logging.error(f" Error reading {file_path}:\n{e}")
        sys.exit(1)


def filter_data(json_data, patterns):
    """
    Filter the JSON data based on the provided regex patterns.
    """
    compiled_pattern = re.compile(patterns)
    return {key: value for key, value in json_data.items() if compiled_pattern.match(key)}


def write_json(file_path, data):
    """
    Write data to a JSON file.
    """
    try:
        with open(file_path, 'w') as out:
            json.dump(data, out, indent=4)
    except Exception as e:
        logging.error(f" Error writing to {file_path}:\n{e}")
        sys.exit(1)


def main(input_path, output_path):
    """
    Main function to load JSON, filter data, and write to a new file.
    """
    json_data = load_json(input_path)
    regex_patterns = '|'.join([
        r'^player_skill_name_msg',
        r'^hyakuryu_skill_name_msg',
        r'^decorations_name_msg',
        r'^decorations$',
        r'^hyakuryu_decos_name_msg',
        r'^hyakuryu_decos$',
        r'^armor$',
        r'^armor_.+_name_msg'
    ])
    filtered_data = filter_data(json_data, regex_patterns)
    write_json(output_path, filtered_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_file_path = sys.argv[1] if len(sys.argv) > 1 else './data/mhric.json'
    output_file_path = sys.argv[2] if len(
        sys.argv) > 2 else './data/filtered.json'
    main(input_file_path, output_file_path)
