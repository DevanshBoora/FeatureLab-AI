from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# Supabase requires connection pooling to be configured if using a pooler, but we are using the direct URL.
# If connecting directly via IPv4 to Supabase, we use postgresql:// not postgresql+psycopg:// for SQLAlchemy 2.0 with default psycopg2 driver, 
# but since we installed psycopg[binary], we should use postgresql+psycopg://
db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

engine = create_engine(
    db_url, 
    pool_pre_ping=True, 
    pool_size=10, 
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
