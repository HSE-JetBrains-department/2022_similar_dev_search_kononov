import calendar
from collections import Counter
import logging
import time
from typing import Dict

from github import RateLimitExceededException, Github, Repository

logger = logging.getLogger(__name__)


def get_repo(repo_name: str,
             github_account: Github) -> Repository:
    """
    Get repository with specified name
    :param repo_name: specified name
    :param github_account: account
    :return: Github instance representing repository
    """
    repo = None
    while repo is None:
        try:
            repo = github_account.get_repo(repo_name)
        except RateLimitExceededException:
            logger.exception("rate limit exceeded while getting repository")
            wait_for_request(github_account)

    return repo


def wait_for_request(github_account: Github):
    """
    Wait until github api is usable again

    :param github_account: account
    """
    search_rate_limit = github_account.get_rate_limit().search
    reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())

    time.sleep(max(0.001, reset_timestamp - calendar.timegm(time.gmtime())))


def process_stargazers(repo_name: str,
                       key: str,
                       repos_per_user: int = 10,
                       stargazers_number: int = 10,
                       top_repos_number: int = 10,
                       requests_per_page: int = 10
                       ) -> Dict[str, int]:
    """
    Get dictionary of repository names and number of stargazers, that starred repository with repo_name
    :param repo_name: name of initial repository
    :param key: github token
    :param repos_per_user: number of starred repositories for each user
    :param stargazers_number: number of stargazers for
    :param top_repos_number: number of repositories with most stars
    :param requests_per_page: number of requests on each page
    :return: dictionary[repo_name, number_of_stars]
    """
    if key is None:
        raise ValueError("you should specify access_token or token_env_key")

    github_account = Github(key)
    repo = get_repo(repo_name, github_account)
    repo._requester.per_page = requests_per_page

    stars_per_repo = Counter()
    # add number of stargazers for initial repo
    stars_per_repo[repo.full_name] = repo.stargazers_count

    i = 0
    for user in repo.get_stargazers():
        if i == stargazers_number:
            break
        i += 1
        j = 1
        try:
            for starred_repo in user.get_starred():
                if j >= repos_per_user:
                    break
                # initial repository is not counted
                if starred_repo == repo:
                    continue
                stars_per_repo[starred_repo.full_name] += 1
                j += 1
        except RateLimitExceededException as e:
            logger.exception(e)
            wait_for_request(github_account)
        except Exception as e:
            logger.exception(f"unexpected exception - {e}")

    return dict(stars_per_repo.most_common(top_repos_number))
