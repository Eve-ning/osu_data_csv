import logging
import sys

from src.pipelines import pipeline

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    fn = sys.argv[1]
    sql_names = [
        "osu_user_stats_mania.sql",
        "osu_scores_mania_high.sql",
        "osu_beatmap_difficulty.sql",
        "osu_beatmaps.sql"
    ]
    pipeline(fn, 'data/', sql_names, cleanup=False, zip_csv_files=True)
