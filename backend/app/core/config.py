import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://finance:finance@localhost:5432/finance"
)