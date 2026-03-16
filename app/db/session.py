import os
from sqlalchemy import create_all, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Check if we are running on Vercel
if os.getenv("VERCEL"):
    DATABASE_URL = "sqlite:////tmp/test.db"
else:
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
