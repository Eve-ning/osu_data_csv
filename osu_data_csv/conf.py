from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import yaml

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


def get_mapping(
        mode: str, ignore_path: Path = None,
        default_path: Path = Path(__file__).parent / 'default_mapping.yaml'
) -> dict[str, list[Column]]:
    """ Retrieves the File Configuration for a particular mode

    Notes:
        Usually, you don't need to change default_yaml

    Args:
        mode: Game Mode: (osu/taiko/catch/mania)
        ignore_path: Path to ignore YAML
        default_path: Path to default YAML

    Returns:
        The file mapping as a dict[str, list[Column]]
        E.g. {'osu_beatmaps.sql': [Column(name='beatmap_id', dtype=<class int>, include=True), ... ], ...}

    """
    with open(default_path.as_posix(), 'r') as f:
        mapping: dict[str, list[list[str | bool]]] = yaml.safe_load(f)

    # Cast the lists within mapping to Column
    for _, sql_map in mapping.items():
        for e, (column, dtype, include) in enumerate(sql_map):
            sql_map[e] = Column(column, type_mapping[dtype], include)

    # Explicitly specify the type change.
    mapping: dict[str, list[Column]]

    # Run only if we have items to ignore
    if ignore_path is not None:
        with open(ignore_path.as_posix(), 'r') as f:
            ignore: dict[str, list[str]] = yaml.safe_load(f)

        # We loop through ignore yaml and set .include to false
        for ignore_sql, ignore_columns in ignore.items():
            for ignore_column in ignore_columns:
                # We loop through its columns and check if the .name is the ignore_column
                # mapping[ignore_sql]: list[Column]
                # x: Column
                next(filter(lambda x: x.name == ignore_column,
                            mapping[ignore_sql])).include = False

    mode = mode_mapping[mode]

    for k, v in list(mapping.items()):
        # We reformat the {mode} tags to the actual mode
        mapping[k.format(mode=mode)] = mapping.pop(k)

    return mapping
