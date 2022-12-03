import logging
from pathlib import Path
from typing import List

from src.convert import sql_to_df
from src.download import download_file
from src.tarbz2 import unzip_tar_bz2, zip_tar_bz2


def download_pipeline(url: str, fn_tar: Path, sql_names: List[str], overwrite=False, cleanup=False):
    """ Downloads the database files

    Args:
        url: https://data.ppy.sh... url
        fn_tar: File Name to download to
        sql_names: SQL files to extract
        overwrite: Whether to overwrite the tar gz2
        cleanup: Deletes the tar gz2

    """
    if download_file(url, fn_tar, overwrite):
        unzip_tar_bz2(fn_tar)
        if cleanup:
            logging.info(f"Cleaning up file {fn_tar}")
            fn_tar.unlink()


def convert_pipeline(fn_dir: Path, fn_dir_csv: Path, sql_names: List[str]):
    """ Converts the sql files to csvs and

    Args:
        fn_dir: Directory of the SQLs to convert
        fn_dir_csv: Directory of CSV output
        sql_names: SQL file names to convert

    """
    for sql_name in sql_names:
        fn_sql = fn_dir / sql_name
        fn_csv = fn_dir_csv / (sql_name[:-3] + "csv")
        if fn_csv.exists():
            print(f"{fn_csv} exists, skipping")
            continue
        df, data_bad = sql_to_df(fn_sql)
        df.to_csv(fn_csv, index=False)

    fn_tar = fn_dir / "csv.tar.gz"
    zip_tar_bz2(fn_tar, fn_dir / "csv")
