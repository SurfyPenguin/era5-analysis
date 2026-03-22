from collections.abc import Iterator
import os
from typing import overload

from constants import DATA_CONFIG

from cds_weather_api import RequestBuilder
from cds_weather_api.validators import Validators as validate

def month_range(chunk: int) -> Iterator[tuple[int, int]]:
    for start_month in range(1, 13, chunk):
        end_month: int = min(start_month + chunk - 1, 12)
        yield start_month, end_month

def download_year(year: int, output_dir: str | None = None) -> None:
    era5_config: dict = DATA_CONFIG["era5"]
    fmt: str = era5_config["download_format"]

    def get_target(start: int, end: int) -> str:
        file_name: str = f"{year}_{start}-{end}.{fmt}"

        if output_dir:
            return os.path.join(output_dir, file_name)
        return file_name

    for start, end in month_range(chunk=5):
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

@overload
def download(start_year: int, *, output_dir: str | None = None) -> None: ...

@overload
def download(start_year: int, end_year: int, *, output_dir: str | None = None) -> None: ...

def download(*args, **kwargs):
    # validate
    validate.years(args)

    if len(args) == 1:
        download_year(*args, **kwargs)

    if len(args) == 2:
        start: int = args[0]
        end: int = args[-1]
        for year in range(start, end + 1):
            download_year(year, **kwargs)
