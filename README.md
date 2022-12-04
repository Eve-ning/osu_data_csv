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
python main.py
```

A series of prompts should show up.

2) (Alternatively) run in a single command

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

# Appendix

## Sample Output

![image](https://user-images.githubusercontent.com/26498608/205480023-b6258b36-daba-4b59-820c-a4bee882fbbe.png)

## Sample Console Output

```
C:\...\data_ppy_sh_to_csv>python main.py
-y: Dataset Year & Month(YYYY_MM) [2022_12]: 2022_10
-d: Dataset Mode [mania]:
-s: Dataset Top ____ (1000 or 10000) [1000]:
-l: Folder to download files to [data/]:
-n: SQL Files to convert, separated by commas. <MODE> is substituted for --mode. Convert all files if 'ALL' [osu_user_stats_<MODE>.sql,osu_scores_<MODE>_high.sql,osu_beatmap_difficulty.sql,osu_beatmaps.sql]:
-c: Whether to cleans up downloaded tar.bz2 and sql files after execution (Y/N) [N]:
-c: Whether to zip the csv files in a tar.bz2 after conversion (Y/N) [N]:
Download Files:
        - C:/.../data_ppy_sh_to_csv/data/2022_10_01_performance_mania_top_1000.tar.bz2
Derived Files:
        - C:/.../data_ppy_sh_to_csv/data/2022_10_01_performance_mania_top_1000/___.sql (All SQL Files are extracted)
        - C:/.../data_ppy_sh_to_csv/data/2022_10_01_performance_mania_top_1000/csv/osu_user_stats_mania.csv
        - C:/.../data_ppy_sh_to_csv/data/2022_10_01_performance_mania_top_1000/csv/osu_scores_mania_high.csv
        - C:/.../data_ppy_sh_to_csv/data/2022_10_01_performance_mania_top_1000/csv/osu_beatmap_difficulty.csv
        - C:/.../data_ppy_sh_to_csv/data/2022_10_01_performance_mania_top_1000/csv/osu_beatmaps.csv
Proceed to Download & Process Files [Y]/n:
Proceeding to Download ...
INFO:root:Downloading from https://data.ppy.sh/2022_10_01_performance_mania_top_1000.tar.bz2 to data\2022_10_01_performance_mania_top_1000.tar.bz2
100% [......................................................................] 309871720 / 309871720INFO:root:Unzipping File data\2022_10_01_performance_mania_top_1000.tar.bz2
INFO:root:Converting data\2022_10_01_performance_mania_top_1000\osu_user_stats_mania.sql
INFO:root:Converting data/2022_10_01_performance_mania_top_1000/osu_user_stats_mania.sql to DataFrame
Parsing Data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 215k/215k [00:00<00:00, 14.1MB/s]INFO:root:Coercing To DataFrame & Setting Data Types
Filtering bad rows: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [00:00<?, ?it/s] 
INFO:root:Writing to DataFrame
INFO:root:Coercing DataFrame Types
Parsing Data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 215k/215k [00:00<00:00, 7.04MB/s]
INFO:root:Converting data\2022_10_01_performance_mania_top_1000\osu_scores_mania_high.sql
INFO:root:Converting data/2022_10_01_performance_mania_top_1000/osu_scores_mania_high.sql to DataFrame
Parsing Data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 185M/185M [00:14<00:00, 13.4MB/s]INFO:root:Coercing To DataFrame & Setting Data Types
Filtering bad rows: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1845534/1845534 [00:00<00:00, 2083402.14it/s] 
INFO:root:Writing to DataFrame
INFO:root:Coercing DataFrame Types
Parsing Data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 185M/185M [00:21<00:00, 8.91MB/s]
INFO:root:Converting data\2022_10_01_performance_mania_top_1000\osu_beatmap_difficulty.sql
INFO:root:Converting data/2022_10_01_performance_mania_top_1000/osu_beatmap_difficulty.sql to DataFrame
Parsing Data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 639M/639M [01:08<00:00, 9.84MB/s]INFO:root:Coercing To DataFrame & Setting Data Types
Filtering bad rows: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 13622130/13622130 [00:10<00:00, 1339370.22it/s] 
INFO:root:Writing to DataFrame
INFO:root:Coercing DataFrame Types
Parsing Data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 639M/639M [01:47<00:00, 6.24MB/s]
INFO:root:Converting data\2022_10_01_performance_mania_top_1000\osu_beatmaps.sql
INFO:root:Converting data/2022_10_01_performance_mania_top_1000/osu_beatmaps.sql to DataFrame
Parsing Data: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 29.9M/29.9M [00:01<00:00, 21.3MB/s]INFO:root:Coercing To DataFrame & Setting Data Types
Filtering bad rows: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 137318/137318 [00:00<00:00, 1393814.54it/s] 
INFO:root:Writing to DataFrame
INFO:root:Coercing DataFrame Types
Parsing Data: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 29.9M/29.9M [00:02<00:00, 12.4MB/s]
```
