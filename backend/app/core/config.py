import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://finance:finance@localhost:5432/finance"
)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://finance:finance@db_test:5432/finance_test"
)