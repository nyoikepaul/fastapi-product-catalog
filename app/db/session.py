import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Vercel sets this environment variable automatically
if os.environ.get("VERCEL") == "1":
    # Four slashes '////' are required for an absolute path in SQLite
    DATABASE_URL = "sqlite:////tmp/product_catalog.db"
else:
    # Standard local path
    DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
