import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.database import Base, get_db
from app.main import app
from app.core.config import TEST_DATABASE_URL
import time

# -----------------------------
# Engine & Session
# -----------------------------
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------
# Wait for DB & Create Tables
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    for _ in range(10):
        try:
            with engine.connect():
                break
        except OperationalError:
            time.sleep(1)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# -----------------------------
# Transactional session per test
# -----------------------------
@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# -----------------------------
# Truncate tables to reset IDs
# -----------------------------
@pytest.fixture(autouse=True)
def truncate_tables(db):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"))
    db.commit()

# -----------------------------
# Fresh TestClient per test
# -----------------------------
@pytest.fixture(scope="function")
def client(db):
    def _get_test_db():
        yield db

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()