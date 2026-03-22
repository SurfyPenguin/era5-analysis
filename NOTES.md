## Dropping Coordinates
`expvar` (experiment version) & `number` (ensemble number) values are dropped from the dataset, since its consistent over all datasets.

## Resampling of Data
All datasets will be resampled to daily resolution. This is how it affects the variables:
* `total precipitation (tp)`: Consider the value at the end of the day, since the data has accumulated precipitation, taking the last value gives us total precipitation for that day.
* `others (t2m, u10, v10, d2m)`: Take mean of them as they are instantaneous and defined per hour unlike `tp`.