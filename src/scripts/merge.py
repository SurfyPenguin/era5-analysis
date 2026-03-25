from dataclasses import dataclass
import glob
import os
from typing import Self

import xarray as xr

from constants import DATA_CONFIG

VARIABLES = DATA_CONFIG["era5"]["parameters"]

@dataclass
class Datasets:
    da_instant: xr.Dataset | None = None
    da_accum: xr.Dataset | None = None
    da_merged: xr.Dataset | None = None

    def serialize(
            self,
            *,
            output_dir: str | None = None,
            zlib: bool = True,
            complevel: int = 4,
    ) -> None:
        print("Serialize...")

        for var in VARIABLES:
            self.da_merged[[var]].to_netcdf(
                path=output_dir,
                format="NETCDF4",
                encoding={var: {"zlib": zlib, "complevel": complevel}},
                mode="a",
            )

class Operations:
    def __init__(self, year: int, *, raw_dir: str) -> None:
        if not os.path.exists(raw_dir):
            raise FileNotFoundError(f"{raw_dir}: doesn't exist")
        
        year_pattern = f"{raw_dir}/{year}_*"

        self._accum_dirs = sorted(glob.glob(f"{year_pattern}/*accum.nc"))
        self._instant_dirs = sorted(glob.glob(f"{year_pattern}/*instant.nc"))

        if not self._accum_dirs:
            raise FileNotFoundError(f"No accum files found in {raw_dir}")
        if not self._instant_dirs:
            raise FileNotFoundError(f"No instant files found in {raw_dir}")

        self._datasets = Datasets()

    def deserialize_accum(
            self,
            *,
            drop_expver: bool = True,
            drop_number: bool = True,
    ) -> Self:
        print("Deserialize accumulated variables...")
        self._datasets.da_accum = xr.open_mfdataset(self._accum_dirs, chunks="auto")

        # filter
        if drop_expver:
            self._datasets.da_accum = self._datasets.da_accum.drop_vars("expver")
        if drop_number:
            self._datasets.da_accum = self._datasets.da_accum.drop_vars("number")
        
        return self

    def deserialize_instant(
            self,
            *,
            drop_expver: bool = True,
            drop_number: bool = True,
    ) -> Self:
        print("Deserialize instantaneous variables...")
        self._datasets.da_instant = xr.open_mfdataset(self._instant_dirs, chunks="auto")

        # filter
        if drop_expver:
            self._datasets.da_instant = self._datasets.da_instant.drop_vars("expver")
        if drop_number:
            self._datasets.da_instant = self._datasets.da_instant.drop_vars("number")

        return self
    
    def resample_accum(self) -> Self:
        print("Resample accumulated variables...")
        self._datasets.da_accum = self._datasets.da_accum.resample(valid_time="1D").last()
        return self
    
    def resample_instant(self) -> Self:
        print("Resample instantaneous variables...")
        self._datasets.da_instant = self._datasets.da_instant.resample(valid_time="1D").mean()
        return self
    
    def merge(self) -> Self:
        print("Merging...")
        accum_daily = self._datasets.da_accum
        instant_daily = self._datasets.da_instant

        self._datasets.da_merged = xr.merge([
            accum_daily,
            instant_daily,
        ])
        # clear memory
        print("Clear accum & instant datasets from memory...")
        self._datasets.da_accum = None
        self._datasets.da_instant = None

        return self
    
    def build(self) -> Datasets:
        return self._datasets