# ERA5 Analysis

## Getting Started

### Clone the project
```bash
git clone https://github.com/SurfyPenguin/era5-analysis.git
```

### Create venv

Using __uv__ can make the setup process smoother:
```bash
uv sync
```
This will create `.venv` and install dependencies.

To avoid installing dependencies instantly, use
```bash
uv venv
```

However for __pip__, you will need to create `.venv` manually. Here's how:
```bash
python -m venv .venv

source .venv/bin/activate
```
for __windows__
```ps
# powershell
.venv\Scripts\activate.ps1

# cmd
.venv\Scripts\activate.bat
```
No need to install dependencies with pip as the next step covers it.

__Note__: If you get something like
>Running scripts is disabled on this system

or similar `Execution policy error` on windows, you will need to run these commands in ps:

* One-time fix (if you have no idea what the error is about):
```ps
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
* Permanent fix for more sophisticated windows users:
```ps
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Create editable Install
```bash
uv pip install -e .

# or
pip install -e .
```
Now scripts inside `src/` will be accessible.

## Storing Data
Most of the directory names are self-explanatory.
* `src/`: Store scripts (`.py`).
* `config/`: Store config files.
* `notebooks/`: Store notebooks (`.ipynb`)
* `data/`: Contains datasets, grouped by `compressed`, `interim`, `processed`, and `raw`.
* `drafts/`: Store drafts.
* `outputs/`: Store results, plots, etc.

## Datasets
### Time span & area (BoundingBox)
The datasets are collected for the years __2000–2024__, over all months and all days as listed in [config file](config/data.yaml).

### Variables
We have two types of datasets:
* __Accumulated__: Summed over time (hours in our case) from the beginning of forecast.
* __Instantaneous__: Defined at specific time (at any hour) from the beginning of forecast.

In our case, we have one accumulated variable (`tp`) and four instantaneous variables (`t2m`, `v10`, `u10`, `d2m`).

| Parameter | Name | Unit
|---|---|---|
| `t2m` | 2 metre temperature | Kelvin ($K$) |
| `v10`/`u10` | 10 metre u/v wind component | metres per second ($m/s$) |
| `d2m` | 2 metre dewpoint temperature | Kelvin ($K$) |
| `tp` | Total precipitation | metres ($m$)

[Learn more](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels).
# License
This project is licensed under MIT License.