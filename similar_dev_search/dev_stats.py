from collections import defaultdict
from dataclasses import dataclass

from dulwich.repo import Repo

from extract import get_repo_changes
import setup
from utils import compare_ngrams, get_ngrams, get_sorted_dict_by_value


class DevStats:
    def __init__(self,
                 languages=None,
                 variables=None,
                 classes=None,
                 functions=None):
        if functions is None:
            functions = defaultdict(float)
        if classes is None:
            classes = defaultdict(float)
        if variables is None:
            variables = defaultdict(float)
        if languages is None:
            languages = defaultdict(float)
        self.languages = languages
        self.variables = variables
        self.classes = classes
        self.functions = functions

    def update(self, file: dict, commit: dict):
        """
        Update variables', classes' and functions' identifiers for a developer
        :param file: dictionary with identifiers collected from file
        :param commit: dictionary with commit info
        """
        self.languages[file["language"]] = self.languages[file["language"]] + commit["added"]
        if file["lines_number"] == 0:  # prevent division by zero
            return
        weight = commit["added"] / file["lines_number"]
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
        for _, lines in self.languages.items():
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
    def __init__(self, devs=None, mails=None):
        if mails is None:
            mails = defaultdict()
        if devs is None:
            devs = defaultdict(lambda: DevStats())
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
                if commit["author"] not in self.devs:
                    self.devs[commit["author"]] = DevStats()
                # repo_dict[commit_path]["author"] = commit["author"]
                # repo_dict[commit_path]["mail"] = commit["mail"]
                # repo_dict[commit_path]["added"] = commit["added"]
                # repo_dict[commit_path]["deleted"] = commit["deleted"]
                self.devs[commit["author"]].update(repo_dict[commit_path], commit)
                self.mails[commit["mail"]] = commit["author"]

    def find_similar(self, dev_name, k):
        """
        Find similar devs by preferred languages, total lines in each language
        and most used identifiers (by counting weighted ngrams)
        :param dev_name: name of a compared developer
        :param k: number of similar developers
        :return: k similar developers by 3 parameters
        """
        precalculated_dev_lines = self.devs[dev_name].get_experience()
        scores = {}
        for other_dev_name, other_dev_stats in self.devs.items():
            language_distance, dev_lines, other_dev_lines = \
                self.get_language_distribution(dev_name, other_dev_name, precalculated_dev_lines)
            scores[other_dev_name] = \
                {"language_distance": language_distance,
                 "experience": min(dev_lines, other_dev_lines) / max(dev_lines, other_dev_lines),
                 "identifier_similarity": self.get_identifier_similarity(dev_name, other_dev_name)}
        similar_by_language_use = dict(sorted(scores.items(),
                                              key=lambda name, stats: stats["language_distance"]))

    def get_language_distribution(self, compared_dev_name, other_dev_name,
                                  precalculated_dev_lines=-1.0) -> (float, float, float):
        """
        TODO
        :param compared_dev_name:
        :param other_dev_name:
        :param precalculated_dev_lines:
        :return:
        """
        dev_lines = self.devs[compared_dev_name].get_experience() \
            if precalculated_dev_lines == -1.0 else precalculated_dev_lines
        other_dev_lines = self.devs[other_dev_name].get_experience()
        distribution_dev = dict((language, lines / dev_lines)
                                for (language, lines) in
                                self.devs[compared_dev_name].languages.items())
        distribution_other_dev = dict((language, lines / other_dev_lines)
                                      for (language, lines) in
                                      self.devs[other_dev_name].languages.items())
        distance = 0.0
        for language, usage in distribution_dev.items():
            if language not in distribution_other_dev:
                distance += usage
            else:
                distance += abs(usage - distribution_other_dev[language])
        return distance, dev_lines, other_dev_lines

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
