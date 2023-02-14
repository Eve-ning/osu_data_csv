import logging
from datetime import datetime
from pathlib import Path

import click
import yaml

from .pipelines import pipeline


def get_dataset(year_month: str, mode: str, set: str, dl_dir: str,
                bypass_confirm: str, cleanup: str, ignore_path: str):
    fn = f"{year_month}_01_performance_{mode}_top_{set}"
    dl_dir_abs = Path(dl_dir).absolute().as_posix()

    print(f"Download Files: ")
    print(f"\t- {dl_dir_abs}/{fn}.tar.bz2")
    print(f"Derived Files: ")
    print(f"\t- {dl_dir_abs}/{fn}/___.sql (All SQL Files are extracted)")

    if bypass_confirm == "Y":
        agree = "Y"
    else:
        agree = input("Proceed to Download & Process Files [Y]/n: ") or "Y"
    if agree.upper() != 'Y':
        print("Aborting.")
        return

    print("Proceeding to Download ...")
    pipeline(fn, dl_dir, cleanup=cleanup == 'Y', mode=mode, ignore_path=ignore_path)


@click.command()
@click.option('--year_month', '-y',
              default=datetime.now().strftime("%Y_%m"),
              prompt=f"-y: Dataset Year & Month(YYYY_MM)".upper(),
              help="Year Month in the YYYY_MM format")
@click.option('--mode', '-d',
              default="catch",
              prompt=f"-d: Dataset Mode (osu/taiko/catch/mania)",
              help="Game Mode. Must be either osu/taiko/catch/mania")
@click.option('--set', '-s',
              default="1000",
              prompt=f"-s: Dataset Top ____ (1000 or 10000)",
              help="Top-N player scores. Must be either 1000 or 10000")
@click.option('--dl_dir', '-l',
              default="data/",
              prompt=f"-l: Folder to download files to",
              help="The folder to download the zip, extract, and convert to")
@click.option('--cleanup', '-c',
              default="N",
              prompt=f"-c: Whether to cleans up downloaded tar.bz2 and sql files after execution (Y/N)",
              help="Whether to clean up the downloads after the script is complete")
@click.option('--bypass_confirm', '-q',
              default="N",
              help="Whether to bypass the confirmation. Use this to skip the final prompt")
@click.option('--ignore_path', '-i',
              default="",
              help="Path to the Ignore YAML. The format must be exactly as shown in the README.md. Optional ")
def get_dataset_click(year_month: str, mode: str, set: str, dl_dir: str,
                      bypass_confirm: str, cleanup: str, ignore_path: str):
    """ Downloads, Extracts and converts the .sql dataset into .csv

    Notes:
        --ignore_path is optional.
        You can use this if you want to speed up the conversion.
        Please refer to the example in the README.md or in
        https://github.com/Eve-ning/osu_data_csv/blob/master/README.md

    """
    get_dataset(year_month, mode, set, dl_dir, bypass_confirm, cleanup, ignore_path)


def main():
    logging.getLogger().setLevel(logging.INFO)
    get_dataset_click()


if __name__ == '__main__':
    main()
