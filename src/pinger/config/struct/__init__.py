from pydantic import BaseModel
import yaml
from pathlib import Path
from typing import Optional, Dict


class AppConfig(BaseModel):
    name: str


class Config:
    _config: Optional[AppConfig] = None
    _raw: Optional[Dict] = None

    @classmethod
    def config(cls) -> AppConfig:
        if cls._config is None:
            cls._raw = cls.load_config()
            cls._config = AppConfig(**cls._raw)
        return cls._config

    @classmethod
    def raw(cls) -> Dict:
        if cls._raw is None:
            cls._raw = cls.load_config()
        return cls._raw

    @staticmethod
    def load_yaml_file(path: Path) -> Dict:
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    @classmethod
    def load_config(cls) -> Dict:
        # Ordered by priority (lowest first)
        locations = [
            Path("/etc/pinger/config.yml"),
            Path.home() / ".config/pinger/config.yml",
            Path(".pinger.yml"),
        ]

        merged: Dict = {}
        for path in locations:
            data = cls.load_yaml_file(path)
            merged.update(data)

        return merged
