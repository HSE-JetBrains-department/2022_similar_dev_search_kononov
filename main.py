from typing import Tuple

from dulwich.repo import Repo
from dulwich.walk import WalkEntry
from dulwich.diff_tree import TreeChange
import difflib
import json


def calc_diff(repo: Repo, change: TreeChange) -> Tuple[int, int]:
    """
    get amount of added and deleted lines

    :param repo: repository with change
    :param change: change of file
    :return: added number, deleted number
    """
    d = difflib.Differ()
    diffs = d.compare(repo.get_object(change.old.sha).data.decode().splitlines(),
                      repo.get_object(change.new.sha).data.decode().splitlines())

    added = 0
    deleted = 0
    for j in diffs:
        if j[0] == '+':
            added += 1
        elif j[0] == '-':
            deleted += 1

    return added, deleted


def get_diff(repo: Repo, entry: WalkEntry) -> dict:
    """
    get information about commit such as:
        number of added lines for each file
        number of deleted lines for each file
        blob_id for each file

    :param repo: pending repository
    :param entry: commit object
    :return: info in form of dict {TODO}
    """
    res = {}
    for c in entry.changes():
        res[str(c.new.path)] = {}

        try:
            if c.old.sha is None:
                res[str(c.new.path)]['added'] = len(repo.get_object(c.new.sha).data.decode().splitlines())
                res[str(c.new.path)]['deleted'] = 0
                res[str(c.new.path)]['blob_id'] = str(repo.get_object(c.new.sha).id)
            elif c.new.sha is None:
                res[str(c.new.path)]['added'] = 0
                res[str(c.new.path)]['deleted'] = len(repo.get_object(c.old.sha).data.decode().splitlines())
                res[str(c.new.path)]['blob_id'] = str(repo.get_object(c.old.sha).id)
            else:
                res[str(c.new.path)]['added'], res[str(c.new.path)]['deleted'] = calc_diff(repo, c)
                res[str(c.new.path)]['blob_id'] = str(repo.get_object(c.old.sha).id)

        except UnicodeDecodeError:
            del res[str(c.new.path)]
            continue
    return res


def form(repo: Repo) -> dict:
    """
    form a dictionary out of a repository

    :param repo: pending repository
    :return: repository in a dictionary form
    """
    res = {}
    # i = 0

    for c in repo.get_walker():
        # if i == 10:
        #    break
        if len(c.commit.parents) <= 1:
            res[str(c.commit.author)] = {}
            res[str(c.commit.author)][str(c.commit.sha().hexdigest())] = get_diff(repo, c)
        # i += 1

    return res


def repo_to_json(name: str, json_name: str):
    """
    writes repository to json

    :param name: repository name
    :param json_name: file name
    """
    r = Repo(name)
    res = json.JSONEncoder().encode(form(r))

    with open(json_name, 'w') as f:
        f.write(res)


repo_to_json('scikit-learn', 'res.json')
