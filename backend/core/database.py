from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# Supabase requires connection pooling to be configured if using a pooler, but we are using the direct URL.
if settings.DATABASE_URL.startswith("postgresql://"):
    db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
    engine = create_engine(db_url, pool_pre_ping=True, pool_size=10, max_overflow=20)
else:
    db_url = settings.DATABASE_URL
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
