import logging
import tarfile
from pathlib import Path

from src.conf import FILE_CONFIGS


def unzip_tar_bz2(tar_file: Path):
    """ Unzips the file """
    logging.info(f"Unzipping File {tar_file}")
    with tarfile.open(tar_file.as_posix(), "r:bz2") as tar:
        for member in tar.getmembers():
            if any([k in member.name for k in FILE_CONFIGS.keys()]):
                print(f"Extracting: {member.name}")
                tar.extract(member)
