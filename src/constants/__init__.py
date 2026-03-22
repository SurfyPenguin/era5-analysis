from pathlib import Path
import yaml

CONFIG_DIR: Path = Path(__file__).parent.parent.parent / "config"

def _load_config(name: str) -> dict:
    """Loading config from `config/`.

    Args:
        name (str): yaml file name without '.yaml' extension.

    Returns:
        dict: Parsed yaml.
    """
    with open(CONFIG_DIR / f"{name}.yaml") as file:
        return yaml.safe_load(file)
    
DATA_CONFIG: dict = _load_config("data")

__all__ = ["DATA_CONFIG"]