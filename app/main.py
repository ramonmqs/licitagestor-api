from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title="LicitaGestor API")


@app.get("/")
def read_root():
    return {"projeto": "LicitaGestor", "ambiente": settings.environment}