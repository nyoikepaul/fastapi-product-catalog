import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# Fix: SQLAlchemy 2.0 REQUIRES 'postgresql://' (Supabase gives 'postgres://')
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(raw_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF# 1. Fix the broken vercel.json
printf '{\n  "version": 2,\n  "rewrites": [{ "source": "/(.*)", "destination": "app/main.py" }]\n}' > vercel.json

# 2. Ensure your dependencies are clean
printf 'fastapi==0.104.1\nuvicorn==0.24.0\nsqlalchemy==2.0.23\npsycopg2-binary==2.9.9\npython-dotenv==1.0.0\nrequests==2.31.0' > requirements.txt

# 3. Double-check your database session code for the prefix fix
cat > app/db/session.py << 'EOF'
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# Fix: SQLAlchemy 2.0 REQUIRES 'postgresql://' (Supabase gives 'postgres://')
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(raw_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
