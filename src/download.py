import logging
from pathlib import Path

import wget


def download_file(url: str, fn: Path) -> bool:
    """ Downloads a file from the URL to File Name

    Returns:
        If the file is downloaded
    """
    logging.info(f"Downloading from {url} to {fn}")
    if fn.exists():
        print("File exists. Skipping Download")
        return False
    wget.download(url, fn.as_posix())
    return True
