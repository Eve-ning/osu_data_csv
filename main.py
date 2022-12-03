import logging
import sys

from src.conf import DATA_DIR
from src.pipelines import download_pipeline, convert_pipeline
# 2022_10_01_performance_mania_top_1000
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    fn = sys.argv[1]
    fn_tar = fn + ".tar.bz2"
    fn_dir = DATA_DIR / fn
    fn_dir_csv = fn_dir / "csv"
    fn_dir_csv.mkdir(parents=True, exist_ok=True)
    fn_url = fr"https://data.ppy.sh/{fn_tar}"

    sql_names = [
        "osu_user_stats_mania.sql",
        "osu_scores_mania_high.sql",
        "osu_beatmap_difficulty.sql",
        "osu_beatmaps.sql"
    ]

    download_pipeline(fn_url, DATA_DIR / fn_tar, sql_names=sql_names, overwrite=False, cleanup=False)
    convert_pipeline(fn_dir, fn_dir_csv, sql_names=sql_names)
