import logging
import tarfile
from pathlib import Path
from typing import List

from tqdm import tqdm


def unzip_tar_bz2(fn: Path, sql_names: List[str]):
    """ Unzips the file"""
    logging.info(f"Unzipping File {fn}")
    with tarfile.open(fn.as_posix(), "r:bz2") as tar:
        for sql_name in tqdm(sql_names, desc='Extracting Files'):
            tar.extract(sql_name, fn.parent.as_posix())

def zip_tar_bz2(fn_tar: Path, tar_target: Path, archive_name: str = 'csv'):
    """ Zips the directory """
    if fn_tar.exists():
        print(f"{fn_tar} exists, skipping")
    else:
        with tarfile.open(fn_tar, "w:gz") as tar:
            tar.add(tar_target, arcname=archive_name)
