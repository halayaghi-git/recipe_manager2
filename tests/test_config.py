import config


def _reset_settings_cache():
    config.get_settings.cache_clear()


def test_settings_use_defaults(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("CORS_ALLOW_ORIGINS", raising=False)
    monkeypatch.delenv("RECIPES_PAGE_SIZE", raising=False)
    _reset_settings_cache()

    settings = config.get_settings()

    assert settings.database_url == "sqlite:///./recipes.db"
    assert settings.recipes_page_size == 100
    assert settings.cors_allow_origins == [
        "http://localhost:3000",
        "http://localhost:3001",
    ]


def test_settings_respect_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///tmp/test.db")
    monkeypatch.setenv(
        "CORS_ALLOW_ORIGINS", "https://example.com, https://api.example.com"
    )
    monkeypatch.setenv("RECIPES_PAGE_SIZE", "5")
    _reset_settings_cache()

    settings = config.get_settings()

    assert settings.database_url == "sqlite:///tmp/test.db"
    assert settings.recipes_page_size == 5
    assert settings.cors_allow_origins == [
        "https://example.com",
        "https://api.example.com",
    ]

    # Clean up cache for other tests
    _reset_settings_cache()
