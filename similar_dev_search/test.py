from unittest import TestCase

import utils


class Test(TestCase):
    def test_utils(self):
        assert utils.split_name_and_mail("Some Name <some mail>") == ("Some Name", "some mail")
        assert utils.get_sorted_dict_by_value({"a": 1, "b": 1.01, "c": 0}) \
               == {"c": 0, "b": 1.01, "a": 1}
        assert list(utils.get_ngram("abcdefgh", 3)) == ["abc", "bcd", "cde", "def", "efg", "fgh"]
        assert list(utils.get_ngram("ab", 2)) == ["ab"]
        assert list(utils.get_ngram("a", 2)) == []
