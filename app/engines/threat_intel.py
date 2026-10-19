import requests
import base64
from app.config import VIRUSTOTAL_API_KEY

def check_virustotal(url: str):
    signals = []
    score = 0

    if not VIRUSTOTAL_API_KEY or VIRUSTOTAL_API_KEY == "your_vt_key_here":
        return {"signals": ["VirusTotal API key not configured. Skipping."], "partial_score": 0}

    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUSTOTAL_API_KEY
    }
    
    try:
        response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            
            if malicious > 0 or suspicious > 0:
                signals.append(f"VirusTotal: {malicious} security vendors flagged this as malicious, {suspicious} as suspicious.")
                score += min((malicious + suspicious) * 15, 80) 
            else:
                signals.append("VirusTotal: 0 security vendors flagged this URL.")
                
        elif response.status_code == 404:
            signals.append("VirusTotal: URL not found in database (Likely new or un-scanned).")
        else:
            signals.append(f"VirusTotal API returned an error (Status: {response.status_code}).")
            
    except Exception as e:
        signals.append(f"Failed to connect to VirusTotal: {str(e)}")

    return {"signals": signals, "partial_score": score}
