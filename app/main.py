from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.engines.risk_engine import calculate_global_risk
from app.engines.qr_analyzer import analyze_qr_image

app = FastAPI(
    title="CYBERGUARD X API",
    description="Next-Generation AI-Powered Threat Intelligence Platform",
    version="0.2.0"
)

class ScanRequest(BaseModel):
    target_url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to CYBERGUARD X Engine. System is Online."}

@app.post("/api/v1/scan/url")
def scan_url(request: ScanRequest):
    try:
        result = calculate_global_risk(request.target_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/scan/qr")
async def scan_qr(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        image_bytes = await file.read()
        result = analyze_qr_image(image_bytes)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
