import json

from dev_stats import DevStats, AllDevStats


def search(dev_name: str, stats_path: str):
    """
    Search can be done by three categories:
    preferred language (language lines are nearest in relation to each other),
    similar experience (overall lines is most near),
    same identifiers by n gram
    :param stats_path:
    :param dev_name:
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
    dev_stats =
    scores = {}
    for dev in dev_stats["devs"]:
        scores[dev] = get_scores(dev_name, dev, stats["devs"])




def get_ngrams(dev_dict) -> dict:
    print()


def get_dev_stats(dev_name: str):
    """
    Get dev preferred languages, total lines in each language and most used identifiers
    :param dev_name: name of developer
    """
