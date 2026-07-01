from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from domain.exceptions import FeatureLabException
from utils.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="FeatureLab AI Backend API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
