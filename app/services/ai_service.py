from google import genai
from app.core.config import settings
import json
class AIService:

    def __init__(self):
        self.client=genai.Client(
            api_key=settings.GEMINI_API_KEY
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
         
        response=self.client.models.generate_content(
             model="gemini-2.5-flash",
             contents=prompt
        )
        response_text = response.text

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")

        return json.loads(response_text.strip())