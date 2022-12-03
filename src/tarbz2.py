import logging
import tarfile
from pathlib import Path


def unzip_tar_bz2(fn_tar: Path):
    """ Unzips the file"""
    logging.info(f"Unzipping File {fn_tar}")
    with tarfile.open(fn_tar.as_posix(), "r:bz2") as tar:
        tar.extractall(fn_tar.parent)


def zip_tar_bz2(fn_tar: Path, tar_target: Path, archive_name: str = 'csv'):
    """ Zips the directory """
    if fn_tar.exists():
        logging.info(f"{fn_tar} exists, skipping")
    else:
        logging.info(f"Zipping to {fn_tar}")
        with tarfile.open(fn_tar, "w:gz") as tar:
            tar.add(tar_target, arcname=archive_name)
