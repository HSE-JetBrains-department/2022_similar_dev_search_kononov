import ast
import json
import os
import platform
import subprocess

from tqdm import tqdm


def extract_languages(repo_path: str, json_path: str):
    """
    Traverse repository directory, for each programming language file create a json using enry,
    Write json to jsonl file
    :param repo_path: path of extracted repository
    :param json_path: path to jsonl file
    """
    path = os.walk(repo_path)
    with open(json_path, "w") as json_file:
        for root, _, files in tqdm(path):
            for file in files:
                enry_result = subprocess.check_output(
                    ["./enry.exe" if platform.system() == "Windows" else "./enry", "-json",
                     root + "/" + file], text=True)
                language_json = ast.literal_eval(
                    enry_result.replace(":false", ":False").replace(":true", ":True"))
                if language_json["language"] != "":
                    language_json["path"] = root.replace("\\", "/") \
                                            + "/" + language_json["filename"]
                    del language_json["filename"]
                    json_file.write(json.dumps(language_json) + "\n")
