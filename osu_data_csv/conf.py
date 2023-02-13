from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import yaml

DATA_DIR = Path(__file__).parents[1] / "data"

mode_mapping = {
    'osu': '',
    'taiko': '_taiko',
    'catch': '_fruits',
    'mania': '_mania',
}

type_mapping = {
    'str': str,
    'int': int,
    'float': float,
    'datetime': datetime.fromisoformat
}


@dataclass
class Column:
    name: str
    dtype: Callable
    include: bool = True


THIS_DIR = Path(__file__).parent


def get_mapping(mode: str, mapping: dict[str, list[list]] = "", ignore: dict[str, list[str]] = "") -> dict[
    str, list[Column]]:
    """ Retrieves the File Configuration for a particular mode """
    with open(THIS_DIR / 'default_mapping.yaml', 'r') as f:
        mapping: dict[str, list[list]] = yaml.safe_load(f)

    with open(THIS_DIR / 'ignore_mapping.yaml', 'r') as f:
        ignore: dict[str, list[str]] = yaml.safe_load(f)

    for _, sql_map in mapping.items():
        for e, (column, dtype, include) in enumerate(sql_map):
            sql_map[e] = Column(column, type_mapping[dtype], include)

    for ignore_sql, ignore_columns in ignore.items():
        for ignore_column in ignore_columns:
            next(filter(lambda x: x.name == ignore_column,
                        mapping[ignore_sql])).include = False

    mode = mode_mapping[mode]

    for k, v in list(mapping.items()):
        mapping[k.format(mode=mode)] = mapping.pop(k)

    return mapping
