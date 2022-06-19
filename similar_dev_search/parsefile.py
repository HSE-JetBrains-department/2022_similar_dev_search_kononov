from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import platform
import subprocess
from typing import Dict

from tqdm import tqdm
import tree_sitter
from tree_sitter import Language

from setup import enry_folder, logger

LANGUAGES = {"python": Language("../build/my-languages.so", "python"),
             "go": Language("../build/my-languages.so", "go"),
             "javascript": Language("../build/my-languages.so", "javascript")}
QUERIES = {"python": LANGUAGES["python"].query("""
             (assignment left: (identifier) @var_name)
             (class_definition name: (identifier) @class_name)
             (function_definition name: (identifier) @func_name)
            """),
           "go": LANGUAGES["go"].query("""
                (short_var_declaration left: (expression_list (identifier)) @var_name)
                (type_spec name: (type_identifier) @class_name)
                (function_declaration name: (identifier) @func_name)
                """),
           "javascript": LANGUAGES["javascript"].query("""
             (variable_declarator name: (identifier) @var_name)
             (class_declaration name: (identifier) @class_name)
             (function_declaration name: (identifier) @func_name)
            """)}


class SingletonParser:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = tree_sitter.Parser()
        return cls.instance


parser = SingletonParser()
unparseable_languages = set()


def get_identifiers(path: str, language: str) -> Dict[str, Counter]:
    """
    Get file identifiers (variable, class and function names) in a form of a count dictionary
    :param path: path to file
    :param language: language of file
    """
    parser.set_language(LANGUAGES[language])
    query = QUERIES[language]
    with open(path, "r") as file:
        code = bytes(file.read(), "utf8")
    ident_vector = {"variables": Counter(), "classes": Counter(), "functions": Counter()}
    for index, identifier in enumerate(query.captures(parser.parse(code).root_node)):
        node = identifier[0]
        capture_type = identifier[1]
        ident = code[node.start_byte: node.end_byte].decode()
        ident_vector["variables" if capture_type == "var_name" else (
            "classes" if capture_type == "class_name" else "functions")][ident] += 1
    return ident_vector


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
        repo_dict[file_info["path"]].update(
            get_identifiers(file_info["path"], file_info["language"]))
    elif file_info["language"] not in unparseable_languages:
        logger.error(f"Language {file_info['language']} is not parseable")
        unparseable_languages.add(file_info["language"])


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


def extract_languages(repo_path: Path):
    """
    Traverse repository directory, for each programming language file create a json using enry,
    write json to jsonl file
    :param repo_path: path of extracted repository
    """
    path = os.walk(repo_path)
    file_dict = defaultdict(dict)
    for root, _, files in tqdm(path):
        root = Path(root)
        for file in files:
            language_json = get_enry_result(root / file)
            if language_json["language"] != "" and not language_json["vendored"]:
                add_file_language_info(root, language_json, file_dict)
    return file_dict
