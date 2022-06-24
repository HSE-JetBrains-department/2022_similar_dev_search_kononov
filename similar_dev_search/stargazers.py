import calendar
from collections import Counter
import logging
import time
from typing import Dict

from github import Github, RateLimitExceededException, Repository
from github.GithubException import GithubException

logger = logging.getLogger(__name__)


def get_repo(repo_name: str, github_account: Github) -> Repository:
    """
    Get repository with specified name
    :param repo_name: specified name
    :param github_account: account
    :return: GitHub instance representing repository
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
    Wait until GitHub api is usable again
    :param github_account: account
    """
    search_rate_limit = github_account.get_rate_limit().search
    reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())

    time.sleep(max(0, reset_timestamp - calendar.timegm(time.gmtime())))


def extract_stargazers(
    repo_name: str,
    key: str,
    repos_per_user: int = 100,
    stargazers_number: int = 100,
    top_repos_number: int = 100,
    requests_per_page: int = 100,
) -> Dict[str, int]:
    """
    Get dictionary of repository names and number of stargazers, that starred
    repository with repo_name
    :param repo_name: name of initial repository
    :param key: GitHub token
    :param repos_per_user: maximum number of starred repositories for each user
    :param stargazers_number: maximum number of stargazers
    :param top_repos_number: number of repositories with most stars
    :param requests_per_page: number of requests on each page
    :return: dictionary[repo_name, number_of_stars]
    """
    if key is None:
        raise ValueError("Specify github key")
    github_account = Github(key)
    repo = get_repo(repo_name, github_account)
    repo._requester.per_page = requests_per_page

    stars_per_repo = Counter()
    # add number of stargazers for initial repo
    stars_per_repo[repo.full_name] = repo.stargazers_count

    viewed_stargazers_number = 0
    for user in repo.get_stargazers():
        if viewed_stargazers_number == stargazers_number:
            break
        viewed_stargazers_number += 1
        starred_repos_number = 1
        try:
            for starred_repo in user.get_starred():
                if starred_repos_number > repos_per_user:
                    break
                # initial repository is not counted
                if starred_repo.full_name == repo.full_name:
                    continue
                stars_per_repo[starred_repo.full_name] += 1
                starred_repos_number += 1
        except (
            RateLimitExceededException,
            GithubException,
        ) as e:  # throws server error 502
            logger.exception(e)
            wait_for_request(github_account)
    return dict(stars_per_repo.most_common(top_repos_number))
