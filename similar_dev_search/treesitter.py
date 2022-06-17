from collections import Counter

import tree_sitter
from tree_sitter import Language

are_parsers_ready: bool = None
LANGUAGES: dict
QUERIES: dict


class SingletonParser:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = tree_sitter.Parser()
        return cls.instance


parser = SingletonParser()


def save_identifiers(path: str, repo_dict: dict):
    """
    Write file identifiers to a count dictionary
    :param repo_dict: dictionary with info (number of lines, language and identifiers)
    about files inside it
    :param path: path to file
    """
    parser.set_language(LANGUAGES[repo_dict[path]["language"]])
    query = QUERIES[repo_dict[path]["language"]]
    with open(path, "r") as file:
        code = bytes(file.read(), "utf8")
    ident_vector = {"variables": Counter(), "classes": Counter(), "functions": Counter()}
    for index, identifier in enumerate(query.captures(parser.parse(code).root_node)):
        node = identifier[0]
        capture_type = identifier[1]
        ident = code[node.start_byte: node.end_byte].decode()
        ident_vector["variables" if capture_type == "var_name" else (
            "classes" if capture_type == "class_name" else "functions")][ident] += 1
    repo_dict[path].update(ident_vector)


def set_parsers():
    """
    Function to set parsers once for each import of this file
    """
    global LANGUAGES, QUERIES, are_parsers_ready
    if are_parsers_ready is None:
        LANGUAGES = {"python": Language("../build/my-languages.so", "python"),
                     "go": Language("../build/my-languages.so", "go"),
                     "javascript": Language("../build/my-languages.so", "javascript")}
        QUERIES = {"python": LANGUAGES["python"].query("""
                (assignment left: (identifier) @var_name)
                (class_definition name: (identifier) @class_name)
                (function_definition name: (identifier) @func_name)
               """),
                   "go": LANGUAGES["go"].query("""
                   (short_var_declaration left: (expression_list (identifier)) @var_name)
                   (type_spec name: (type_identifier) @class_name)
                   (function_declaration name: (identifier) @func_name)
                   """),
                   "javascript": LANGUAGES["javascript"].query("""
                (variable_declarator name: (identifier) @var_name)
                (class_declaration name: (identifier) @class_name)
                (function_declaration name: (identifier) @func_name)
               """)}
        are_parsers_ready = True


set_parsers()
