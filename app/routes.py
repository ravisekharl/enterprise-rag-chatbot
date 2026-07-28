from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.document_processor import extract_text


router = APIRouter(prefix="", tags=["Home"])

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.post("/upload")
async def upload_document(file:UploadFile = File(...)):
    file_path = UPLOAD_DIR/file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text(file_path)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:500]
    }