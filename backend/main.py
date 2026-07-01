from fastapi import FastAPI

app = FastAPI(
    title="InsightIQ",
    description="Enterprise Business Intelligence Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project": "InsightIQ",
        "message": "Backend Running Successfully 🚀"
    }