from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from src.conf import FILE_CONFIGS
from src.download import download_file
from src.parse_sql import parse_sql_file
from src.tarbz2 import unzip_tar_bz2


def download_pipeline(url: str, fn_tar: Path):
    """ Downloads the database files

    Args:
        url: https://data.ppy.sh... url
        fn_tar: File Name to download to

    """
    if download_file(url, fn_tar):
        unzip_tar_bz2(fn_tar)


def convert_pipeline_csv(tar_dir: Path, csv_dir: Path, sql_names: List[str] | None):
    """ Converts the sql files to csvs and

    Args:
        tar_dir: Directory of the SQLs to convert
        csv_dir: Directory of CSV output
        sql_names: SQL file names to convert
    """
    if sql_names is None:
        sql_names = {p.name for p in tar_dir.glob("*.sql")}

    sql_names = sql_names.intersection(FILE_CONFIGS)

    if len(sql_names) == 0:
        raise FileNotFoundError("SQL Files not found. Did you spell them correctly?")

    for sql_name in sql_names:
        sql_file = tar_dir / sql_name
        csv_file = csv_dir / (sql_name[:-3] + "csv")
        if csv_file.exists():
            logging.info(f"{csv_file} exists, skipping")
            continue
        logging.info(f"Converting {sql_file}")
        parse_sql_file(sql_file, csv_file)


def pipeline(fn: str, dl_dir: str,
             sql_names: List[str] | None,
             cleanup: bool):
    dl_dir = Path(dl_dir)
    tar_name = fn + ".tar.bz2"
    tar_dir = dl_dir / fn
    tar_file = dl_dir / tar_name
    csv_dir = tar_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    tar_url = fr"https://data.ppy.sh/{tar_name}"

    download_pipeline(tar_url, tar_file)
    convert_pipeline_csv(tar_dir, csv_dir=csv_dir, sql_names=sql_names)

    if cleanup:
        logging.info("Cleaning Up & Removing Files...")
        tar_file.unlink(missing_ok=True)
        logging.info(f"\t- {tar_file.as_posix()}")
        for f in tar_dir.glob("*.sql"):
            f.unlink(missing_ok=True)
            logging.info(f"\t- {f.as_posix()}")
