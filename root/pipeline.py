import json
import os

from dulwich import porcelain

from enry import extract_languages
from extract import repo_to_json


def pipeline():
    """
    1. Run stargazers.py to find repositories

    2. For each repository from a previous step, run enry.py on head revision, creating
    a dictionary {file_name: {language, total_lines}}

    3. Run treesitter.py to add variable names and imports to dictionary from previous step.
    Optimally, run tree-sitter on an already received bytes (to prevent opening file twice,
    unfortunately not possible because enry is executed with subprocess)

    4. Run extract.py to extract commits

    5. For each commit change (that has a file in current head revision),
    call add_file_to_dev_stats from dev-stats.py
    """
    clone_found_repos()  # 1, 2, 3, 4


def find_similar():
    print()


def clone_found_repos():
    cloned_repos = os.listdir("../repos")
    extracted_repos = os.listdir("../used_jsons")
    with open("../used_jsons/stargazers.json", "r") as file:
        repos_list = map(lambda repo_name: repo_name.replace("/", "-"),
                         json.loads(file.read()).keys())
        # repos_list = list(filter(lambda repo_name: repo_name not in cloned_repos, repos_list))
        for key in repos_list:
            if key not in cloned_repos:
                porcelain.clone("git://github.com/" + key, "../repos/" + key)
            extract_languages("../repos/" + key)  # 3. Add identifiers
            # 4. Extract commits
            if key not in extracted_repos:
                repo_to_json(key, "https://github.com/", "../used_jsons/" + key)
