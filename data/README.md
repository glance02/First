# Downloaded Dataset Notes

## Selected public dataset

- Source: Zenodo
- Record: `LIGHT dataset sample for solar smart home pilot - 201801`
- Direct file used: `XXX_Pdc_1min_avg - 012018.csv`
- Download URL:
  - `https://zenodo.org/records/1256733/files/XXX_Pdc_1min_avg%20-%20012018.csv?download=1`

## Why this dataset

- It is a real photovoltaic power dataset rather than synthetic data.
- The file size is small enough for a course experiment.
- The original file is CSV and easy to inspect.
- It contains minute-level PV power data, which fits short-term forecasting tasks well.

## Local files

- Raw download:
  - [light_pv_power_201801.csv](/e:/code/github/First/data/raw/light_pv_power_201801.csv)
- Prepared single-site version used for experiments:
  - [light_pv_id00002_201801.csv](/e:/code/github/First/data/processed/light_pv_id00002_201801.csv)

## Preparation details

- The raw CSV contains two gateways: `ID00001` and `ID00002`.
- `ID00002` was selected because it covers the full range from `2018-01-01 00:01:00` to `2018-01-31 23:59:00`.
- The prepared file is:
  - filtered to one gateway
  - sorted in ascending time order
  - deduplicated by timestamp
  - renamed to standard columns: `timestamp`, `power`

## Recommended run command

```bash
python experiments/pv_forecast.py \
  --data-path data/processed/light_pv_id00002_201801.csv \
  --time-col timestamp \
  --target-col power \
  --resample-rule 15min \
  --add-time-features \
  --window-size 20 \
  --horizon 2 \
  --epochs 40 \
  --batch-size 32 \
  --hidden-size 128 \
  --output-dir artifacts/pv_experiment_light \
  --device cuda
```

## Existing smoke test output

I already ran the recommended real-data setup and saved the outputs here:

- [metrics.csv](/e:/code/github/First/artifacts/pv_experiment_light/metrics.csv)
- [predictions.csv](/e:/code/github/First/artifacts/pv_experiment_light/predictions.csv)
- [prediction_curve.png](/e:/code/github/First/artifacts/pv_experiment_light/prediction_curve.png)
- [report_snippet.md](/e:/code/github/First/artifacts/pv_experiment_light/report_snippet.md)
