from pypdf import PdfReader
from fastapi import UploadFile

class PDFService:
   def extract_text(self,file:UploadFile) ->str:
      pdf_reader=PdfReader(file.file)

      text=""
      for page in pdf_reader.pages:
         text+=page.extract_text()

      return text