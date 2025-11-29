import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app, get_db
from database import Base


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database"""
    db_fd, db_path = tempfile.mkstemp()
    test_engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=test_engine)

    yield test_engine

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def db_session(test_engine):
    """Test database session"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session):
    """Test client"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_recipe():
    return {
        "title": "Test Pasta",
        "ingredients": "pasta, tomato sauce, cheese",
        "instructions": "1. Boil pasta 2. Add sauce 3. Add cheese",
        "cuisine": "Italian",
        "meal_type": "dinner",
    }
