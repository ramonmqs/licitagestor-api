from fastapi import FastAPI

app = FastAPI(title="LicitaGestor API")


@app.get("/")
def read_root():
    return {"projeto": "LicitaGestor", "status": "no ar"}