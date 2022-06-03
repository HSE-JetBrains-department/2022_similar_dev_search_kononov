from collections import Counter
import json

from tree_sitter import Language, Parser

languages = {"python": Language("build/my-languages.so", "python"),
             "go": Language("build/my-languages.so", "go"),
             "javascript": Language("build/my-languages.so", "javascript")}


def save_identifiers(path: str, json_path, code: bytes = None, language_name: str = "python"):
    """
    Write file identifiers to json in form of a count dictionary
    :param path: path to file
    :param json_path: path to created json
    :param code: (optional) bytes of code, from which extraction of identifiers happen
    :param language_name: name of a used language
    :return: created count dictionary
    """
    parser = Parser()
    parser.set_language(languages[language_name])
    query = languages[language_name].query("""
       (
       (identifier) @all_identifiers
       )
       """)
    if code is None:
        with open(path, "r") as file:
            code = bytes(file.read(), "utf8")
    ident_vector = Counter()
    with open(json_path, "w") as json_file:
        for index, identifier in enumerate(query.captures(parser.parse(code).root_node)):
            node = identifier[0]
            ident = code[node.start_byte: node.end_byte].decode()
            ident_vector[ident] += 1
        json_file.write(json.dumps(ident_vector))
    return ident_vector
