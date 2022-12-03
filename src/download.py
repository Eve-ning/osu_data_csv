import logging
import tarfile
from pathlib import Path
from typing import List

import wget
from tqdm import tqdm


def download_file(url: str, fn: Path, overwrite=False) -> bool:
    """ Downloads a file from the URL to File Name

    Returns:
        If the file is downloaded
    """
    logging.info(f"Downloading from {url} to {fn}")
    if fn.exists() and not overwrite:
        print("File exists, and overwrite is false, skipping")
        return False
    wget.download(url, fn.as_posix())
    return True


def unzip_tar_bz2(fn: Path, sql_names: List[str]):
    """ Unzips the file"""
    logging.info(f"Unzipping File {fn}")
    with tarfile.open(fn.as_posix(), "r:bz2") as tar:
        for sql_name in tqdm(sql_names, desc='Extracting Files'):
            tar.extract(sql_name, fn.parent.as_posix())


def download_pipeline(url: str, fn: Path, sql_names: List[str], overwrite=False, cleanup=False):
    """ Downloads the database files

    Args:
        url: https://data.ppy.sh... url
        fn: File Name to download to
        sql_names: SQL files to extract
        overwrite: Whether to overwrite the tar gz2
        cleanup: Deletes the tar gz2

    """
    if download_file(url, fn, overwrite):
        unzip_tar_bz2(fn, sql_names)
        if cleanup:
            logging.info(f"Cleaning up file {fn}")
            fn.unlink()
