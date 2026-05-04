import io
import json
import os
import logging
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from app.services.parsepdf import extract_text_from_pdf
from app.agents.resume_extractor import generate_response
from app.agents.jd_extractor import analyze_jd
from app.agents.evaluation import candidate_evaluation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
PROCESSED_FILES_PATH = Path("app/resources/processed_files.json")


def _get_drive_service():
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "app/resources/credentials.json")
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def _load_processed() -> set:
    if PROCESSED_FILES_PATH.exists():
        return set(json.loads(PROCESSED_FILES_PATH.read_text()))
    return set()


def _save_processed(processed: set) -> None:
    PROCESSED_FILES_PATH.write_text(json.dumps(list(processed)))


def _list_pdf_files(service, folder_id: str) -> list:
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    result = service.files().list(q=query, fields="files(id, name)").execute()
    return result.get("files", [])


def _download_file(service, file_id: str) -> io.BytesIO:
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buffer.seek(0)
    return buffer


def poll_drive():
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id:
        logger.error("GOOGLE_DRIVE_FOLDER_ID not set in .env")
        return

    try:
        service = _get_drive_service()
    except Exception as e:
        logger.error(f"Failed to connect to Google Drive: {e}")
        return

    processed = _load_processed()
    files = _list_pdf_files(service, folder_id)

    for file in files:
        file_id = file["id"]
        file_name = file["name"]

        if file_id in processed:
            continue

        logger.info(f"New CV detected: {file_name} — processing...")

        try:
            pdf_buffer = _download_file(service, file_id)
            resume_text = extract_text_from_pdf(pdf_buffer)
            resume_data = generate_response(resume_text)

            with open("app/resources/JD.pdf", "rb") as jd_file:
                jd_text = extract_text_from_pdf(jd_file)
            jd_data = analyze_jd(jd_text)

            result = candidate_evaluation(resume_data, jd_data)
            logger.info(f"Result for {file_name}: {json.dumps(result, indent=2)}")

        except Exception as e:
            logger.error(f"Failed to process {file_name}: {e}")

        processed.add(file_id)
        _save_processed(processed)
