from pathlib import Path

import yaml
from pydantic import ValidationError

from app.models import AppConfig


def load_config(config_path: str | Path) -> AppConfig:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        raw_config = yaml.safe_load(file)

    try:
        return AppConfig.model_validate(raw_config)
    except ValidationError as error:
        raise ValueError(f"Invalid configuration file: {error}") from error
