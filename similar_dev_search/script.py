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


def add_stargazers_command(subparsers_action: argparse.Action):
    """
    Add subparser for getting top repositories that stargazers starred
    :param subparsers_action: exposed action of main parser
    """
    stargazers_parser = subparsers_action.add_parser("stargazers")
    stargazers_parser.add_argument("-rp", "--repo-path", type=str,
                                   help="Path of repository with stargazers.")
    stargazers_parser.add_argument("-k", "--key", type=str,
                                   help="Github token")
    stargazers_parser.add_argument("-rpu", "--repos-per-user", type=str,
                                   help="Number of starred repositories for user")
    stargazers_parser.add_argument("-sn", "--stargazers-number", type=str,
                                   help="Number of stargazers")
    stargazers_parser.add_argument("-tr", "--top-repos-number", type=str,
                                   help="Number of repositories with most stars")
    stargazers_parser.add_argument("-rp", "--repos-per-page", type=str,
                                   help="Number of requests on each page")
    stargazers_parser.add_argument("-j", "--json-name", type=str,
                                   help="File name where stargazers` data is stored")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract repository.")
    subparsers = parser.add_subparsers()
    add_extract_command(subparsers)

    args = parser.parse_args()
    print(vars(args))

    if 'repo_path' in vars(args):
        stargazers_map = extract_stargazers(repo_name=args.repo_path,
                                            key=args.key,
                                            repos_per_user=args.repos_per_user,
                                            top_repos_number=args.top_repos_number,
                                            )
        with open(args.json_name) as file:
            save_to_json(stargazers_map, file)
    else:
        repo_to_json(name=args.repo_name, url=args.repo_url, jsonl_path=args.json_name)
