import csv
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from tqdm import tqdm

DATA_DIR = Path("data/2022_10_01_performance_mania_top_1000/")

file_configs = {
    "osu_scores_mania_high.sql":
        [
            ('score_id', int, True),
            ('beatmap_id', int, True),
            ('user_id', int, True),
            ('score', int, True),
            ('maxcombo', int, False),
            ('rank', str, False),
            ('count50', int, True),
            ('count100', int, True),
            ('count300', int, True),
            ('countmiss', int, True),
            ('countgeki', int, True),
            ('countkatu', int, True),
            ('perfect', int, False),
            ('enabled_mods', int, True),
            ('date', datetime.fromisoformat, True),
            ('pp', float, True),
            ('replay', int, True),
            ('hidden', int, False),
            ('country_acronym', str, False),
        ],
    "osu_beatmaps.sql":
        [
            ('beatmap_id', int, True),
            ('beatmapset_id', int, True),
            ('user_id', int, True),
            ('filename', str, True),
            ('checksum', str, False),
            ('version', str, False),
            ('total_length', float, False),
            ('hit_length', int, False),
            ('countTotal', int, True),
            ('countNormal', int, True),
            ('countSlider', int, True),
            ('countSpinner', int, True),
            ('diff_drain', float, True),
            ('diff_size', float, True),
            ('diff_overall', float, True),
            ('diff_approach', float, False),
            ('playmode', int, True),
            ('approved', int, True),
            ('last_update', datetime.fromisoformat, True),
            ('difficultyrating', float, True),
            ('playcount', int, False),
            ('passcount', int, False),
            ('youtube_preview', str, False),
            ('score_version', int, False),
            ('deleted_at', datetime.fromisoformat, False),
            ('bpm', float, True),
        ],
    "osu_beatmap_difficulty.sql":
        [
            ('beatmap_id', int, True),
            ('mode', int, True),
            ('mods', int, True),
            ('diff_unified', float, True),
            ('last_update', datetime.fromisoformat, True)
        ],
    "osu_user_stats_mania.sql":
        [
            ('user_id', int, True),
            ('count300', int, False),
            ('count100', int, False),
            ('count50', int, False),
            ('countMiss', int, False),
            ('accuracy_total', int, False),
            ('accuracy_count', int, False),
            ('accuracy', float, False),
            ('playcount', int, False),
            ('ranked_score', int, False),
            ('total_score', int, False),
            ('x_rank_count', int, False),
            ('xh_rank_count', int, False),
            ('s_rank_count', int, False),
            ('sh_rank_count', int, False),
            ('a_rank_count', int, False),
            ('rank', int, False),
            ('level', float, False),
            ('replay_popularity', int, False),
            ('fail_count', int, False),
            ('exit_count', int, False),
            ('max_combo', int, False),
            ('country_acronym', str, False),
            ('rank_score', float, True),
            ('rank_score_index', int, True),
            ('accuracy_new', float, False),
            ('last_update', datetime.fromisoformat, False),
            ('last_played', datetime.fromisoformat, False),
            ('total_seconds_played', int, False),
        ]
}


def load_sql_tokens(path: Path):
    with open(path.as_posix(), encoding='utf-8', errors='ignore') as f:
        line = ""
        while not line.startswith("INSERT"):
            line = f.readline()

        while f and (not line.startswith("/*")):
            reader = csv.reader([line], delimiter=",", quotechar="'", escapechar="\\")

            tokens = next(reader)
            tokens[0] = "(" + tokens[0].split("(")[-1]
            yield tokens
            line = f.readline()


non_int = re.compile(r'[^\d]+')
non_float = re.compile(r'[^\d.]+')
non_datetime = re.compile(r'[^\d\-\:\s]+')


def parse_insert_into_line(tokens: str, file_config: tuple):
    records = []
    record = []

    token_ix = 0
    token_names = [x[0] for x in file_config if x[2]]
    for token in tokens:

        token_name, token_type, token_in = file_config[token_ix]

        if token_in:
            if token_ix == 0 or token_ix == len(file_config) - 1:
                if token_type == int:
                    token = non_int.sub('', token)
                elif token_type == float:
                    token = non_float.sub('', token)
                elif token_type == datetime.fromisoformat:
                    token = non_datetime.sub('', token)
            if token == 'NULL':
                token = ''
            record.append(token_type(token) if token else None)

        token_ix += 1

        if token_ix == len(file_config):
            records.append(record)
            token_ix = 0
            record = []

    df = pd.DataFrame(records, columns=token_names)
    return df


for fn in list(file_configs.keys()):
    fp = DATA_DIR / fn
    for e, tokens in tqdm(enumerate(load_sql_tokens(fp)), desc=f"Parsing {fp.stem}"):
        df = parse_insert_into_line(tokens, file_configs[fp.name])

        if e == 0:
            df.to_csv(f"{fp.stem}.csv", header=True, index=False)
        else:
            df.to_csv(f"{fp.stem}.csv", mode='a', header=False, index=False)
