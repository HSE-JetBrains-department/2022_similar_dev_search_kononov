from collections import Counter

dev_stats = {}
"""
dictionary with devs containing for each dev:

* counter of languages (language: number of lines)

* counter of imports

* counter of variable names
"""


def add_file_to_dev_stats(file: dict):
    """
    Add file commit

    * identifiers,

    * and language lines

    to a respective developer
    :param file: added file
    """
    if file["author"] not in dev_stats:
        dev_stats[file["author"]] = {"languages": Counter(), "variables": Counter(),
                                     "classes": Counter(), "functions": Counter()}
    author = dev_stats[file["author"]]
    author["languages"][file["language"]] += file["added"]
    weight = file["added"] / file["lines_number"]
    for identifier in ["variables", "classes", "functions"]:
        for name in file[identifier]:
            # if currently file has fewer lines than author added, weight > 1 - bad case.
            author[identifier][name] += min(1, weight) * file[identifier][name]
