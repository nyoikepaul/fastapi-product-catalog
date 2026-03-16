import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 1. Get the URL
raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# 2. Fix the prefix if necessary (SQLAlchemy requirement)
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

# 3. Use NullPool for Serverless (prevents connection ghosting)
# Also add SSL mode if connecting to a remote Postgres
if "postgresql" in raw_url:
    engine = create_engine(raw_url, poolclass=NullPool)
else:
    engine = create_engine(raw_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
