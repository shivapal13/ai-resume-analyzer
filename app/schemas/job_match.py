from pydantic import BaseModel

class JobMatchResponse(BaseModel):
    file_name:str
    job_description:str
    resume_text:str
    match_score:int
    matched_keywords:str
    missing_keywords:str
    strenghts:str
    weaknesses:str
    suggestions:str
    
    class Config:
        from_attributes=True