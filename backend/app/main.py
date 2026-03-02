from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.accounts import router as accounts_router

app = FastAPI(title="Personal Finance Tracker")

app.include_router(accounts_router)
app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Finance Tracker API"}