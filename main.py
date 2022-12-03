import logging
import tarfile

from tqdm import tqdm

from src.conf import DATA_DIR
from src.download import download_pipeline
from src.sql_to_df import sql_to_df

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    fn = "2022_10_01_performance_mania_top_1000"
    fn_tar = fn + ".tar.bz2"
    fn_dir = DATA_DIR / fn
    fn_dir_csv = fn_dir / "csv"
    fn_dir_csv.mkdir(parents=True, exist_ok=True)
    fn_url = fr"https://data.ppy.sh/{fn_tar}"

    download_pipeline(fn_url, DATA_DIR / fn_tar, overwrite=False, cleanup=False)

    sql_names = [
        "osu_user_stats_mania.sql",
        "osu_user_beatmap_playcount.sql"
    ]

    for sql_name in sql_names:
        fn_sql = fn_dir / sql_name
        fn_csv = fn_dir_csv / (sql_name[:-3] + "csv")
        if fn_csv.exists():
            print(f"{fn_csv} exists, skipping")
            continue
        df, data_bad = sql_to_df(fn_sql)
        df.to_csv(fn_csv, index=False)

    fn_tar = fn_dir / "csv.tar.gz"
    if fn_tar.exists():
        print(f"{fn_tar} exists, skipping")
    else:
        with tarfile.open(fn_tar, "w:gz") as tar:
            tar.add(fn_dir / "csv", arcname='csv')
