from pathlib import Path

from src.conf import FILE_CONFIGS
from src.parse_sql import parse_sql_file

DATA_DIR = Path("data/2022_10_01_performance_mania_top_1000/")

for fn in list(FILE_CONFIGS.keys())[-1:]:
    fp = DATA_DIR / fn
    parse_sql_file(fp, DATA_DIR / f"{fp.stem}.csv")
    break
