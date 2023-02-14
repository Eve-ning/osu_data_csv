from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

from .conf import get_mapping, Column
from .download import download_file
from .parse_sql import parse_sql_file
from .tarbz2 import unzip_tar_bz2


def download_pipeline(url: str, fn_tar: Path, files_to_extract: List[str]):
    """ Downloads the database files

    Args:
        url: https://data.ppy.sh... url
        fn_tar: File Name to download to
        files_to_extract: File names to extract from.
    """
    if download_file(url, fn_tar):
        unzip_tar_bz2(fn_tar, files_to_extract=files_to_extract)


def convert_pipeline_csv(tar_dir: Path, csv_dir: Path, mapping: Dict[str, List[Column]]):
    """ Converts the sql files to csvs and

    Args:
        tar_dir: Directory of the SQLs to convert
        csv_dir: Directory of CSV output
        mapping: Mapping information for all .sql files
    """
    for sql_name, sql_mapping in mapping.items():
        # E.g. sql_name = "osu_beatmaps.sql"
        sql_file = tar_dir / sql_name
        csv_file = csv_dir / (sql_name[:-3] + "csv")

        if csv_file.exists():
            logging.info(f"{csv_file} exists, skipping")
            continue

        logging.info(f"Converting {sql_file}")
        parse_sql_file(sql_file, csv_file, sql_mapping=sql_mapping)


def pipeline(fn: str, dl_dir: str, cleanup: bool, mode: str, ignore_path: str):
    """ Runs the download, extract and convert pipeline

    Args:
        fn: File name of the .tar.bz2 to be downloaded from the data warehouse (excluding .tar.bz2)
        dl_dir: Download directory
        cleanup: Whether to clean up the .sql and .tar.bz2 upon completion
        mode: Game Mode
        ignore_path: Path to ignore YAML file.

    """

    dl_dir = Path(dl_dir)
    tar_name = fn + ".tar.bz2"
    tar_dir = dl_dir / fn
    tar_file = dl_dir / tar_name
    csv_dir = tar_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    tar_url = fr"https://data.ppy.sh/{tar_name}"

    mapping = get_mapping(mode=mode, ignore_path=Path(ignore_path) if ignore_path else None)
    download_pipeline(tar_url, tar_file, files_to_extract=list(mapping.keys()))
    convert_pipeline_csv(tar_dir, csv_dir=csv_dir, mapping=mapping)

    if cleanup:
        logging.info("Cleaning Up & Removing Files...")
        tar_file.unlink(missing_ok=True)
        logging.info(f"\t- {tar_file.as_posix()}")
        for f in tar_dir.glob("*.sql"):
            f.unlink(missing_ok=True)
            logging.info(f"\t- {f.as_posix()}")
