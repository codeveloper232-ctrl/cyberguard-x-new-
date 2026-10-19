from app.engines.url_analyzer import analyze_url
from app.engines.threat_intel import check_virustotal

def calculate_global_risk(url: str):
    url_results = analyze_url(url)
    vt_results = check_virustotal(url)
    
    total_score = url_results["partial_score"] + vt_results["partial_score"]
    total_score = min(total_score, 100)
    
    severity = "SAFE"
    if total_score >= 80:
        severity = "CRITICAL"
    elif total_score >= 50:
        severity = "HIGH"
    elif total_score >= 20:
        severity = "MEDIUM"

    return {
        "url": url,
        "risk_score": total_score,
        "severity": severity,
        "explainable_ai": {
            "url_structural_signals": url_results["signals"],
            "threat_intel_signals": vt_results["signals"]
        }
    }
