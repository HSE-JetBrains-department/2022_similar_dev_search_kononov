from collections import defaultdict
import json
import os
from pathlib import Path
import platform
import subprocess

from tqdm import tqdm

from globals import enry_folder, logger, repo_info_folder
from treesitter import QUERIES, save_identifiers

unparseable_languages = set()


def extract_languages(repo_path: Path):
    """
    Traverse repository directory, for each programming language file create a json using enry,
    write json to jsonl file
    :param repo_path: path of extracted repository
    """
    path = os.walk(repo_path)
    file_dict = defaultdict(dict)
    with open(repo_info_folder / (repo_path.stem + ".json"), "w") as json_file:
        for root, _, files in tqdm(path):
            root = Path(root)
            for file in files:
                language_json = get_enry_result(root / file)
                if language_json["language"] != "" and not language_json["vendored"]:
                    add_file_language_info(root, language_json, file_dict)
        json_file.write(json.dumps(file_dict))
    return file_dict


def get_enry_result(file_path: str) -> dict:
    """
    Get language, number of lines and vendor info for a file
    :param file_path: path to file
    :return: dictionary with language and number of lines in file
    """
    enry_result = subprocess.check_output(
        [str(enry_folder) + "/./enry.exe" if platform.system() == "Windows"
         else str(enry_folder) + "/./enry", "-json",
         file_path], text=True)
    return json.loads(enry_result)


def add_file_language_info(root: Path, file_info: dict, repo_dict: dict):
    """
    Add information about file received from enry call
    :param root: path to root directory of repository
    :param file_info: dictionary with file information
    :param repo_dict: dictionary conatining file_info dictionaries for its files
    """
    file_info["language"] = file_info["language"].lower()
    if file_info["language"] in QUERIES:
        file_info["path"] = str(root / file_info["filename"])
        repo_dict[file_info["path"]] = {"language": file_info["language"],
                                        "lines_number": file_info["total_lines"]}
        save_identifiers(file_info["path"], repo_dict)
    elif file_info["language"] not in unparseable_languages:
        logger.error(f"Language {file_info['language']} is not parseable")
        unparseable_languages.add(file_info["language"])
