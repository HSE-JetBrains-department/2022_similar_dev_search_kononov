from collections import defaultdict
from typing import Tuple


def split_name_and_mail(name_and_mail: str) -> Tuple:
    """
    Split name and email and return them separately
    :param name_and_mail: string with name and mail
    :return: name, mail
    """
    array = name_and_mail.split(" <")
    name = array[0]
    mail = array[1][:array[1].rindex(">")]
    return name, mail


def get_sorted_dict_by_value(arg: dict) -> dict:
    """
    Sort dictionary by its value
    :param arg: dictionary to sort
    :return: sorted arg
    """
    return dict(sorted(arg.items(), key=lambda item: item[1], reverse=True))


def get_ngrams(word_dict: dict, n: int) -> (dict, int):
    """
    Get all ngrams from a dictionary with weighted words
    :param word_dict: dictionary with words and weights
    :param n: length of ngram
    :return: dictionary with ngrams and respective weights and overall weight
    """
    result = defaultdict(float)
    overall_weight = 0.0
    for ident in word_dict:
        for ngram in get_ngram(ident, n):
            result[ngram] = result[ngram] + word_dict[ident]
            overall_weight += word_dict[ident]
    return result, overall_weight


def get_ngram(ident: str, n: int):
    """
    Get ngram from a string
    :param ident: string that is decomposed into ngrams
    :param n: length of ngram
    :return: all ngrams of string
    """
    ident_len = len(ident) - n + 1
    for i in range(ident_len):
        yield ident[i:i + n]


def get_ngrams_dict_overlap(ngrams1: dict, ngrams2: dict) -> float:
    """
    Sum minimal scores for each ngram in two dictionaries
    :param ngrams1: first dict with ngrams and scores
    :param ngrams2: second dict with ngrams and socres
    :return: counted score
    """
    score = 0.0
    for ngram, weight in ngrams1.items():
        if ngram in ngrams2:
            score += min(weight, ngrams2[ngram])
    return score


def get_top_k_from_devs_by_metric(devs: dict, metric: str, k: int, reversed: bool) -> list:
    """
    Get list of names of top developers by metric
    :param devs: dictionary with developer names and DevStats
    :param metric: metric to sort by
    :param k: number of top names to return
    :param reversed: reverse sorted list if true
    :return: k top developer names by metric
    """
    tuple_list = sorted(devs.items(), key=lambda item: item[1][metric], reverse=reversed)
    return [name_stats[0] for name_stats in tuple_list][:k]


def dict_keys_to_string(dictionary: dict, limit: int, sep="\n") -> str:
    """
    Format dictionary keys to string
    :param dictionary: dictionary to format into string
    :param limit: number of first keys to return
    :param sep: separator to use between keys
    :return: string of dictionary keys
    """
    if len(dictionary) == 0:
        return "(NONE)"
    return sep.join([key for key in dictionary][:limit])
