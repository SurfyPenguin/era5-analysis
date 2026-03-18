import os
from pathlib import Path

import yaml

from cds_weather_api import RequestBuilder

# for terminal
FILL_CHAR: str = "="

# assumes script is at src/scripts/download.py
CONFIG_DIR: Path = Path(__file__).parent.parent.parent / "config"

def load_config(name: str) -> dict:
    with open(CONFIG_DIR / f"{name}.yaml") as file:
        return yaml.safe_load(file)

def download() -> None:
    config: dict = load_config("data")
    # working variables
    variables: list[str] = config["era5"]["variables"]

    # step value for 'range()'
    CHUNK: int = 4

    for year in range(2020, 2025):
        for month in range(1, 13, CHUNK):

            end_month = min(month + CHUNK -1, 13)
            file_name = f"{year}_{month}-{end_month}.zip"

            request = (
                RequestBuilder()
                .dataset("reanalysis-era5-single-levels")
                .product_type("reanalysis")
                .variables(variables)
                .year(year)
                .month_range(month, end_month)
                .day_range(1, 31)
                .time_range(0, 23)
                .data_format("netcdf")
                .area((35, 65, 5, 95))
                .download_format("zip")
                .target(file_name=file_name)
                .build()
            )
            print(f">> Started download: {file_name}")
            request.execute()

def main() -> None:
    terminal_width: int = os.get_terminal_size()[0]
    print("Dataset Download Script".center(terminal_width, FILL_CHAR))

    download()

if __name__ == "__main__":
    main()
