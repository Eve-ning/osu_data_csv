from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parents[1] / "data"

mode_mapping = {
    'osu': '',
    'taiko': '_taiko',
    'catch': '_fruits',
    'mania': '_mania',
}


def get_file_configs(mode: str):
    """ Retrieves the File Configuration for a particular mode

    Notes:
        This can be easily outdated due to the ever-changing database schema
    """
    mode = mode_mapping[mode]
    return {
        "osu_beatmap_difficulty.sql":
            [
                ('beatmap_id', int),
                ('mode', int),
                ('mods', int),
                ('diff_unified', float),
                ('last_update', datetime.fromisoformat)
            ],
        "osu_beatmaps.sql":
            [
                ('beatmap_id', int),
                ('beatmapset_id', int),
                ('user_id', int),
                ('filename', str),
                ('checksum', str),
                ('version', str),
                ('total_length', float),
                ('hit_length', int),
                ('countTotal', int),
                ('countNormal', int),
                ('countSlider', int),
                ('countSpinner', int),
                ('diff_drain', float),
                ('diff_size', float),
                ('diff_overall', float),
                ('diff_approach', float),
                ('playmode', int),
                ('approved', int),
                ('last_update', datetime.fromisoformat),
                ('difficultyrating', float),
                ('playcount', int),
                ('passcount', int),
                ('youtube_preview', str),
                ('score_version', int),
                ('deleted_at', datetime.fromisoformat),
                ('bpm', float),
            ],
        f"osu_scores{mode}_high.sql":
            [
                ('score_id', int),
                ('beatmap_id', int),
                ('user_id', int),
                ('score', int),
                ('maxcombo', int),
                ('rank', str),
                ('count50', int),
                ('count100', int),
                ('count300', int),
                ('countmiss', int),
                ('countgeki', int),
                ('countkatu', int),
                ('perfect', int),
                ('enabled_mods', int),
                ('date', datetime.fromisoformat),
                ('pp', float),
                ('replay', int),
                ('hidden', int),
                ('country_acronym', str),
            ],
        f"osu_user_stats{mode}.sql":
            [
                ('user_id', int),
                ('count300', int),
                ('count100', int),
                ('count50', int),
                ('countMiss', int),
                ('accuracy_total', int),
                ('accuracy_count', int),
                ('accuracy', float),
                ('playcount', int),
                ('ranked_score', int),
                ('total_score', int),
                ('x_rank_count', int),
                ('xh_rank_count', int),
                ('s_rank_count', int),
                ('sh_rank_count', int),
                ('a_rank_count', int),
                ('rank', int),
                ('level', float),
                ('replay_popularity', int),
                ('fail_count', int),
                ('exit_count', int),
                ('max_combo', int),
                ('country_acronym', str),
                ('rank_score', float),
                ('rank_score_index', int),
                ('rank_score_exp', float),
                ('rank_score_index_exp', int),
                ('accuracy_new', float),
                ('last_update', datetime.fromisoformat),
                ('last_played', datetime.fromisoformat),
                ('total_seconds_played', int),
            ]
    }
