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

Clone this repository and run `main.py` via `python main.py`.

A series of prompts should show up.

You may also run in a single command

```bash
python main.py \
  -y "2022" \
  -m "12" \
  -d "mania" \
  -s "1000" \
  -l "data" \
  -n "osu_user_stats_<MODE>.sql,osu_scores_<MODE>_high.sql,osu_beatmap_difficulty.sql,osu_beatmaps.sql" \
  -c "N" \
  -z "Y" \
  -a "Y"
```

## Arguments
| Option           | Option (Shorthand) | Desc.                                                                  | Example                                      |
|------------------|--------------------|------------------------------------------------------------------------|----------------------------------------------|
| --year_month     | -y                 | Dataset Year and Month. Will fail if doesn't exist anymore             | `2022_10`                                    |
| --mode           | -d                 | Gamemode. ['catch', 'mania', 'osu', 'taiko']                           | `mania`                                      |
| --set            | -s                 | Dataset of Top 1K or 10K players. ['1000', '10000']                    | `1000`                                       |
| --dl_dir         | -l                 | Directory to download to. Best if empty. Can be not created.           | `data/`                                      |
| --sql_names      | -n                 | SQL file names to retrieve, delimited by commas. See below.            | `osu_user_stats_<MODE>.sql,osu_beatmaps.sql` |
| --cleanup        | -c                 | Whether to delete unused files after conversion. ['Y', 'N']            | `N`                                          |
| --zip_csv_files  | -z                 | Whether to zip csv files created after conversion. ['Y', 'N']          | `N`                                          |
| --bypass_confirm | -q                 | Whether to bypass confirmation of downloaded and new files. ['Y', 'N'] | `N`                                          |

### SQL Names

> :information_source: `<MODE>` is substituted for the input in `--mode` / `d`

> :exclamation: `osu_beatmapsets.sql`'s conversion is not stable due to binary blobs. I recommend excluding it.

Possible SQL file names are:

```
osu_beatmap_difficulty.sql
osu_beatmap_difficulty_attribs.sql
osu_beatmap_failtimes.sql
osu_beatmap_performance_blacklist.sql
osu_beatmaps.sql
osu_beatmapsets.sql
osu_counts.sql
osu_difficulty_attribs.sql
osu_scores_<MODE>_high.sql
osu_user_beatmap_playcount.sql
osu_user_stats_<MODE>.sql
sample_users.sql
```

By default, it's set to retrieve the following:

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
    - csv.tar.gz (!)
    - osu_user_stats_<MODE>.sql (*)
    - _.sql (*)
    - ...
```

- `(*)` files are deleted if `cleanup` is enabled.
- `(!)` will only generate if `zip_csv_files` is enabled.
