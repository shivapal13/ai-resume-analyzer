from fastapi import FastAPI,APIRouter,Depends,UploadFile,Form,File,status,HTTPException
from app.schemas import resume_analysis
from app.schemas import job_match
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService
from app.models.resume_analysis import ResumeAnalysis
from app.models.job_match import JobMatch
router=APIRouter(
    prefix="/resumes",
    tags=["Resume Analysis"]
)

pdf_service=PDFService()
ai_service=AIService()

@router.post("/analyze",response_model=resume_analysis.ResumeAnalysisResponse,
              status_code=status.HTTP_201_CREATED)

def analyze_resume(db:Session=Depends(get_db),file:UploadFile=File(...),target_role:str=Form(...)):


    resume_text=pdf_service.extract_text(file)

    analysis=ai_service.analyze_resume(
         resume_text,
         target_role
    )

    db_analysis=ResumeAnalysis(
          file_name=file.filename,
          target_role=target_role,
          resume_text=resume_text,
          summary=analysis["summary"],
          matched_skills=analysis["matched_skills"],
          missing_skills=analysis["missing_skills"],
          weaknesses=analysis["weaknesses"],
          suggestions=analysis["suggestions"],
          ats_score=analysis["ats_score"]
    )

    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return db_analysis

@router.get("/",response_model=list[resume_analysis.ResumeAnalysisResponse],status_code=status.HTTP_200_OK)
def analysis_history(db:Session=Depends(get_db),page:int=1,limit:int=10):
    

    offset=(page-1)*limit
    
    previous_analysis=db.query(ResumeAnalysis).offset(offset).limit(limit).all()


    return previous_analysis

@router.get("/target_role/{target_role}",response_model=list[resume_analysis.ResumeAnalysisResponse],
            status_code=status.HTTP_200_OK)
def analysis_historyByRole(target_role:str,db:Session=Depends(get_db),page:int=1,limit:int=10):
    
    offset=(page-1)*limit
    
    previous_analysis=db.query(ResumeAnalysis).filter(ResumeAnalysis.target_role==target_role).offset(offset).limit(limit).all()

    return previous_analysis
    


@router.get("/{id}",response_model=resume_analysis.ResumeAnalysisResponse,
                    status_code=status.HTTP_200_OK)
def analysis_historybyId(id:int,db:Session=Depends(get_db)):
    
    previous_analysis=db.query(ResumeAnalysis).filter(ResumeAnalysis.id==id).first()

    if previous_analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Analysis not found")


    return previous_analysis




@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(id:int,db:Session=Depends(get_db)):
    
    analysis=db.query(ResumeAnalysis).filter(ResumeAnalysis.id==id).first()

    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Analysis not found")
    
    db.delete(analysis)
    db.commit()

@router.post("/matches",response_model=job_match.JobMatchResponse,status_code=status.HTTP_201_CREATED)
def job_match(file:UploadFile=File(...),job_description:str=Form(...),db:Session=Depends(get_db)):

    resume_text=pdf_service.extract_text(file)

    if not resume_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Could not extract text from PDF")
    
    match_analysis=ai_service.match_resume_wih_jb(
        resume_text,
        job_description
        )
    
    db_match = JobMatch(
        file_name=file.filename,
        job_description=job_description,
        resume_text=resume_text,
        match_score=match_analysis["match_score"],
        matched_keywords=match_analysis["matched_keywords"],
        missing_keywords=match_analysis["missing_keywords"],
        strengths=match_analysis["strengths"],
        weaknesses=match_analysis["weaknesses"],
        suggestions=match_analysis["suggestions"]
    )
    

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return db_match
   
    

