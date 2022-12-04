import logging
import tarfile
from pathlib import Path


def unzip_tar_bz2(tar_file: Path):
    """ Unzips the file"""
    logging.info(f"Unzipping File {tar_file}")
    with tarfile.open(tar_file.as_posix(), "r:bz2") as tar:
        tar.extractall(tar_file.parent)


def zip_tar_bz2(tar_file: Path, tar_target: Path, archive_name: str = 'csv'):
    """ Zips the directory """
    if tar_file.exists():
        logging.info(f"{tar_file} exists, skipping")
    else:
        logging.info(f"Zipping to {tar_file}")
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(tar_target, arcname=archive_name)
