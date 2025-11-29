import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List

_DEFAULT_CORS_ORIGINS = "http://localhost:3000,http://localhost:3001"


def _parse_csv_list(raw_value: str | None) -> List[str]:
    if not raw_value:
        return []
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _default_cors_origins() -> List[str]:
    cors_env_value = os.getenv("CORS_ALLOW_ORIGINS", _DEFAULT_CORS_ORIGINS)
    return _parse_csv_list(cors_env_value)


def _default_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./recipes.db")


def _default_page_size() -> int:
    return int(os.getenv("RECIPES_PAGE_SIZE", "100"))


@dataclass(frozen=True)
class Settings:
    database_url: str = field(default_factory=_default_database_url)
    cors_allow_origins: List[str] = field(default_factory=_default_cors_origins)
    recipes_page_size: int = field(default_factory=_default_page_size)

    def __post_init__(self) -> None:
        if self.recipes_page_size < 1:
            object.__setattr__(self, "recipes_page_size", 1)
        if not self.cors_allow_origins:
            object.__setattr__(
                self, "cors_allow_origins", _parse_csv_list(_DEFAULT_CORS_ORIGINS)
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached instance of application settings."""
    return Settings()
