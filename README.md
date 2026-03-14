# ERA5 Analysis

## This repository analyses ERA5 data for feature creation, which will be used to label climate extremes.

## Getting Started

* __Envrionment__:This project uses `uv` for package & project management. Download [uv standalone](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

* Clone repository:
```bash
git clone https://github.com/SurfyPenguin/era5-analysis.git
```
* Install dependencies:
```bash
uv sync

# for pip
pip install .
```
* Install project as editable-package:
```bash
uv pip install -e .

# or
pip install -e .
```
This gives us access to use `era5_analysis` and download command:
```python
form era5_analysis import download
```

## Development
Feel free to create forks, issues or raise pull requests. Any type of contribution that adds value to our analysis is appreciated.