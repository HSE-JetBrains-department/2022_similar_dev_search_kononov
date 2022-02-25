from typing import Tuple, List

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
        if j[0] == '+' and j[1] != '+':
            added += 1
        elif j[0] == '-' and j[1] != '-':
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
        path = c.new.path.decode()
        res[path] = {}

        try:
            if c.old.sha is None:
                res[path]['added'] = len(repo.get_object(c.new.sha).data.decode().splitlines())
                res[path]['deleted'] = 0
                res[path]['blob_id'] = str(repo.get_object(c.new.sha).id.decode())
            elif c.new.sha is None:
                res[path]['added'] = 0
                res[path]['deleted'] = len(repo.get_object(c.old.sha).data.decode().splitlines())
                res[path]['blob_id'] = str(repo.get_object(c.old.sha).id.decode())
            else:
                res[path]['added'], res[path]['deleted'] = calc_diff(repo, c)
                res[path]['blob_id'] = str(repo.get_object(c.old.sha).id.decode())

        except UnicodeDecodeError:
            del res[path]
            continue
    return res


def form(repo: Repo, url: str) -> List:
    """
    form a dictionary out of a repository

    :param repo: pending repository
    :param url: repository github url
    :return: repository in a dictionary form
    """
    res = []
    i = 0

    for c in repo.get_walker():
        #if i == 10:
        #    break
        # take only 1-parent or 0-parent commits
        if len(c.commit.parents) <= 1:
            diffs = get_diff(repo, c)

            for path in diffs.keys():
                commit = {'author': str(c.commit.author.decode()),
                          'commit_sha': str(c.commit.id.decode()),
                          'url': url,
                          'path': path,
                          'added': diffs[path]['added'],
                          'deleted': diffs[path]['deleted'],
                          'blob_id': diffs[path]['blob_id']}
                res.append(commit)
        #i += 1

    return res


def repo_to_json(name: str, url: str, json_name: str):
    """
    writes repository to json

    :param name: repository name
    :param url: repository github url
    :param json_name: file name
    """
    r = Repo(name)
    res = json.JSONEncoder().encode(form(r, url))

    with open(json_name, 'w') as f:
        f.write(res)


repo_to_json('scikit-learn', 'https://github.com/scikit-learn/scikit-learn', 'res2.json')
