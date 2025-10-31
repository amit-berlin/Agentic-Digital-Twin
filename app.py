# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import time
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -------------------------
# Page config & styles
# -------------------------
st.set_page_config(page_title="Earth 3.0 — Live Twin MVP", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
h1 { color: #001F3F; }
.kicker { color: #6b7280; font-size:14px; }
.card { background: #ffffff; border-radius:12px; padding:14px; box-shadow: 0 6px 18px rgba(3,12,34,0.06); }
.small { color:#394049; font-size:14px; }
.btn { border-radius:8px; padding:8px 12px; text-decoration:none; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown("<h1>🌍 Earth 3.0 — Agentic Digital Twin (Demo)</h1>", unsafe_allow_html=True)
st.markdown("**Governance that corrects itself — for Boards, UN, and Investors.**")
st.markdown("---")

# -------------------------
# Utility functions
# -------------------------
@st.cache_data(ttl=60*10)
def generate_time_series(seed=0, periods=12):
    np.random.seed(seed)
    base = np.linspace(60, 85, periods)
    noise = np.random.normal(0, 4, (periods, 3))
    cols = ['Governance', 'ESG', 'Finance']
    df = pd.DataFrame(base.reshape(-1,1) + noise, columns=cols)
    df.index = pd.date_range(end=datetime.utcnow().date(), periods=periods, freq='M')
    return df.clip(0,100).round(1)

def make_pdf_bytes(org_name, summary_lines):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 60, f"Earth 3.0 — Board Audit Snapshot • {org_name}")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 82, f"Generated: {datetime.utcnow():%B %d, %Y %H:%M UTC}")
    text = c.beginText(40, height - 120)
    text.setFont("Helvetica", 11)
    for line in summary_lines:
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

# -------------------------
# Layout: 3 cards horizontally
# -------------------------
col1, col2, col3 = st.columns([1,1,1], gap="large")

# Placeholder images (replace with your GIFs/hosted thumbnails)
IMG1 = "https://via.placeholder.com/800x400.png?text=Self-Governing+Twin"
IMG2 = "https://via.placeholder.com/800x400.png?text=ESG+Audit+Preview"
IMG3 = "https://via.placeholder.com/800x400.png?text=2100+Sustainable+Growth"

# -------------------------
# Card 1: Self-Governing Organization
# -------------------------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image(IMG1, use_column_width=True)
    st.markdown("<div style='padding-top:8px;'><div class='kicker'>Autonomous Decision Frameworks</div>", unsafe_allow_html=True)
    st.markdown("### Self-Governing Organization")
    st.markdown("<div class='small'>Codifies every board decision into auditable machine logic — real-time governance that learns and corrects itself.</div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("**Demo:** This page is a demo interface. For a live twin integration, we connect to ERP, SAP, Salesforce, PLM & Finance via an Agentic RAG fabric.")
    st.markdown("")
    st.markdown("[➡️ See Live Twin](https://share.streamlit.io/user/amit-berlin)  &nbsp;&nbsp; (opens in new tab)", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Card 2: ESG AI Audit Automation
# -------------------------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image(IMG2, use_column_width=True)
    st.markdown("<div style='padding-top:8px;'><div class='kicker'>Continuous Ethics & Risk Scoring</div>", unsafe_allow_html=True)
    st.markdown("### ESG AI Audit Automation")
    st.markdown("<div class='small'>Audits ESG, bias, and compliance in real time — ISO-aligned, self-correcting, zero human bias.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Preview Audit (Simulated)**")
    org = st.text_input("Organization name (for report)", value="Acme Global", key="org_name")
    if st.button("Run Simulated Audit"):
        # fake latency
        time.sleep(0.6)
        df = generate_time_series(seed=42)
        latest = df.iloc[-1]
        st.success("Audit complete — summary below.")

        # present as a two-column table with metric + score
        audit_df = latest.to_frame(name='Score').reset_index()
        audit_df.columns = ['Metric', 'Score']
        st.table(audit_df)

        # small plot: explicit call
        df_reset = df.reset_index().rename(columns={'index':'Date'})
        fig = px.line(df_reset, x='Date', y=['Governance','ESG','Finance'], labels={'value':'Index','variable':'Metric'})
        st.plotly_chart(fig, use_container_width=True, height=260, config={"displayModeBar": False})

        # prepare summary lines for PDF (fixed the f-string typo)
        summary_lines = [
            f"Organization: {org}",
            f"Generated: {datetime.utcnow():%B %d, %Y %H:%M UTC}",
        ]
        summary_lines += [f"{k}: {v}" for k,v in latest.items()]
        pdf_bytes = make_pdf_bytes(org, summary_lines)
        st.download_button("Download Audit Snapshot (PDF)", data=pdf_bytes, file_name=f"{org}_earth3_audit.pdf", mime="application/pdf")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Card 3: 2100 Sustainable Growth
# -------------------------
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.image(IMG3, use_column_width=True)
    st.markdown("<div style='padding-top:8px;'><div class='kicker'>Investor-Ready Governance Engine</div>", unsafe_allow_html=True)
    st.markdown("### 2100 Sustainable Growth")
    st.markdown("<div class='small'>Converts transparency into measurable enterprise value — live ESG signals for investors and boards.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Impact Simulation**")
    base_revenue = st.number_input("Current annual revenue (USD millions)", min_value=10.0, value=500.0, step=10.0, key="rev")
    invest_pct = st.slider("Percent revenue improvement from governance (simulated)", 0, 50, 8, key="improve")
    if st.button("Run Impact Simulation"):
        time.sleep(0.5)
        uplift = base_revenue * invest_pct / 100.0
        projected = base_revenue + uplift
        st.metric("Projected Annual Revenue (M USD)", f"{projected:.1f}M", delta=f"+{uplift:.1f}M")
        sim_df = pd.DataFrame({
            "Scenario":["Current","With Earth 3.0"],
            "Revenue":[base_revenue, projected]
        })
        fig = px.bar(sim_df, x="Scenario", y="Revenue", text="Revenue", height=260)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("**Explanation:** This is a simulation. Actual ROI depends on scope, systems integrated, and board adoption.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# Bottom: Contact CTA and Footnote
# -------------------------
st.markdown("### Ready to pilot Earth 3.0 with your board?")
st.markdown("Book a 15-minute introduction or request a confidential Board Readiness PDF.")
contact_col1, contact_col2 = st.columns([3,1])
with contact_col1:
    email = st.text_input("Best email for a reply", value="amitsutherland@gmail.com", key="contact_email")
with contact_col2:
    if st.button("Request Pilot Invite"):
        st.success("Thanks — your request is recorded. We'll reach out to " + email)

st.markdown("<div style='color:gray;font-size:12px;'>This is a demo MVP for investor & board pilots. Live Twin integrations require Agentic RAG connectivity to ERP, Salesforce, PLM, and ISO sources.</div>", unsafe_allow_html=True)
