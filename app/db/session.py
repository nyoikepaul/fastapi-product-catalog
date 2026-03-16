import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Get the URL and handle the 'postgres://' quirk
raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

# 2. Add connection arguments for stability in Serverless
# we use connect_timeout to prevent the function from hanging
if "postgresql" in raw_url:
    engine = create_engine(
        raw_url, 
        connect_args={'connect_timeout': 10},
        pool_pre_ping=True
    )
else:
    engine = create_engine(
        raw_url, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
