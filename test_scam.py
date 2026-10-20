from app.engines.risk_engine import calculate_global_risk

# Ek fake scam message test karte hain
fake_sms = "URGENT: Your bank account is blocked. Verify your KYC immediately to avoid suspension. Click here: http://fake-bank-kyc-update.com"

print("Scanning Message...")
result = calculate_global_risk(message=fake_sms)

print("\n--- SCAN RESULT ---")
print(f"Risk Score: {result['risk_score']}/100")
print(f"Severity: {result['severity']}")
print("\nWhy was it flagged (Explainable AI)?")
for signal in result['explainable_ai']['nlp_text_signals']:
    print(f"- {signal}")
