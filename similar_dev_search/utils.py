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
    Sort dictionary
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
            result[ngram] += result[ngram] + word_dict[ident]
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


def compare_ngrams(ngrams1: dict, ngrams2: dict) -> float:
    """
    TODO
    :param ngrams1:
    :param ngrams2:
    :return:
    """
    score = 0.0
    for ngram, weight in ngrams1.items():
        score += min(weight, ngrams2[ngram])
    return score
