import os

from CdsApi import RequestBuilder
from CdsApi import ClientConfig as client

# for terminal
FILL_CHAR = "="

def download():
    config = client.config(wait_until_complete=False)
    
    # working variables
    variables: list[str] = [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "total_precipitation"
    ]

    # step value for 'range()'
    CHUNK: int = 2

    for year in range(2020, 2025):
        for month in range(1, 12, CHUNK):

            end_month = month + CHUNK -1
            file_name = f"{year}_{month}-{end_month}.zip"

            request = (
                RequestBuilder()
                .client(config)
                .dataset("reanalysis-era5-single-levels")
                .product_type("reanalysis")
                .variables(variables)
                .year(year)
                .month_range(month, end_month)
                .day_range(1, 31)
                .time_range(0, 12)
                .data_format("netcdf")
                .download_format("zip")
                .target(file_name=file_name)
                .build()
            )
            print(f">> Started download: {file_name}")
            request.execute()

def main():
    terminal_width = os.get_terminal_size()[0]
    print("Dataset Download Script".center(terminal_width, FILL_CHAR))

    download()

if __name__ == "__main__":
    main()
