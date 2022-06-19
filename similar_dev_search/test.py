from stargazers import extract_stargazers
from utils import get_sorted_dict_by_value, split_name_and_mail


def test_stargazers():
    assert extract_stargazers(repo_name="Alex5041/Alex5041.github.io",
                              key="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") \
           == {"Alex5041/Alex5041.github.io": 1}


def test_utils():
    assert split_name_and_mail("Some Name <some mail>") == ("Some Name", "some mail")
    assert get_sorted_dict_by_value({"a": 1, "b": 1.01, "c": 0}) == {"c": 0, "b": 1.01, "a": 1}

def test_pipeline():
    print()


if __name__ == "__main__":
    test_stargazers()
    test_utils()
