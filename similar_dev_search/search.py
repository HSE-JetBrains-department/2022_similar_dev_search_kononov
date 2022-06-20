import json

from dev_stats import AllDevStats, DevStats
from utils import dict_keys_to_string


def search(dev_name: str, stats_path: str,
           number_of_similar_devs: int = 5,
           number_of_top_identifiers: int = 5):
    """
    Search is done by three categories:
    similar languages (language lines are nearest in relation to each other),
    similar experience (overall lines is most near),
    same identifiers by n gram. Function will print search result
    :param stats_path: path to file with developer stats
    :param dev_name: name of developers for which similar are searched
    :param number_of_similar_devs: if bigger than overall developer number, will print
    all developers
    :param number_of_top_identifiers: if bigger than total number of identifiers, will print total
    """
    with open(stats_path, "r") as stats_file:
        dicts_with_stats = json.loads(stats_file.read())
    if dev_name not in dicts_with_stats["devs"]:
        raise ValueError(f"No developer with name {dev_name} found")
    stats = dict((name, DevStats(languages=info["languages"],
                                 variables=info["variables"],
                                 classes=info["classes"],
                                 functions=info["functions"]))
                 for (name, info) in dicts_with_stats["devs"].items())
    all_dev_stats = AllDevStats(stats, dicts_with_stats["mails"])
    print(get_developer_info(all_dev_stats.devs[dev_name], number_of_top_identifiers))
    if len(all_dev_stats.devs) == 1:
        print("No other developers to find similar from")
        return
    similar = all_dev_stats.find_similar(dev_name, number_of_similar_devs)
    for metric in similar:
        print(f"Developers similar by {metric}:")
        print(", ".join(similar[metric]))


def get_developer_info(dev_stats: DevStats, identifiers_number: int):
    """
    Get information about developer including used languages,
    variable, function and class identifiers
    :param dev_stats: class with developers statistics used for information extraction
    :param identifiers_number: number of returned identifiers
    :return: string representing developers by its languages and identifiers
    """
    return f"Developer used languages:\n" \
           f"{dict_keys_to_string(dev_stats.languages, len(dev_stats.languages))}\n" \
           f"Developer top variable identifiers:\n" \
           f"{dict_keys_to_string(dev_stats.variables, identifiers_number)}\n" \
           f"Developer top function identifiers:\n" \
           f"{dict_keys_to_string(dev_stats.functions, identifiers_number)}\n" \
           f"Developer top class identifiers:\n" \
           f"{dict_keys_to_string(dev_stats.classes, identifiers_number)}"
