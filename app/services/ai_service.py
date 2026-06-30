from openai import OpenAI,RateLimitError
from app.core.config import settings
import json
from fastapi import HTTPException,status
class AIService:

    def __init__(self):
        self.client=OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
    
    def analyze_resume(self,resume_text:str,target_role:str):

        prompt = f"""
            Analyze the following resume for the role: {target_role}

            Return ONLY valid JSON.

            Format:

            {{
                "summary": "string",
                "matched_skills": "comma separated string",
                "missing_skills": "comma separated string",
                "weaknesses": "string",
                "suggestions": "string",
                "ats_score": integer
            }}

            Resume:
            {resume_text}
            """  
        try: 
          response=self.client.chat.completions.create(
            model="google/gemma-4-31b-it:free",
            messages=[
                {
             'role':"user",
             'content':prompt
                }
            ]
        )
        except RateLimitError:
           raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="AI limit exceeded plz try again after sometime")
        response_text = response.choices[0].message.content

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")

        return json.loads(response_text.strip())
    
    def match_resume_wih_jb(self,resume_text:str,job_description:str):
            prompt=f"""Compare the resume against the given {job_description}.

                Return ONLY valid JSON.

                Format:

                {{
                    "match_score": integer,
                    "matched_keywords": "comma separated string",
                    "missing_keywords": "comma separated string",
                    "strengths": "string",
                    "weaknesses": "string",
                    "suggestions": "string"
                }}

                Resume:
                {resume_text}
                """

            try: 
                 response=self.client.chat.completions.create(
                    model="google/gemma-4-31b-it:free",
                    messages=[
                        {
                    'role':"user",
                    'content':prompt
                        }
                    ]
                )
            except RateLimitError:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="API limit exceeded Plz try again later")
            
            response_text=response.choices[0].message.content
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")

            return json.loads(response_text.strip())
                    