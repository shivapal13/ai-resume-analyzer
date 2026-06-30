from app.core.database import Base
from sqlalchemy import Column,String,Boolean,Integer,DateTime,Text
from datetime import datetime

class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, nullable=False)

    file_name = Column(String, nullable=False)

    job_description = Column(Text, nullable=False)

    resume_text = Column(Text, nullable=False)

    match_score = Column(Integer, nullable=False)

    matched_keywords = Column(Text, nullable=False)

    missing_keywords = Column(Text, nullable=False)

    strengths = Column(Text, nullable=False)

    weaknesses = Column(Text, nullable=False)

    suggestions = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


