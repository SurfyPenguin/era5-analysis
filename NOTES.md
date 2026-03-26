## Dropping Coordinates
`expver` (experiment version) & `number` (ensemble number) values are dropped from the dataset, since they are consistent over all datasets.

## Resampling of Data
All datasets will be resampled to daily resolution. This is how it affects the variables:
* `total precipitation (tp)`:
Add all the hourly values, because the data accumulates precipitation over the hour. This gives total daily precipitation.

* `others (t2m, u10, v10, d2m)`:
Use the mean, because they are instantaneous hourly values. 

## Processing, file format & naming schemes 
1. `data/compressed/`:
Downloaded datasets follow the naming scheme `YYYY_MM-MM.zip`, where `YYYY` is the year, `MM-MM` is the month range, the dataset covers.

2. `data/raw/`:
Uncompressed versions of downloaded datasets are stored here with directories following same naming scheme `YYYY_MM-MM`.

3. `data/interim/`:
The uncompressed directories contain all the datasets but they are fragmented into monthly chunks. The datasets are merged __year-wise__ using the following process:
    1. __Deserialization__: Load all datasets from same year.
    2. __Resampling__: Resample all the variables to daily resolution.
    3. __Merge__: Combine all monthly fragments into a single yearly dataset.
    4. __Serialization__: Write the merged dataset to disk, into single NetCDF file named `combined_YYYY.nc`.

4. `data/processed`