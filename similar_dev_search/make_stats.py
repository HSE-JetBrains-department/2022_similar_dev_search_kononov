import json
import os

from dulwich import porcelain
from dulwich.client import HTTPUnauthorized

from dev_stats import AllDevStats
from parsefile import extract_languages
import setup


def make_stats(repos_list_path: str, results_path: str):
    """
    1. Clone all unsaved repositories.
    2. For each repository, run parsefile.py on head revision, creating
    a dictionary {file_name: {language, total_lines}}
    3. Run parsefile.py to add variable, class, function identifiers to dictionary
    from previous step.
    4. Run extract.py to extract commits
    5. For each commit change (that has a file in current head revision),
    call add_file_to_dev_stats from dev-stats.py
    """
    cloned_repos = os.listdir(setup.repo_folder)
    all_dev_stats = AllDevStats()
    with open(repos_list_path, "r") as file_with_repos:
        repos_list = json.loads(file_with_repos.read()).keys()
    for key in repos_list:
        key_without_slashes = key.replace("/", "-")
        if key_without_slashes not in cloned_repos:  # 1. Clone repository
            try:
                porcelain.clone("https://github.com/" + key,
                                setup.repo_folder / key_without_slashes)
            except FileNotFoundError:
                setup.logger.error(f"repository {key} not cloneable")
                continue
            except HTTPUnauthorized:
                setup.logger.error(f"repository {key} not found")
                continue
        # 2, 3. Add identifiers
        repo_dict = extract_languages(setup.repo_folder / key_without_slashes)
        # 4. Extract commits, 5. Add dev stats
        all_dev_stats.repo_to_dev_stats(key_without_slashes, "https://github.com/" + key,
                                        repo_dict)
    with open(results_path, "w") as file_with_results:
        file_with_results.write(json.dumps(all_dev_stats.to_json()))
