import streamlit as st
from app.engines.risk_engine import calculate_global_risk

# Page ki setting
st.set_page_config(page_title="CYBERGUARD X", page_icon="🛡️", layout="wide")

st.title("🛡️ CYBERGUARD X Dashboard")
st.markdown("### Next-Generation AI-Powered Threat Intelligence Platform")
st.write("---")

# Do columns banate hain: ek URL ke liye, ek SMS ke liye
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔗 URL / Domain Scanner")
    url_input = st.text_input("Enter a suspicious URL:", placeholder="http://secure-bank-update.com")
    if st.button("Scan URL"):
        if url_input:
            with st.spinner("Analyzing URL..."):
                result = calculate_global_risk(url=url_input)
                display_result(result)
        else:
            st.warning("Please enter a URL first.")

with col2:
    st.subheader("✉️ SMS / Email Scam Scanner")
    msg_input = st.text_area("Paste SMS or Email text:", placeholder="URGENT: Your account is blocked. Verify KYC now...")
    if st.button("Scan Message"):
        if msg_input:
            with st.spinner("Analyzing Message..."):
                result = calculate_global_risk(message=msg_input)
                display_result(result)
        else:
            st.warning("Please enter a message first.")

# Result dikhane ka function
def display_result(result):
    st.write("---")
    score = result['risk_score']
    severity = result['severity']
    
    # Score ke hisaab se color
    if severity == "CRITICAL":
        st.error(f"🚨 **RISK SCORE: {score}/100 ({severity})**")
    elif severity == "HIGH":
        st.warning(f"⚠️ **RISK SCORE: {score}/100 ({severity})**")
    elif severity == "MEDIUM":
        st.info(f"ℹ️ **RISK SCORE: {score}/100 ({severity})**")
    else:
        st.success(f"✅ **RISK SCORE: {score}/100 ({severity})**")

    # Explainable AI (XAI) Breakdown
    st.markdown("#### 🔍 Why was it flagged? (Explainable AI)")
    xai = result['explainable_ai']
    
    if xai['url_structural_signals']:
        st.markdown("**URL Structural Analysis:**")
        for sig in xai['url_structural_signals']:
            st.write(f"- {sig}")
            
    if xai['threat_intel_signals']:
        st.markdown("**Threat Intelligence:**")
        for sig in xai['threat_intel_signals']:
            st.write(f"- {sig}")

    if xai['nlp_text_signals']:
        st.markdown("**NLP Text Analysis:**")
        for sig in xai['nlp_text_signals']:
            st.write(f"- {sig}")
