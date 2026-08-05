"""
Application Routes
 
Responsibilities:
1. Render Home Page
2. Upload Documents
3. Ask Questions
"""
 
from pathlib import Path
 
from fastapi import (
    APIRouter,
    File,
    Form,
    Request,
    UploadFile
)
 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
 
from app.rag import (
    ingest_document,
    ask_question
)
 
router = APIRouter()
 
templates = Jinja2Templates(directory="templates")
 
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
 
 
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
 
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
 
 
@router.post("/upload", response_class=HTMLResponse)
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):
 
    if not (
        file.filename.endswith(".pdf")
        or file.filename.endswith(".docx")
    ):
 
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": "Only PDF and DOCX files are supported."
            }
        )
 
    file_path = UPLOAD_DIR / file.filename
 
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
 
    collection_name = ingest_document(
        file_path=file_path,
        file_name=file.filename
    )
 
    request.session["collection_name"] = collection_name
 
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "success": "Document uploaded successfully."
        }
    )
 
 
@router.post("/chat", response_class=HTMLResponse)
async def chat(
    request: Request,
    question: str = Form(...)
):
 
    collection_name = request.session.get("collection_name")
 
    if collection_name is None:
 
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": "Please upload a document first."
            }
        )
 
    answer = ask_question(
        question=question,
        collection_name=collection_name
    )
 
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "question": question,
            "answer": answer
        }
    )