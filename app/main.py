from fastapi import FastAPI, UploadFile
from app.services.parsepdf import extract_text_from_pdf
from app.agents.resume_extractor import generate_response

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/screen_resume")
async def screen_resume(resume: UploadFile):
    resume_data =  extract_text_from_pdf(resume.file)
    response = generate_response(resume_data)

    return response