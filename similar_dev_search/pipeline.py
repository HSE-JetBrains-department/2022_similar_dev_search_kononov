import json
import os

from dulwich import porcelain

from dev_stats import AllDevStats
from parsefile import extract_languages
import setup


def pipeline(repos_list_path: str, results_path: str):
    """
    1. For each repository, run parsefile.py on head revision, creating
    a dictionary {file_name: {language, total_lines}}

    2. Run parsefile.py to add variable names and imports to dictionary from previous step.
    Optimally, run tree-sitter on an already received bytes (to prevent opening file twice,
    unfortunately not possible because enry is executed with subprocess)

    3. Run extract.py to extract commits

    4. For each commit change (that has a file in current head revision),
    call add_file_to_dev_stats from dev-stats.py
    """
    cloned_repos = os.listdir(setup.repo_folder)
    all_dev_stats = AllDevStats()
    with open(repos_list_path, "r") as file_with_repos:
        repos_list = json.loads(file_with_repos.read()).keys()
    for key in repos_list:
        key_without_slashes = key.replace("/", "-")
        if key_without_slashes not in cloned_repos:
            porcelain.clone("https://github.com/" + key,
                            setup.repo_folder / key_without_slashes)
        repo_dict = extract_languages(
            setup.repo_folder / key_without_slashes)  # 1, 2. Add identifiers
        # 3. Extract commits, 4. Add dev stats
        all_dev_stats.repo_to_dev_stats(key_without_slashes,
                                        "https://github.com/" + key,
                                        repo_dict)
    with open(results_path, "w") as file_with_results:
        file_with_results.write(json.dumps(all_dev_stats.to_json()))
