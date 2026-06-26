from sqlalchemy import Column,String,DateTime,Integer
from app.core.database import Base
from sqlalchemy.sql.sqltypes import Text
from datetime import datetime

class ResumeAnalysis(Base):
    __tablename__="resume_analysis"


    id=Column(Integer,primary_key=True,nullable=False)
    file_name=Column(String,nullable=False)
    target_role=Column(String,nullable=False)
    resume_text=Column(Text,nullable=False)
    summary=Column(Text,nullable=False)
    matched_skills=Column(Text,nullable=False)
    missing_skills=Column(Text,nullable=False)
    suggestions=Column(Text,nullable=False)
    weaknesses=Column(Text,nullable=False)
    ats_score=Column(Integer,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)