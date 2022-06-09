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
    author = dev_stats[file["author"]]
    if author is None:
        dev_stats[file["author"]] = {"languages": Counter(), "names": Counter()}
        author = dev_stats[file["author"]]
    author["languages"][file["language"]] += file["added"]
    weight = file["added"] / file["lines"]
    for name in file["names"]:
        # if currently file has fewer lines than author added, weight > 1 - bad case.
        author["names"][name.key] += min(1, weight) * name.value
