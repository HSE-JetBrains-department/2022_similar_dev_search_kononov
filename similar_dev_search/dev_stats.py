from collections import defaultdict
from dataclasses import dataclass

from dulwich.repo import Repo

from extract import get_repo_changes
import setup
from utils import compare_ngrams, get_ngrams, get_sorted_dict_by_value


@dataclass
class DevStats:
    def __init__(self,
                 languages=defaultdict(float),
                 variables=defaultdict(float),
                 classes=defaultdict(float),
                 functions=defaultdict(float)):
        self.languages = languages
        self.variables = variables
        self.classes = classes
        self.functions = functions

    def update(self, file: dict):
        """
        Update variables', classes' and functions' identifiers for a developer
        :param file: dictionary with identifiers collected from file
        """
        self.languages[file["language"]] = self.languages[file["language"]] + file["added"]
        weight = file["added"] / file["lines_number"]
        for key in file["variables"]:
            self.variables[key] += file["variables"][key] * min(1, weight)
        for key in file["classes"]:
            self.classes[key] += file["classes"][key] * min(1, weight)
        for key in file["functions"]:
            self.functions[key] += file["functions"][key] * min(1, weight)

    def get_experience(self) -> float:
        """
        Get total lines coded.
        :return: total_lines in alll languages
        """
        total_lines = 0.0
        for _, lines in self.languages:
            total_lines += lines
        return total_lines

    def get_ngrams(self, n=3) -> (dict, int):
        """
        TODO
        :param n:
        :return:
        """
        all_idents = dict(self.languages)
        all_idents.update(self.classes)
        all_idents.update(self.variables)
        all_idents.update(self.functions)
        return get_ngrams(all_idents, n)

    def to_json(self):
        """
        Create dictionary of DevStats instance for json serialization
        :return: json-serializable dict with dev stats
        """
        return {"languages": get_sorted_dict_by_value(self.languages),
                "variables": get_sorted_dict_by_value(self.variables),
                "classes": get_sorted_dict_by_value(self.classes),
                "functions": get_sorted_dict_by_value(self.functions)}


@dataclass
class AllDevStats:
    def __init__(self, devs=defaultdict(lambda: DevStats()), mails=defaultdict()):
        self.devs = devs
        self.mails = mails

    def repo_to_dev_stats(self, name: str, url: str, repo_dict: dict):
        """
        Extract repository info to developer stats
        :param name: repository name
        :param url: repository GitHub url
        :param repo_dict: dictionary with paths of files in head revision
        """
        repo = Repo(setup.repo_folder / name)
        for commit in get_repo_changes(repo, url):
            commit_path = str(setup.repo_folder / name / commit["path"])
            if commit_path in repo_dict:
                repo_dict[commit_path]["author"] = commit["author"]
                repo_dict[commit_path]["mail"] = commit["mail"]
                repo_dict[commit_path]["added"] = commit["added"]
                repo_dict[commit_path]["deleted"] = commit["deleted"]
                self.devs[repo_dict[commit_path]["author"]].update(repo_dict[commit_path])
                self.mails[commit["mail"]] = commit["author"]

    def get_scores(self, compared_dev_name, other_dev_name) -> dict:
        dev_lines = self.devs[compared_dev_name].get_experience()
        other_dev_lines = self.devs[other_dev_name].get_experience()
        result = {"languages_distribution": "",
                  "experience": min(dev_lines, other_dev_lines) / max(dev_lines, other_dev_lines),
                  "identifier_similarity":
                      self.get_identifier_similarity(compared_dev_name, other_dev_name)}
        return result

    def get_language_distribution(self):

    def get_identifier_similarity(self, compared_dev_name, other_dev_name) -> float:
        """
        TODO
        :param compared_dev_name:
        :param other_dev_name:
        :return:
        """
        dev1_ngrams, sum_weight1 = self.devs[compared_dev_name].get_ngrams()
        dev2_ngrams, sum_weight2 = self.devs[other_dev_name].get_ngrams()
        return compare_ngrams(dev1_ngrams, dev2_ngrams) / sum_weight1

    def to_json(self):
        """
        Create dictionary of AllDevStats instance for json serialization
        :return: json-serializable dict containing all dev stats
        """
        return {"devs": {key: value.to_json() for key, value in self.devs.items()},
                "mails": dict(self.mails)}
