from pydantic import BaseModel
from datetime import datetime

class ResumeAnalysisResponse(BaseModel):
    id:int
    file_name:str
    target_role:str
    resume_text:str
    summary:str
    matched_skills:str
    missing_skills:str
    weaknesses:str
    suggestions:str
    ats_score:int
    created_at:datetime

    class Config:
        from_attributes=True
 