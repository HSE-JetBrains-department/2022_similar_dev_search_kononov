import argparse
import json

from pipeline import pipeline
from search import search
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
    stargazers_parser = subparsers_action.add_parser(
        "stargazers", help="Find top starred repositories by users who starred initial repository")
    stargazers_parser.add_argument("-rp", "--repo-path", type=str,
                                   help="Path to repository with stargazers.", required=True)
    stargazers_parser.add_argument("-k", "--key", type=str,
                                   help="Github token", required=True)
    stargazers_parser.add_argument("-p", "--json-path", type=str,
                                   help="File name where stargazers' data is saved",
                                   required=True)
    stargazers_parser.add_argument("-rpu", "--repos-per-user", type=str,
                                   help="Number of starred repositories for user", default=2)
    stargazers_parser.add_argument("-sn", "--stargazers-number", type=str,
                                   help="Number of stargazers", default=2)
    stargazers_parser.add_argument("-tr", "--top-repos-number", type=str,
                                   help="Number of repositories with most stars", default=10)
    stargazers_parser.add_argument("-rpp", "--repos-per-page", type=str,
                                   help="Number of requests on each page", default=2)


def add_make_stats_command(subparsers_action: argparse.Action):
    stats_parser = subparsers_action.add_parser(
        "stats", help="Create dev stats from existing repository list")
    stats_parser.add_argument("-rl", "--repos-list-path", type=str,
                              help="Path to json with list of repos from which to create dev "
                                   "stats", required=True)
    stats_parser.add_argument("-p", "--path", type=str,
                              help="Path to created json with results", required=True)


def add_search_command(subparsers_action: argparse.Action):
    search_parser = subparsers_action.add_parser("search", help="Find similar devs")
    search_parser.add_argument("-p", "--path", type=str, help="Path to json with dev stats",
                               required=True)
    search_parser.add_argument("-n", "--name", type=str, help="Name of searched developer")
    search_parser.add_argument("-m", "--mail", type=str, help="Mail of searched developer")


def run_stargazers(stargazers_args: argparse.Namespace):
    stargazers_map = extract_stargazers(repo_name=stargazers_args.repo_path,
                                        key=stargazers_args.key,
                                        repos_per_user=stargazers_args.repos_per_user,
                                        top_repos_number=stargazers_args.top_repos_number,
                                        stargazers_number=stargazers_args.stargazers_number
                                        )
    with open(stargazers_args.json_path, "w") as json_file:
        json_file.write(json.dumps(stargazers_map))


if __name__ == "__main__":
    "search -p s.json -n 'Alexey Kononov'"
    "stats -rl st.json -p s.json"
    parser = argparse.ArgumentParser(prog="sds", description="Extract repository.")
    subparsers = parser.add_subparsers(dest="command")
    add_extract_command(subparsers)
    add_make_stats_command(subparsers)
    add_stargazers_command(subparsers)
    add_search_command(subparsers)

    args = parser.parse_args()
    print(vars(args))
    if args.command == "stats":
        pipeline(args.repos_list_path, args.path)
    elif args.command == "stargazers":
        run_stargazers(args)
    elif args.command == "search":
        search(args.name, args.path)
