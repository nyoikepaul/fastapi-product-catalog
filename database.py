import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# If running on Vercel, use the /tmp directory for the database
if os.environ.get('VERCEL'):
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/shop.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./shop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
