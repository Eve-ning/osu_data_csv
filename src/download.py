import logging
import tarfile
from pathlib import Path

import wget


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


def unzip_tar_bz2(fn: Path):
    """ Unzips the file"""
    logging.info(f"Unzipping File {fn}")
    with tarfile.open(fn.as_posix(), "r:bz2") as tar:
        tar.extractall(fn.parent)


def download_pipeline(url: str, fn: Path, overwrite=False, cleanup=False):
    """ Downloads the database files

    Args:
        url: https://data.ppy.sh... url
        fn: File Name to download to
        overwrite: Whether to overwrite the tar gz2
        cleanup: Deletes the tar gz2

    """
    if download_file(url, fn, overwrite):
        logging.info(f"Unzipping files from {fn}")
        unzip_tar_bz2(fn)
        if cleanup:
            logging.info(f"Cleaning up file {fn}")
            fn.unlink()
