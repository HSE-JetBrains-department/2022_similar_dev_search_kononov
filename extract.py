from collections import defaultdict
import difflib
import json
from typing import List, Tuple

from dulwich.diff_tree import TreeChange
from dulwich.repo import Repo
from dulwich.walk import WalkEntry


def calc_diff(repo: Repo, change: TreeChange) -> Tuple[int, int]:
    """
    Get amount of added and deleted lines

    :param repo: repository with change
    :param change: single change between two trees
    :return: number of lines added/deleted
    """
    d = difflib.Differ()
    diffs = d.compare(repo.get_object(change.old.sha).data.decode().splitlines(),
                      repo.get_object(change.new.sha).data.decode().splitlines())

    added = 0
    deleted = 0
    for j in diffs:
        if j[0] == "+" and j[1] != "+":
            added += 1
        elif j[0] == "-" and j[1] != "-":
            deleted += 1

    return added, deleted


def get_diff(repo: Repo, entry: WalkEntry) -> dict:
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
    for c in entry.changes():
        path = c.new.path.decode()
        try:
            if c.old.sha is None:
                res[path]["added"] = len(repo.get_object(c.new.sha).data.decode().splitlines())
                res[path]["deleted"] = 0
                res[path]["blob_id"] = str(repo.get_object(c.new.sha).id.decode())
            elif c.new.sha is None:
                res[path]["added"] = 0
                res[path]["deleted"] = len(repo.get_object(c.old.sha).data.decode().splitlines())
                res[path]["blob_id"] = str(repo.get_object(c.old.sha).id.decode())
            else:
                res[path]["added"], res[path]["deleted"] = calc_diff(repo, c)
                res[path]["blob_id"] = str(repo.get_object(c.old.sha).id.decode())

        # Handling of binary of corrupted files
        except UnicodeDecodeError:
            continue
    return res


def form(repo: Repo, url: str) -> List:
    """
    Form a list of blob changes out of a repository

    :param repo: pending repository
    :param url: repository github url
    :return: repository in a list form
    """
    res = []

    for entry in repo.get_walker():
        # Take only 1-parent or 0-parent commits
        if len(entry.commit.parents) <= 1:
            diffs = get_diff(repo, entry)

            for path in diffs.keys():
                commit = {"author": str(entry.commit.author.decode()),
                          "commit_sha": str(entry.commit.id.decode()),
                          "url": url,
                          "path": path,
                          "added": diffs[path]["added"],
                          "deleted": diffs[path]["deleted"],
                          "blob_id": diffs[path]["blob_id"]}
                res.append(commit)

    return res


def repo_to_json(name: str, url: str, json_name: str):
    """
    Writes repository to json

    :param name: repository name
    :param url: repository github url
    :param json_name: file name
    """
    r = Repo(name)
    res = json.JSONEncoder().encode(form(r, url))

    with open(json_name, "w") as f:
        f.write(res)
