#main.py
"""
main.py
--------
LegalEase FastAPI backend.
 
Exposes one endpoint per legal document type (matching the three
project scenarios) plus a generic /generate endpoint, a preview
endpoint that returns raw text without writing files, and a
download endpoint for retrieving a previously generated format.
 
Run with:
    uvicorn main:app --reload
"""
 
import os
import uuid
from typing import Literal, Optional
 
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
 
from templates.prompts import PROMPT_BUILDERS
from ai_core import generate_legal_text
from doc_generator import generate_all_formats, OUTPUT_DIR
 
app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator",
    version="1.0.0",
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)
 
DocType = Literal["employment_contract", "nda", "lease_agreement"]
 
 
# ---------------------------------------------------------------------------
# Request models — one per scenario, plus a generic wrapper
# ---------------------------------------------------------------------------
class EmploymentContractRequest(BaseModel):
    company_name: str
    employee_name: str
    job_title: str
    start_date: str
    compensation: str
    work_location: Optional[str] = "Remote"
    employment_type: Optional[str] = "Full-time"
 
 
class NDARequest(BaseModel):
    disclosing_party: str
    receiving_party: str
    purpose: str
    scope: str
    effective_date: str
    term: Optional[str] = "2 years from the Effective Date"
 
 
class LeaseAgreementRequest(BaseModel):
    landlord_name: str
    tenant_name: str
    property_address: str
    lease_start: str
    lease_end: str
    monthly_rent: str
    security_deposit: Optional[str] = "One month's rent"
 
 
class GenerateResponse(BaseModel):
    document_id: str
    doc_type: DocType
    preview_text: str
    download_links: dict
 
 
# ---------------------------------------------------------------------------
# Core helper shared by every scenario endpoint
# ---------------------------------------------------------------------------
def _run_generation(doc_type: DocType, data: dict, logo_path: Optional[str] = None) -> GenerateResponse:
    prompt_builder = PROMPT_BUILDERS[doc_type]
    prompt = prompt_builder(data)
 
    raw_text = generate_legal_text(prompt)
 
    document_id = uuid.uuid4().hex[:10]
    filename = f"{doc_type}_{document_id}"
 
    paths = generate_all_formats(doc_type, data, raw_text, filename, logo_path)
 
    return GenerateResponse(
        document_id=document_id,
        doc_type=doc_type,
        preview_text=raw_text,
        download_links={
            fmt: f"/download/{os.path.basename(path)}"
            for fmt, path in paths.items()
        },
    )
 
 
# ---------------------------------------------------------------------------
# Scenario 1: Employment Contract
# ---------------------------------------------------------------------------
@app.post("/generate/employment-contract", response_model=GenerateResponse)
def generate_employment_contract(payload: EmploymentContractRequest):
    try:
        return _run_generation("employment_contract", payload.model_dump())
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
 
 
# ---------------------------------------------------------------------------
# Scenario 2: NDA
# ---------------------------------------------------------------------------
@app.post("/generate/nda", response_model=GenerateResponse)
def generate_nda(payload: NDARequest):
    try:
        return _run_generation("nda", payload.model_dump())
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
 
 
# ---------------------------------------------------------------------------
# Scenario 3: Lease Agreement
# ---------------------------------------------------------------------------
@app.post("/generate/lease-agreement", response_model=GenerateResponse)
def generate_lease_agreement(payload: LeaseAgreementRequest):
    try:
        return _run_generation("lease_agreement", payload.model_dump())
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
 
 
# ---------------------------------------------------------------------------
# Branded generation: accepts an uploaded logo (multipart/form) for scenario 1
# ---------------------------------------------------------------------------
@app.post("/generate/employment-contract/branded", response_model=GenerateResponse)
async def generate_employment_contract_branded(
    company_name: str = Form(...),
    employee_name: str = Form(...),
    job_title: str = Form(...),
    start_date: str = Form(...),
    compensation: str = Form(...),
    work_location: str = Form("Remote"),
    employment_type: str = Form("Full-time"),
    logo: Optional[UploadFile] = File(None),
):
    data = {
        "company_name": company_name,
        "employee_name": employee_name,
        "job_title": job_title,
        "start_date": start_date,
        "compensation": compensation,
        "work_location": work_location,
        "employment_type": employment_type,
    }
 
    logo_path = None
    if logo is not None:
        logo_path = os.path.join(OUTPUT_DIR, f"logo_{uuid.uuid4().hex[:6]}_{logo.filename}")
        with open(logo_path, "wb") as f:
            f.write(await logo.read())
 
    try:
        return _run_generation("employment_contract", data, logo_path)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
 
 
# ---------------------------------------------------------------------------
# File download
# ---------------------------------------------------------------------------
@app.get("/download/{file_name}")
def download_file(file_name: str):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=file_name)
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}
