import argparse
import json

from make_stats import make_stats
from search import search
from stargazers import extract_stargazers


def add_extract_command(subparsers_action: argparse.Action):
    """
    Add subparser for repository extraction
    :param subparsers_action: exposed action of main parser
    """
    extract_parser = subparsers_action.add_parser("extract")
    extract_parser.add_argument(
        "-rn", "--repo-name", type=str, help="Name of extracted repository"
    )
    extract_parser.add_argument(
        "-ru", "--repo-url", type=str, help="Url of extracted repository"
    )
    extract_parser.add_argument(
        "-j", "--json-name", type=str, help="File name where repository data is stored"
    )


def add_stargazers_command(subparsers_action: argparse.Action):
    """
    Add subparser for getting top repositories that stargazers starred
    :param subparsers_action: exposed action of main parser
    """
    stargazers_parser = subparsers_action.add_parser(
        "stargazers",
        help="Find top starred repositories by users who starred initial repository",
    )
    stargazers_parser.add_argument(
        "-rp",
        "--repo-path",
        type=str,
        help="Path to repository with stargazers.",
        required=True,
    )
    stargazers_parser.add_argument(
        "-k", "--key", type=str, help="Github token", required=True
    )
    stargazers_parser.add_argument(
        "-p",
        "--json-path",
        type=str,
        help="File name where stargazers' data is saved",
        required=True,
    )
    stargazers_parser.add_argument(
        "-rpu",
        "--repos-per-user",
        type=str,
        help="Number of starred repositories for user",
        default=100,
    )
    stargazers_parser.add_argument(
        "-sn", "--stargazers-number", type=str, help="Number of stargazers", default=100
    )
    stargazers_parser.add_argument(
        "-tr",
        "--top-repos-number",
        type=str,
        help="Number of repositories with most stars",
        default=100,
    )
    stargazers_parser.add_argument(
        "-rpp",
        "--requests-per-page",
        type=str,
        help="Number of requests on each page",
        default=100,
    )


def add_make_stats_command(subparsers_action: argparse.Action):
    """
    Add subparser for developer statistics creation
    :param subparsers_action:  exposed action of main parser
    """
    stats_parser = subparsers_action.add_parser(
        "stats", help="Create dev stats from existing repository list"
    )
    stats_parser.add_argument(
        "-rl",
        "--repos-list-path",
        type=str,
        help="Path to json with list of repos from which to create dev " "stats",
        required=True,
    )
    stats_parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to created json with results",
        required=True,
    )


def add_search_command(subparsers_action: argparse.Action):
    """
    Add subparser for searching similar developers
    :param subparsers_action:  exposed action of main parser
    """
    search_parser = subparsers_action.add_parser("search", help="Find similar devs")
    search_parser.add_argument(
        "-p", "--path", type=str, help="Path to json with dev stats", required=True
    )
    search_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Name of searched developer.Put it " "in quotations if contains spaces",
    )
    search_parser.add_argument(
        "-m", "--mail", type=str, help="Mail of searched developer"
    )
    search_parser.add_argument(
        "-qd",
        "--quantity-devs",
        type=int,
        help="Number of similar devs to show",
        default=5,
    )
    search_parser.add_argument(
        "-qi",
        "--quantity-identifiers",
        type=int,
        help="Number of top identifiers to show",
        default=5,
    )


def run_stargazers(stargazers_args: argparse.Namespace):
    """
    Run stargazers.py with saving received data
    :param stargazers_args: arguments for stargazers extraction method
    """
    stargazers_map = extract_stargazers(
        repo_name=stargazers_args.repo_path,
        key=stargazers_args.key,
        repos_per_user=int(stargazers_args.repos_per_user),
        stargazers_number=int(stargazers_args.stargazers_number),
        top_repos_number=int(stargazers_args.top_repos_number),
        requests_per_page=int(stargazers_args.requests_per_page),
    )
    with open(stargazers_args.json_path, "w") as json_file:
        json_file.write(json.dumps(stargazers_map))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="sds", description="Run similar dev search program"
    )
    subparsers = parser.add_subparsers(dest="command")
    add_extract_command(subparsers)
    add_make_stats_command(subparsers)
    add_stargazers_command(subparsers)
    add_search_command(subparsers)

    args = parser.parse_args()
    if args.command == "stats":
        make_stats(args.repos_list_path, args.path)
    elif args.command == "stargazers":
        run_stargazers(args)
    elif args.command == "search":
        search(
            args.name,
            args.path,
            number_of_similar_devs=int(args.quantity_devs),
            number_of_top_identifiers=int(args.quantity_identifiers),
        )
