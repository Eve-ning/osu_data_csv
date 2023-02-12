[![Upload files to Release (Monthly)](https://github.com/Eve-ning/data_ppy_sh_to_csv/actions/workflows/monthly_retrieval.yml/badge.svg)](https://github.com/Eve-ning/data_ppy_sh_to_csv/actions/workflows/monthly_retrieval.yml)
# Data PPY CSV Retrieval

Retrieve data from the data ppy dump as CSV files.

# :exclamation: Important

I have been given permission to upload the script, however, not the data. 

Thus, if **you** want to upload the data elsewhere, please contact ppy through contact@ppy.sh.

```
All data provided here is done so with the intention of it being used for statistical analysis
and testing osu! subsystems.

Permission is NOT implicitly granted to deploy this in production use of any kind.
Should you wish to publicly use/expose the data provided here, please contact me first at contact@ppy.sh.

Please see https://github.com/ppy/osu-performance for more information.

Thanks,
ppy
```

## Executing the Script

1) Set up
```bash
git clone https://github.com/Eve-ning/data_ppy_sh_to_csv.git
cd data_ppy_sh_to_csv
python -m pip install tables
python -m pip install -r requirements.txt
```

2) Run the script
```bash
python osu_data_csv/main.py
```

A series of prompts should show up.

2) (Alternatively) run in a single command

```bash
python osu_data_csv/main.py \
  -y "2022_12" \
  -d "mania" \
  -s "1000" \
  -l "data" \
  -c "N" \
  -q "Y"
```

## Arguments

| Option           | Option (Shorthand) | Desc.                                                                  | Example                                      |
|------------------|--------------------|------------------------------------------------------------------------|----------------------------------------------|
| --year_month     | -y                 | Dataset Year and Month. Will fail if doesn't exist anymore             | `2022_10`                                    |
| --mode           | -d                 | Gamemode. ['catch', 'mania', 'osu', 'taiko']                           | `mania`                                      |
| --set            | -s                 | Dataset of Top 1K or 10K players. ['1000', '10000']                    | `1000`                                       |
| --dl_dir         | -l                 | Directory to download to. Best if empty. Can be not created.           | `data/`                                      |
| --cleanup        | -c                 | Whether to delete unused files after conversion. ['Y', 'N']            | `N`                                          |
| --bypass_confirm | -q                 | Whether to bypass confirmation of downloaded and new files. ['Y', 'N'] | `N`                                          |

### SQL Names

It's set to retrieve the following:

```
osu_user_stats_<MODE>.sql
osu_scores_<MODE>_high.sql
osu_beatmap_difficulty.sql
osu_beatmaps.sql
```

## Output

This will generate a few files. You'd want to retrieve the `.csv`.

```
- main.py 
- <dl_dir>/
  - 202X_XX_01_performance_<MODE>_top_<SET>.tar.bz2 (*)
  - 202X_XX_01_performance_<MODE>_top_<SET>/
    - csv/
      - osu_user_stats_<MODE>.csv
      - _.csv
      - ...
    - osu_user_stats_<MODE>.sql (*)
    - _.sql (*)
    - ...
```

- `(*)` files are deleted if `cleanup` is enabled.
