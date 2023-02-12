import logging
from datetime import datetime
from pathlib import Path

import click

from src.pipelines import pipeline


def get_dataset(year_month: str, mode: str, set: str, dl_dir: str,
                bypass_confirm: str, cleanup: str):
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
    pipeline(fn, dl_dir, cleanup=cleanup == 'Y', mode=mode)


@click.command()
@click.option('--year_month', '-y', default=datetime.now().strftime("%Y_%m"),
              prompt=f"-y: Dataset Year & Month(YYYY_MM)")
@click.option('--mode', '-d', default="mania", prompt=f"-d: Dataset Mode")
@click.option('--set', '-s', default="1000", prompt=f"-s: Dataset Top ____ (1000 or 10000)")
@click.option('--dl_dir', '-l', default="data/", prompt=f"-l: Folder to download files to")
@click.option('--cleanup', '-c', default="N",
              prompt=f"-c: Whether to cleans up downloaded tar.bz2 and sql files after execution (Y/N)")
@click.option('--bypass_confirm', '-q', default="N")
def get_dataset_click(year_month: str, mode: str, set: str, dl_dir: str, bypass_confirm: str, cleanup: str):
    get_dataset(year_month, mode, set, dl_dir, bypass_confirm, cleanup)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    get_dataset_click()
