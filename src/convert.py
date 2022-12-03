import csv
import logging
import re
import warnings
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm


def csv_split(x):
    """ Splits the CSV-like SQL Line via csv library """
    return list(csv.reader([x], delimiter=',', quotechar="'", escapechar='\\'))[0]


def sub_binary(x):
    """ Substitutes the Binary Blob Blocks as 'BINARY' """
    return re.sub(rb"_binary(.*?)',", b'BINARY,', x)


def sql_to_df(sql_file: Path) -> Tuple[pd.DataFrame, List]:
    """ Converts the .sql dump into a DataFrame, also returns a list of failed entries

    Notes:
        This will attempt to coerce the types

    Args:
        sql_file: Path to SQL File.

    Returns:
        A converted DataFrame and a List of entries failed to convert due to mismatch in column size.
    """
    logging.info(f"Converting {sql_file.as_posix()} to DataFrame")
    pbar = tqdm(total=sql_file.stat().st_size, unit='B', unit_scale=True, unit_divisor=1024, position=0, leave=True)

    with open(sql_file, "rb") as f:
        line = b""

        while not line.startswith(b"CREATE TABLE "):
            line = f.readline()

        col_info = {}
        data = []

        logging.debug(f"Inferring Data Types")
        # Parse column names
        while not line.startswith(b"INSERT INTO"):
            line = f.readline()

            if line.strip().startswith(b"`"):
                col_name = line.split(b"`")[1].decode('ascii')
                if b"bigint" in line:
                    col_dtype = np.int64
                elif b"int" in line:
                    col_dtype = int
                elif b"float" in line:
                    col_dtype = float
                else:
                    col_dtype = str
                col_info[col_name] = col_dtype

        logging.debug(f"Inferred Column Data Types {col_info}")

        # Parse all INSERT INTO statements.
        while not line.startswith(b"/*"):
            pbar.n = f.tell()
            pbar.set_description("Parsing Data")
            pbar.refresh()

            line = sub_binary(line)

            # Decode to str with ASCII (unicode is not important)
            line = line.decode("ascii", errors='ignore')

            # Remove text before (. E.g. 'INSERT INTO ...'
            line = line[line.find("(") + 1:-4].split("),(")

            # Split the CSV-like line
            line = [csv_split(i) for i in line]

            # Extend the data
            data.extend(line)

            # Go to next line
            line = f.readline()

    pbar.n = pbar.total
    pbar.refresh()

    logging.info(f"Coercing To DataFrame & Setting Data Types")

    data_good, data_bad = [], []
    n_cols = len(col_info)
    for d in tqdm(data, desc="Filtering bad rows", position=0, leave=True):
        if len(d) == n_cols:
            data_good.append(d)
        else:
            data_bad.append(d)

    logging.info(f"Writing to DataFrame")
    df = pd.DataFrame(data_good, columns=col_info.keys())

    logging.info(f"Coercing DataFrame Types")
    df = df.astype(col_info, errors='ignore')

    # If there are entry failures, warn
    if data_bad:
        warnings.warn(f"Failed to convert {len(data_bad)}/{len(data)} ({len(data_bad) / len(data):.2%}) lines")
    return df, data_bad
