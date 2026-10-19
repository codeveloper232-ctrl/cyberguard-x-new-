import tldextract
import whois
from datetime import datetime

def analyze_url(url: str):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    signals = []
    risk_score = 0

    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            if age_days < 30:
                signals.append(f"Domain is newly registered ({age_days} days old)")
                risk_score += 40
            else:
                signals.append(f"Domain age is established ({age_days} days)")
    except Exception:
        signals.append("Could not retrieve WHOIS data")
        
    suspicious_keywords = ["login", "secure", "update", "verify", "bank"]
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        signals.append("URL contains common phishing keywords")
        risk_score += 20

    return {
        "domain": domain,
        "signals": signals,
        "partial_score": min(risk_score, 100)
    }
