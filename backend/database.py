import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch values from environment variables
TURSO_DB_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# 2. Construct database URL dynamically
if TURSO_DB_URL and TURSO_TOKEN:
    # Production / Cloud setup using Turso
    db_url = TURSO_DB_URL.replace("libsql://", "sqlite+libsql://")
    SQLALCHEMY_DATABASE_URL = f"{db_url}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
        "auth_token": TURSO_TOKEN,
        "check_same_thread": False})
else:
    # Fallback for local testing (runs locally if env vars are missing)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./tzoker.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                           "check_same_thread": False})  # required for SQLite + FastAPI

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
