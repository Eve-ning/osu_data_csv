import logging
import tarfile
from pathlib import Path
from typing import List


def unzip_tar_bz2(tar_file: Path, files_to_extract: List[str]):
    """ Unzips the file """
    logging.info(f"Unzipping File {tar_file}")
    with tarfile.open(tar_file.as_posix(), "r:bz2") as tar:
        for member in tar.getmembers():
            if any([k in member.name for k in files_to_extract]):
                print(f"Extracting: {member.name}")
                tar.extract(member, tar_file.parent.as_posix())
