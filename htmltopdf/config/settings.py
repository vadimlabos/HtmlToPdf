from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


@lru_cache()
def get_general_settings():
    return GeneralSettings()


class GeneralSettings(BaseSettings):
    address: str
    port: int
    workers: int
    timeout_keep_alive_sec: int
    log_level: str
    footer_path: str
    css_path: str
    temp_dir: str

    class Config:
        env_file = Path(__file__).parent / "./../.env"
