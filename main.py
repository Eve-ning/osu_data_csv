import logging
import sys

from src.conf import DATA_DIR
from src.pipelines import download_pipeline, convert_pipeline

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    DATA_DIR.mkdir(exist_ok=True, parents=True)

    fn = sys.argv[1]
    # fn = "2022_10_01_performance_mania_top_1000"
    fn_tar = fn + ".tar.bz2"
    fn_dir = DATA_DIR / fn
    fn_url = fr"https://data.ppy.sh/{fn_tar}"

    sql_names = [
        "osu_user_stats_mania.sql",
        "osu_scores_mania_high.sql",
        "osu_beatmap_difficulty.sql",
        "osu_beatmaps.sql"
    ]

    download_pipeline(fn_url, DATA_DIR / fn_tar, overwrite=False, cleanup=False)
    convert_pipeline(fn_dir, sql_names=sql_names)
