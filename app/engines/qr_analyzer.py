from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO
from app.engines.risk_engine import calculate_global_risk

def analyze_qr_image(image_bytes: bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        decoded_objects = decode(image)
        
        if not decoded_objects:
            return {"error": "No QR code found in the provided image."}
        
        results = []
        for obj in decoded_objects:
            qr_url = obj.data.decode('utf-8')
            scan_result = calculate_global_risk(qr_url)
            
            results.append({
                "payload_type": obj.type,
                "extracted_url": qr_url,
                "scan_result": scan_result
            })
            
        return {"qr_analysis": results}
    except Exception as e:
        return {"error": f"Failed to process image: {str(e)}"}
