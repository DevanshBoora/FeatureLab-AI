from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

import re
import urllib.parse

def get_corrected_db_url() -> str:
    url = settings.DATABASE_URL
    if not url or not url.startswith("postgresql"):
        return url

    try:
        # Extract project ref from Supabase URL (e.g. azddhdmyzjkfwyvtduea)
        project_ref = settings.SUPABASE_URL.replace("https://", "").replace("http://", "").split(".")[0]
        
        # Parse the connection URL
        parsed = urllib.parse.urlparse(url)
        
        # 1. Clean brackets from password if present (e.g. [password] -> password)
        password = parsed.password or ""
        if password.startswith("[") and password.endswith("]"):
            password = password[1:-1]
            
        username = parsed.username or "postgres"
        host = parsed.hostname or ""
        port = parsed.port or 5432
        
        # 2. If it's a direct Supabase host (db.[ref].supabase.co), rewrite to IPv4 Pooler
        # because Render does not support IPv6 outbound.
        if "supabase.co" in host and not "pooler" in host:
            host = "aws-0-us-east-1.pooler.supabase.com"
            port = 6543
            
        # 3. Ensure username has the tenant identifier suffix (postgres.[ref]) if using the pooler
        if "pooler.supabase.com" in host and not username.endswith(f".{project_ref}"):
            # Strip any existing suffix just in case, then append correct one
            base_user = username.split(".")[0]
            username = f"{base_user}.{project_ref}"
            
        # Reconstruct URL
        auth = f"{username}:{password}" if password else username
        netloc = f"{auth}@{host}:{port}"
        
        # Ensure sslmode=require query param is set for Supabase
        query_params = urllib.parse.parse_qs(parsed.query)
        query_params["sslmode"] = ["require"]
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        
        corrected = urllib.parse.urlunparse(parsed._replace(netloc=netloc, query=new_query))
        return corrected
    except Exception as e:
        print(f"Failed to auto-correct database URL: {e}")
        return url

# Correct the DB url and apply the psycopg driver dialect prefix
raw_url = get_corrected_db_url()
if raw_url.startswith("postgresql://"):
    db_url = raw_url.replace("postgresql://", "postgresql+psycopg://")
    engine = create_engine(db_url, pool_pre_ping=True, pool_size=10, max_overflow=20)
else:
    db_url = raw_url
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
