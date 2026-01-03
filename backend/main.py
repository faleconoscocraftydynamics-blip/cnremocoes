from fastapi import FastAPI, Response
from pdf_generator import generate_pdf

app = FastAPI()

@app.post("/submit")
async def submit(data: dict):
  pdf_bytes = generate_pdf(data)

  return Response(
  content=pdf_bytes, 
  media_type="application/pdf",
  headers={
    "Content-Disposition":"attachment; filename=medical_service_report.pdf"
  },
)
