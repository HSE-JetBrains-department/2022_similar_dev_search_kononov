import argparse

from extract import repo_to_json, save_to_json
from stargazers import extract_stargazers


def add_extract_command(subparsers_action: argparse.Action):
    """
    Add subparser for repository extraction
    :param subparsers_action: exposed action of main parser
    """
    extract_parser = subparsers_action.add_parser("extract")
    extract_parser.add_argument("-rn", "--repo-name", type=str,
                                help="Name of extracted repository")
    extract_parser.add_argument("-ru", "--repo-url", type=str, help="Url of extracted repository")
    extract_parser.add_argument("-j", "--json-name", type=str,
                                help="File name where repository data is stored")
    extract_parser.add_argument("-rp", "--repo-path", type=str,
                                help="Path of repository with stargazers")


def add_stargazers_command(subparsers_action: argparse.Action):
    """
    Add subparser for getting top repositories that stargazers starred
    :param subparsers_action: exposed action of main parser
    """
    stargazers_parser = subparsers_action.add_parser("stargazers")
    stargazers_parser.add_argument("-rp", "--repo-path", type=str,
                                   help="Path of repository with stargazers.")
    stargazers_parser.add_argument("-k", "--key", type=str,
                                   help="Path of repository with stargazers")
    stargazers_parser.add_argument("-rpu", "--repos-per-user", type=str,
                                   help="Path of repository with stargazers")
    stargazers_parser.add_argument("-sn", "--stargazers-number", type=str,
                                   help="Path of repository with stargazers")
    stargazers_parser.add_argument("-tr", "--top-repos-number", type=str,
                                   help="Path of repository with stargazers")
    stargazers_parser.add_argument("-rp", "--repos-per-page", type=str,
                                   help="Path of repository with stargazers")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract repository.")
    subparsers = parser.add_subparsers()
    add_extract_command(subparsers)

    args = parser.parse_args()
    print(args)

    if args.repo_path is None:
        repo_to_json(args.repo_name, args.repo_url, args.json_name)
    else:
        save_to_json(extract_stargazers(args.repo_path,
                                        args.key,
                                        args.repos_per_user,
                                        args.top_repos_number,
                                        ), "")
