import csv
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from src.conf import get_file_configs

non_int = re.compile(r'[^\d]+')
non_float = re.compile(r'[^\d.]+')
non_datetime = re.compile(r'[^\d\-\:\s]+')


def read_sql_tokens(path: Path):
    with open(path.as_posix(), encoding='utf-8', errors='ignore') as f:
        line = ""
        while not line.startswith("INSERT"):
            line = f.readline()

        pbar = tqdm(total=path.stat().st_size, unit='B', unit_scale=True,
                    unit_divisor=1024, position=0, leave=False)
        pbar.n = f.tell()
        pbar.refresh()

        while f and (not line.startswith("/*")):
            reader = csv.reader([line], delimiter=",", quotechar="'", escapechar="\\")

            tokens = next(reader)
            tokens[0] = "(" + tokens[0].split("(")[-1]
            yield tokens
            line = f.readline()
            pbar.n = f.tell()
            pbar.refresh()

        pbar.n = pbar.total
        pbar.refresh()


def parse_sql_tokens(tokens: str, file_config: tuple) -> pd.DataFrame:
    records = []
    record = []

    token_ix = 0
    token_names = [x[0] for x in file_config if x[2]]
    for token in tokens:

        token_name, token_type, token_in = file_config[token_ix]

        if token_in:
            if token_ix == 0 or token_ix == len(file_config) - 1:
                if token_type == int:
                    token = non_int.sub('', token)
                elif token_type == float:
                    token = non_float.sub('', token)
                elif token_type == datetime.fromisoformat:
                    token = non_datetime.sub('', token)
            if token == 'NULL':
                token = ''

            record.append(token_type(token) if token else None)

        token_ix += 1

        if token_ix == len(file_config):
            records.append(record)
            token_ix = 0
            record = []

    df = pd.DataFrame(records, columns=token_names)
    return df


def parse_sql_file(fp: Path, csv_output_path: Path, mode: str):
    for e, tokens in tqdm(enumerate(read_sql_tokens(fp)), desc=f"Parsing {fp.stem}"):
        df = parse_sql_tokens(tokens, get_file_configs(mode)[fp.name])

        if e == 0:
            df.to_csv(csv_output_path.as_posix(), header=True, index=False)
        else:
            df.to_csv(csv_output_path.as_posix(), mode='a', header=False, index=False)
