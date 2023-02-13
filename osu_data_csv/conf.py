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
                ('beatmap_id', int, True),
                ('mode', int, True),
                ('mods', int, True),
                ('diff_unified', float, True),
                ('last_update', datetime.fromisoformat, True)
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
        f"osu_scores{mode}_high.sql":
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
        f"osu_user_stats{mode}.sql":
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
                ('rank_score_exp', float, True),
                ('rank_score_index_exp', int, True),
                ('accuracy_new', float, False),
                ('last_update', datetime.fromisoformat, False),
                ('last_played', datetime.fromisoformat, False),
                ('total_seconds_played', int, False),
            ]
    }
