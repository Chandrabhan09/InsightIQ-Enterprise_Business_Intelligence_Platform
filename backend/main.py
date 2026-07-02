from fastapi import FastAPI

from api.profile import router as profile_router
from api.visualization import router as visualization_router
from api.numerical import router as numerical_router

app = FastAPI(
    title="InsightIQ API",
    version="1.0.0"
)

app.include_router(profile_router)
app.include_router(visualization_router)
app.include_router(numerical_router)