from collections import defaultdict
from dataclasses import dataclass


@dataclass
class DevStats:
    languages = defaultdict(float)
    variables = defaultdict(float)
    classes = defaultdict(float)
    functions = defaultdict(float)

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

    def __str__(self):
        return f"""
        languages:{dict(self.languages)},
        variables: {dict(self.variables)},
        classes: {dict(self.classes)},
        functions: {dict(self.functions)}"""

    def __repr__(self):
        return self.__str__()


"""
Dictionary with devs containing dev stats
"""
stats = defaultdict(lambda: DevStats())


def add_file_to_dev_stats(file: dict):
    """
    Add file commit to a respective developer
    :param file: added file dictionary
    """
    stats[file["author"]].update(file)
