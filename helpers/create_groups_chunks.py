from typing import List
from database.database_requests import Group, get_all_groups


def chunks(array: List[Group], n: int):
    d, r = divmod(len(array), n)
    for i in range(n):
        si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
        yield array[si:si + (d + 1 if i < r else d)]


def create_groups_chunks() -> List[List[Group]] | None:
    groups: List[Group | None] = get_all_groups()
    if len(groups) == 0:
        return
    elif len(groups) >= 6:
        n = 6
    else:
        n = len(groups)
    x = [i for i in chunks(groups, n)]
    return x
