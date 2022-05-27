import ast
import json
import os
import subprocess

from tqdm import tqdm


# 151.3629 if json.loads
# 133.6954357624054 if ast.literal_eval
def extract_languages(repo_path, json_path):
    """
    Extract programming language jsons into jsonl file
    :param repo_path: path of extracted repository
    :param json_path: path to jsonl file
    """
    path = os.walk(repo_path)
    with open(json_path, "w") as json_file:
        for root, _, files in tqdm(path):
            for file in files:
                enry_result = subprocess.check_output(
                    ["./enry.exe", "-json", root + "/" + file], text=True)
                language_json = ast.literal_eval(
                    enry_result.replace(":false", ":False").replace(":true", ":True"))
                if language_json["language"] != "":
                    language_json["path"] = root.replace("\\", "/") \
                                            + "/" + language_json["filename"]
                    del language_json["filename"]
                    json_file.write(json.dumps(language_json) + "\n")
