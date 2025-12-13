import json
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from .common.fs_utils import write_safe

class AppConfig(BaseModel):
    archive_root: Optional[str] = None

class ConfigManager:
    def __init__(self, override_path: Optional[str] = None):
        if override_path:
            self.config_dir = Path(override_path)
        else:
            # Default to XDG-ish config in home dir
            self.config_dir = Path.home() / ".config" / "digital-estate-mvp"
        
        self.config_file = self.config_dir / "config.json"
        self._ensure_dir()

    def _ensure_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> AppConfig:
        if not self.config_file.exists():
            return AppConfig()
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                return AppConfig(**data)
        except (json.JSONDecodeError, OSError):
            # If corrupt or unreadable, return default (auth decision: maybe backup?)
            return AppConfig()

    def save(self, config: AppConfig) -> None:
        json_str = config.model_dump_json(indent=2)
        write_safe(str(self.config_file), json_str)

    def get_archive_root(self) -> Optional[Path]:
        cfg = self.load()
        if cfg.archive_root:
            return Path(cfg.archive_root)
        return None

    def set_archive_root(self, path: str) -> None:
        # Validate path existence?
        # The logic might span: validation -> save.
        # Here we just save. Validation belongs in the caller/use-case most likely,
        # but let's at least ensure we are saving a string.
        cfg = self.load()
        cfg.archive_root = str(path)
        self.save(cfg)
