import logging
from datetime import datetime
from pathlib import Path

import click

default_sql_names = [
    "osu_user_stats_<MODE>.sql",
    "osu_scores_<MODE>_high.sql",
    "osu_beatmap_difficulty.sql",
    "osu_beatmaps.sql"
]


@click.command()
@click.option('--year_month', '-y', default=datetime.now().strftime("%Y_%m"),
              prompt=f"-y: Dataset Year & Month(YYYY_MM)")
@click.option('--mode', '-d', default="mania", prompt=f"-d: Dataset Mode")
@click.option('--set', '-s', default="1000", prompt=f"-s: Dataset Top ____ (1000 or 10000)")
@click.option('--dl_dir', '-l', default="data/", prompt=f"-l: Folder to download files to")
@click.option('--sql_names', '-n', default=",".join(default_sql_names),
              prompt=f"-n: SQL Files to convert, separated by commas. <MODE> is substituted for --mode. "
                     f"Convert all files if None")
@click.option('--cleanup', '-c', default="N",
              prompt=f"-c: Whether to cleans up downloaded tar.bz2 and sql files after execution (Y/N)")
@click.option('--zip_csv_files', '-z', default="N",
              prompt=f"-c: Whether to zip the csv files in a tar.bz2 after conversion (Y/N)")
@click.option('--bypass_confirm', '-q', default="N")
def cli_input(year_month: str, mode: str, set: str, dl_dir: str,
              bypass_confirm: str, sql_names: str, cleanup: str, zip_csv_files: str):
    fn = f"{year_month}_01_performance_{mode}_top_{set}"
    dl_dir_abs = Path(dl_dir).absolute().as_posix()
    sql_names = sql_names.replace("<MODE>", mode).split(",")

    print(f"Download Files: ")
    print(f"\t- {dl_dir_abs}/{fn}.tar.bz2")
    print(f"Derived Files: ")
    print(f"\t- {dl_dir_abs}/{fn}/___.sql (All SQL Files are extracted)")
    for sql_name in sql_names:
        print(f"\t- {dl_dir_abs}/{fn}/csv/{sql_name[:-4]}.csv")

    if bypass_confirm == "Y":
        agree = "Y"
    else:
        agree = input("Proceed to Download & Process Files [Y]/n: ") or "Y"
    if agree.upper() != 'Y':
        print("Abort!")
        return

    print("Proceeding to Download ...")
    print(locals())
    # pipeline(fn, dl_dir, sql_names,
    #          cleanup=cleanup == 'Y',
    #          zip_csv_files=zip_csv_files == 'Y')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    cli_input()
