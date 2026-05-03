from fastapi import FastAPI, UploadFile, HTTPException
from app.services.parsepdf import extract_text_from_pdf
from app.agents.resume_extractor import generate_response
from app.agents.jd_extractor import analyze_jd
from app.agents.evaluation import candidate_evaluation

app = FastAPI()


def _require_pdf(file: UploadFile) -> None:
    if file.content_type != "application/pdf" and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"'{file.filename}' is not a PDF file.")


@app.get("/")
async def root():
    return {"message": "Resume Screening API is running."}


@app.post("/screen_resume")
async def screen_resume(resume: UploadFile, jd: UploadFile):
    _require_pdf(resume)
    _require_pdf(jd)

    try:
        resume_text = extract_text_from_pdf(resume.file)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Resume PDF error: {e}")

    try:
        jd_text = extract_text_from_pdf(jd.file)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"JD PDF error: {e}")

    try:
        resume_data = generate_response(resume_text)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Resume extraction failed: {e}")

    try:
        jd_data = analyze_jd(jd_text)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"JD extraction failed: {e}")

    try:
        result = candidate_evaluation(resume_data, jd_data)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Evaluation failed: {e}")

    return result
