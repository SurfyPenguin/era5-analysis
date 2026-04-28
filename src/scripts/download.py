from collections.abc import Iterator
import os

from cds_weather_api import RequestBuilder
from cds_weather_api.validators import Validators as validate

from constants import DATA_CONFIG
from ranges import month_chunk

def download_year(year: int, *,  output_dir: str | None = None) -> None:
    era5_config: dict = DATA_CONFIG["era5"]
    fmt: str = era5_config["download_format"]

    def get_target(start: int, end: int) -> str:
        file_name: str = f"{year}_{start}-{end}.{fmt}"

        if output_dir:
            return os.path.join(output_dir, file_name)
        return file_name

    for start, end in month_chunk(5):
        target = get_target(start, end)
        request = (
            RequestBuilder()
            .dataset(era5_config["dataset"])
            .product_type(era5_config["product_type"])
            .variables(era5_config["variables"])
            .year(year)
            .month_range(start, end)
            .day_range(1, 31)
            .time_range(0, 23)
            .area(era5_config["bounding_box"])
            .download_format(era5_config["download_format"])
            .data_format(era5_config["data_format"])
            .target(file_name=target)
            .build()
        )
        print(f">> Started download: {target}")
        request.execute()

def download(start_year: int, end_year: int | None = None, *, output_dir: str | None = None) -> None:
    end_year = start_year if end_year is None else end_year

    for year in range(start_year, end_year+1):
        download_year(year, output_dir=output_dir)