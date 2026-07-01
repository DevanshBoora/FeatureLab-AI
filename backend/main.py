from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from domain.exceptions import FeatureLabException
from utils.logger import logger

from contextlib import asynccontextmanager
from core.database import Base, engine, SessionLocal
from models.all_models import WorkspaceModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    # Ensure default workspace exists
    db = SessionLocal()
    try:
        from uuid import UUID
        default_ws_id = UUID("00000000-0000-0000-0000-000000000001")
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == default_ws_id).first()
        if not ws:
            ws = WorkspaceModel(id=default_ws_id, name="Default Workspace")
            db.add(ws)
            db.commit()
    except Exception as e:
        logger.error(f"Failed to create default workspace: {e}")
    finally:
        db.close()
    
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="FeatureLab AI Backend API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routers import workspaces, datasets, jobs

app.include_router(workspaces.router, prefix=settings.API_V1_STR)
app.include_router(datasets.router, prefix=settings.API_V1_STR)
app.include_router(jobs.router, prefix=settings.API_V1_STR)

@app.exception_handler(FeatureLabException)
async def featurelab_exception_handler(request: Request, exc: FeatureLabException):
    logger.error(f"FeatureLabException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_type": exc.__class__.__name__},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "error_type": "InternalServerError"},
    )

@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
