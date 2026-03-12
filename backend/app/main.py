from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.accounts import router as accounts_router
from app.routers.transactions import router as transactions_router
from app.routers.balances import router as balances_router
from app.routers.reports import router as reports_router
from app.routers.cashflow import router as cashflow_router
from app.routers.ingestion import router as ingestion_router
from app.routers.category_rules import router as category_rules_router
from app.routers.budgets import router as budgets_router

app = FastAPI(title="Personal Finance Tracker")

app.include_router(accounts_router)
app.include_router(health_router)
app.include_router(transactions_router)
app.include_router(balances_router)
app.include_router(reports_router)
app.include_router(cashflow_router)
app.include_router(ingestion_router)
app.include_router(category_rules_router)
app.include_router(budgets_router)

@app.get("/")
def root():
    return {"message": "Finance Tracker API"}