from fastapi import FastAPI
from api.upload import router as upload_router

app = FastAPI(
    title="InsightIQ",
    description="Enterprise Business Intelligence Platform",
    version="1.0.0"
)

app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "project": "InsightIQ",
        "status": "Running",
        "message": "Welcome to InsightIQ 🚀"
    }