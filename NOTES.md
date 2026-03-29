## Downloading Datasets
We used [cds-weather-api](https://github.com/SurfyPenguin/cds-weather-api), to programmatically download datasets using a script (`src/scripts/download.py`).

## Shape of Datasets
The raw dataset contains __five__ dimensions: __latitude__, __longitude__, __time__, __experiment version__, and __ensemble number__.

The resulting dataset will contain only __three__ dimensions i.e __longitude__, __latitude__, and  __time__. Next part covers the reason for dropping __experiment version__ and __ensemble number__.

## Dropping Coordinates
The `expver` (experiment version) and `number` (ensemble number) coordinates were dropped, since both are consistent across all years.

## Resampling
The pipeline resamples all the datasets to daily resolution. For `total precipitation`, it __sums__ the hourly accumulation values to calculate the total daily precipitation. 

## Processing, File Format & Naming Schemes 
1. `data/compressed/`:
Downloaded datasets were compressed (zip) files following the naming scheme `YYYY-MM-MM.zip`, where `YYYY` is the year and `MM-MM` is the month range the dataset covers.

2. `data/raw/`:
Uncompressed versions of downloaded datasets are stored here with directories following same naming scheme `YYYY_MM-MM`.

3. `data/interim/`:
The uncompressed directories contain all the datasets fragmented into monthly chunks. The datasets are merged __year-wise__ using the following process:
    1. __Deserialization__: Load all datasets from the same year.
    2. __Resampling__: Resample all the variables to daily resolution.
    3. __Merge__: Combine all monthly fragments into a single yearly dataset.
    4. __Serialization__: Write the merged dataset to disk as a single NetCDF file named `combined_YYYY.nc`.

4. `data/processed`:
The final dataset is stored here as a single NetCDF file. It includes a binary target variable `concurrent_extreme`, where `1` indicates a concurrent extreme event and `0` indicates the absence of one.

## Definition of concurrent extreme
We opted for a percentile based approach
> A day is considered concurrent extreme (`1`) if total precipitation exceeds 95th percentile and temperature exceeds 90th percentile of that month's historical distribution. All other days are labelled `0`.

### Why?
Climate in India varies significantly across regions, an absolute threshold can't be defined. For instance, a temperature that constitutes an extreme in Himalayan region might be a normal occurrence in Rajasthan. Percentile-based thresholds are computed relative to each location's historical distribution, ensuring that climate extremes are defined consistently across all regions.

## Labelling Datasets
We processed the 25-year dataset month-by-month to compute __localized thresholds__ (90th percentile for temperature and 95th for precipitation). A day was labelled as a __concurrent extreme__ (`1`) only if both variables simultaneously exceeded their respective monthly thresholds.

__Additional information__: `valid_time` dimension is renamed to `time` in the final labelled dataset.

## Configuration
All the configuration such as era5 attributes, time-span, file paths, and post processing configuration are stored in `data/` directory.