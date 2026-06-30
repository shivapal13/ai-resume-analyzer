from fastapi import FastAPI,Depends
from app.routers import resume_router
from sqlalchemy.orm import Session
from app.core.database import get_db
from sqlalchemy import text



app=FastAPI()

@app.get("/health")
def health_check(db:Session=Depends(get_db)):
    
    db.execute(text("SELECT 1"))

    return{
        "status":"healthy",
        "service":"resume_analyze_api",
        "database":"connected"
    }

app.include_router(resume_router.router)