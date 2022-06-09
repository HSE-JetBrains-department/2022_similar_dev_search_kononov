import ast
from collections import defaultdict
import json
import os
import platform
import subprocess

from tqdm import tqdm

from extract import logger
from treesitter import queries, save_identifiers

unparseable_languages = set()


def extract_languages(repo_path: str):
    """
    Traverse repository directory, for each programming language file create a json using enry,
    Write json to jsonl file
    :param repo_path: path of extracted repository
    """
    path = os.walk(repo_path)
    file_dict = defaultdict(dict)
    with open("../used_jsons/" + repo_path.split("/")[-1] + ".json", "w") as json_file:
        for root, _, files in tqdm(path):
            for file in files:
                language_json = get_enry_result(root + "/" + file)
                if language_json["language"] != "" and not language_json["vendored"]:
                    add_file_language_info(root, language_json, file_dict)
        json_file.write(json.dumps(file_dict))


def get_enry_result(file_path: str) -> dict:
    """
    Get language, number of lines and vendor info for a file
    :param file_path: path to file
    :return: dictionary with language and number of lines in file
    """
    enry_result = subprocess.check_output(
        [".././enry.exe" if platform.system() == "Windows" else "./enry", "-json",
         file_path], text=True)
    return ast.literal_eval(
        enry_result.replace(":false", ":False").replace(":true", ":True"))


def add_file_language_info(root: str, file_info: dict, repo_dict: dict):
    """

    :param root:
    :param file_info:
    :param repo_dict:
    :return:
    """
    file_info["language"] = file_info["language"].lower()
    if file_info["language"] in queries:
        file_info["path"] = root.replace("\\", "/") \
                            + "/" + file_info["filename"]
        repo_dict[file_info["path"]] = {"language": file_info["language"],
                                        "lines_number": file_info["total_lines"]}
        save_identifiers(file_info["path"], repo_dict)
    elif file_info["language"] not in unparseable_languages:
        logger.error(f"Language {file_info['language']} is not parseable")
        unparseable_languages.add(file_info["language"])


if __name__ == "__main__":
    extract_languages("../scikit-learn/sklearn/svm")
