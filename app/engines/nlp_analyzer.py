import re

def analyze_text(message: str):
    signals = []
    risk_score = 0

    # 1. Check for Urgency & Fear (Social Engineering)
    urgency_words = ["urgent", "immediately", "account suspended", "blocked", "action required", "verify now", "warning", "alert"]
    found_urgency = [word for word in urgency_words if word in message.lower()]
    if found_urgency:
        signals.append(f"Urgency/Fear triggers found: {', '.join(found_urgency)}")
        risk_score += 30

    # 2. Check for Financial/KYC context
    financial_words = ["upi", "kyc", "bank", "payment", "refund", "otp", "pin", "credit card"]
    found_financial = [word for word in financial_words if word in message.lower()]
    if found_financial:
        signals.append(f"Financial/KYC keywords found: {', '.join(found_financial)}")
        risk_score += 20

    # 3. Extract URLs in the text
    urls = re.findall(r'(https?://\S+)', message)
    if urls:
        signals.append(f"Embedded URL found: {urls[0]}")
        risk_score += 30 # URLs in SMS are highly suspicious

    return {"signals": signals, "partial_score": min(risk_score, 100)}
