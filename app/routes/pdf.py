from fastapi import APIRouter, HTTPException, Response
from starlette.responses import StreamingResponse
from app.services.pdf_service import build_patient_dashboard_pdf
from app.routes.client import client

from pymongo import MongoClient
from bson import ObjectId, errors as bson_errors

pdf_router = APIRouter()


patients = client["conectacare"]["patient"]

@pdf_router.get("/patient/{patient_id}")
def patient_pdf(patient_id: str):
    try:
        ide = ObjectId(patient_id)
        patient = patients.find_one({"_id": ide})
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")
    
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")
    buffer = build_patient_dashboard_pdf(patient)
    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=patient_dashboard.pdf"
    })