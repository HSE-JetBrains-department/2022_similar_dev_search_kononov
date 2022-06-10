import json
import os

from dulwich import porcelain

from enry import extract_languages
from extract import repo_to_json
from dev_stats import dev_stats

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
    cloned_repos = os.listdir("../repos")
    extracted_repos = os.listdir("../used_jsons")
    with open("../used_jsons/repos.json", "r") as file:
        repos_list = map(lambda repo_name: repo_name.replace("/", "-"),
                         json.loads(file.read()).keys())
        for key in repos_list:
            if key not in cloned_repos:
                porcelain.clone("git://github.com/" + key, "../repos/" + key)
            repo_dict = extract_languages("../repos/" + key)  # 3. Add identifiers
            # 4. Extract commits, 5. Add dev stats
            repo_to_json(key, "https://github.com/", "../used_jsons/" + key, repo_dict)
    with open("../used_jsons/dev_stats.json","w") as file:
        file.write(json.dumps(dev_stats))


def find_similar():
    print()


def setup():
    dirs = os.listdir("../")


if __name__ == "__main__":
    pipeline()