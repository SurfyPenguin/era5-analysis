from collections.abc import Iterator

def month_chunk(chunk: int, /) -> Iterator[tuple[int, int]]:
    for start_month in range(1, 13, chunk):
        end_month: int = min(start_month + chunk - 1, 12)
        yield start_month, end_month

def year_range(start: int, stop: int, /, *, skip_years: set[int] | None = None) -> Iterator[int]:
    skip_years = skip_years or set()
    for year in range(start, stop + 1):
        if year not in skip_years:
            yield year