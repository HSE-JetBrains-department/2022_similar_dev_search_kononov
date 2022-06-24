from collections import defaultdict
import difflib
from typing import Any, Dict, Generator, List, Tuple

from dulwich.diff_tree import TreeChange
from dulwich.repo import Repo
from dulwich.walk import WalkEntry

import setup
from utils import split_name_and_mail


def is_binary(repo: Repo, change: TreeChange) -> bool:
    """
    Checks if this blob is for binary file
    :param repo: repository with change
    :param change: single change between two trees
    :return: does this blob contain non utf-8 characters
    """
    sha = change.new.sha or change.old.sha
    try:
        repo.get_object(sha).data.decode()
    except UnicodeDecodeError:
        return True
    return False


def into_lines(repo: Repo, sha: bytes) -> List[str]:
    """
    Get lines of blob
    :param repo: repository of blob
    :param sha: sha of blob
    :return: list of lines in blob
    """
    return repo.get_object(sha).data.decode().splitlines()


def calc_diff(repo: Repo, change: TreeChange) -> Tuple[int, int]:
    """
    Get number of added and deleted lines
    :param repo: repository with change
    :param change: single change between two trees
    :return: number of lines added/deleted
    """
    diff_calc = difflib.Differ()
    diffs = diff_calc.compare(
        into_lines(repo, change.old.sha), into_lines(repo, change.new.sha)
    )
    added = 0
    deleted = 0
    for diff in diffs:
        if diff[0] == "+":
            added += 1
        elif diff[0] == "-":
            deleted += 1
    return added, deleted


def update_change_dictionary(
    repo: Repo,
    sha: bytes,
    path: str,
    change_dict: defaultdict,
    missing: str,
    existing: str,
):
    """
    Write number of added and deleted lines for a file if it was created or deleted
    :param repo: repository with change
    :param sha: sha of blob
    :param path: path to file
    :param change_dict: dictionary of corresponding change
    :param missing: nullified parameter for number of lines
    :param existing: calculated number of lines parameter
    """
    change_dict[path][existing] = len(into_lines(repo, sha))
    change_dict[path][missing] = 0
    change_dict[path]["blob_id"] = (
        str(repo.get_object(sha).id.decode()) if missing == "deleted" else str(None)
    )


def get_diff(repo: Repo, entry: WalkEntry) -> Dict[str, Dict]:
    """
    Get information about commit such as:
        number of added lines for each file
        number of deleted lines for each file
        blob_id for each file
    :param repo: pending repository
    :param entry: commit object
    :return: info in form of dict
    """
    res = defaultdict(dict)
    for change in entry.changes():
        if is_binary(repo, change):
            continue
        try:
            if change.old.sha is None:
                update_change_dictionary(
                    repo=repo,
                    sha=change.new.sha,
                    path=change.new.path.decode(),
                    change_dict=res,
                    missing="deleted",
                    existing="added",
                )
            elif change.new.sha is None:
                update_change_dictionary(
                    repo=repo,
                    sha=change.old.sha,
                    path=change.old.path.decode(),
                    change_dict=res,
                    missing="added",
                    existing="deleted",
                )
            else:
                path = change.new.path.decode()
                res[path]["added"], res[path]["deleted"] = calc_diff(repo, change)
                res[path]["blob_id"] = str(repo.get_object(change.new.sha).id.decode())
        except UnicodeDecodeError as e:
            # Handling corrupted files
            setup.logger.error(
                f"Exception in repository: {repo.path},"
                f" file: {(change.new.path or change.old.path).decode()},"
                f" cause: {e}"
            )
            continue
    return res


def get_repo_changes(repo: Repo, url: str) -> Generator[Dict[str, Any], None, None]:
    """
    Form a list of blob changes out of a repository
    :param repo: pending repository
    :param url: repository GitHub url
    :return: repository in a generator form
    """
    for entry in repo.get_walker():
        # Take only 1-parent or 0-parent commits
        if len(entry.commit.parents) <= 1:
            diffs = get_diff(repo, entry)
            for path in diffs.keys():
                (author, mail) = split_name_and_mail(str(entry.commit.author.decode()))
                commit = {
                    "author": author,
                    "mail": mail,
                    "commit_sha": str(entry.commit.id.decode()),
                    "url": url,
                    "path": path,
                    "added": diffs[path]["added"],
                    "deleted": diffs[path]["deleted"],
                    "blob_id": diffs[path]["blob_id"],
                }
                yield commit
