from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.accounts import router as accounts_router
from app.routers.transactions import router as transactions_router
from app.routers.balances import router as balances_router
from app.routers.reports import router as reports_router
from app.routers.cashflow import router as cashflow_router

app = FastAPI(title="Personal Finance Tracker")

app.include_router(accounts_router)
app.include_router(health_router)
app.include_router(transactions_router)
app.include_router(balances_router)
app.include_router(reports_router)
app.include_router(cashflow_router)

@app.get("/")
def root():
    return {"message": "Finance Tracker API"}