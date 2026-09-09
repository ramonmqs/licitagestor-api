from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

app = FastAPI(title="LicitaGestor API")


@app.get("/")
def read_root():
    return {"projeto": "LicitaGestor", "ambiente": settings.environment}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"banco": "conectado"}