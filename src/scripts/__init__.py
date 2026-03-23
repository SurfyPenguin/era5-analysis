from importlib.metadata import version

from .download import download
from .merge import Datasets, Operations 

__version__ = version("era5-analysis")
__all__ = ["download", "Datasets", "Operations"]
