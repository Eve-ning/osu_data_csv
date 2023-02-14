import csv
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from .conf import get_mapping, Column


def read_sql_tokens(sql_path: Path):
    """ Reads a sql and yields a list of comma separated tokens for each INSERT INTO"""
    with open(sql_path.as_posix(), encoding='utf-8', errors='ignore') as f:
        line = ""

        # Skip all lines not INSERT INTO
        while not line.startswith("INSERT"):
            line = f.readline()

        # Init our TQDM progress bar
        pbar = tqdm(total=sql_path.stat().st_size, unit='B', unit_scale=True,
                    unit_divisor=1024, position=0, leave=False)

        while f and (not line.startswith("/*")):
            reader = csv.reader([line], delimiter=",", quotechar="'", escapechar="\\")

            tokens = next(reader)

            # Removes the initial INSERT INTO clause
            tokens[0] = "(" + tokens[0].split("(")[-1]

            yield tokens
            line = f.readline()

            # Update our progress bar based on cursor position
            pbar.n = f.tell()
            pbar.refresh()

        # Complete our progress bar
        pbar.n = pbar.total
        pbar.refresh()


def parse_sql_tokens(tokens: list[str], sql_mapping: list[Column]) -> pd.DataFrame:
    """ Parses the set of sql tokens read. This will use a file config to map the types of the data """
    records = []  # In each set of tokens, we should find multiple records
    record = []  # A record is a row

    # This keeps track of the column index of the record
    col_ix = 0

    # Our INSERT INTO tokens are like:
    # '(123','234', ..., '345)', '(234,' ... , '456);'
    # <----------------------->
    #  One Record
    #
    # Thus, we need to split the list of tokens into records.
    n_col = len(sql_mapping)
    for col in tokens:
        column_map = sql_mapping[col_ix]

        # If our token is the start or end, there's a '(' and ')'.
        # If the token is the very last, we have ');' instead.
        if column_map.include:
            if col_ix == 0:  # If first column
                col = col[1:]
            elif col_ix == n_col - 1:  # If last column
                col = col[:-1 if col.endswith(")") else -2]

            # SQL denotes empty as NULL
            if col == 'NULL':
                col = ''

            record.append(column_map.dtype(col) if col else None)

        col_ix += 1

        if col_ix == n_col:
            records.append(record)
            col_ix = 0
            record = []

    # Get all token names for our dataframe
    token_names = [x.name for x in sql_mapping if x.include]

    df = pd.DataFrame(records, columns=token_names)
    return df


def parse_sql_file(sql_path: Path, csv_path: Path, mode: str):
    """ Parses an SQL file into csv.

    Notes:
        This will slowly populate the CSV to avoid loading everything in memory.
    """
    for e, tokens in tqdm(enumerate(read_sql_tokens(sql_path)), desc=f"Parsing {sql_path.stem}"):
        df = parse_sql_tokens(tokens, get_mapping(mode)[sql_path.name])

        if e == 0:
            df.to_csv(csv_path.as_posix(), header=True, index=False)
        else:
            df.to_csv(csv_path.as_posix(), mode='a', header=False, index=False)
