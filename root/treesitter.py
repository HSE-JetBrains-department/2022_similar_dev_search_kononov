from collections import Counter

from tree_sitter import Language, Parser

languages = {"python": Language("../build/my-languages.so", "python"),
             "go": Language("../build/my-languages.so", "go"),
             "javascript": Language("../build/my-languages.so", "javascript")}
#             "java": Language("../build/my-languages.so", "java")}
queries = {"python": Language("../build/my-languages.so", "python").query("""
        (assignment left: (identifier) @var_name)
        (class_definition name: (identifier) @class_name)
        (function_definition name: (identifier) @func_name)
       """),
           "go": Language("../build/my-languages.so", "go"),
           "javascript": Language("../build/my-languages.so", "javascript").query("""
        (variable_declarator name: (identifier) @var_name)
        (class_declaration name: (identifier) @class_name)
        (function_declaration name: (identifier) @func_name)
       """)}
#     "java": Language("../build/my-languages.so", "java").query("""
#  (
#  variable_declarator name: (identifier) @var_name
#  class_declaration name: (identifier) @class_name
#  method_declaration name: (identifier) @func_name
#  )
# """)}
parser = Parser()


def save_identifiers(path: str, repo_dict: dict):
    """
    Write file identifiers to a count dictionary
    :param repo_dict: dictionary with info (number of lines, language and identifiers)
    about files inside it
    :param path: path to file
    """
    parser.set_language(languages[repo_dict[path]["language"]])
    query = queries[repo_dict[path]["language"]]
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
