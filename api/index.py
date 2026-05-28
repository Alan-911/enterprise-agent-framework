import math
import time
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response, HTMLResponse
from mangum import Mangum
from fpdf import FPDF
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _t():
    return time.time()

def get_state(scale: float = 1.0):
    t = _t()
    health_score = 88 + math.sin(t / 60) * 3
    sentiment_score = 4.2 + math.sin(t / 120) * 0.15
    roas_fb = 67.28 + math.sin(t / 90) * 2
    roas_google = 85.33 + math.sin(t / 75) * 2.5
    anomaly_val = 24000 + math.sin(t / 30) * 5000

    logs = [
        f"[{time.strftime('%H:%M:%S')}] Sentinel Agent: {'Anomaly detected — ROAS dip.' if math.sin(t/45) < -0.7 else 'No Anomalies Detected.'}",
        f"[{time.strftime('%H:%M:%S', time.localtime(t-5))}] Analyst Agent: Summary generated. Inventory low on 'Spark Plug A'. Suggest Procurement.",
        f"[{time.strftime('%H:%M:%S', time.localtime(t-10))}] Reporting Agent: Pushed latest metrics to Prometheus.",
    ]

    return {
        "health_score": health_score,
        "inventory_days": 12,
        "sentiment_text": "POSITIVE" if sentiment_score >= 3.5 else "NEUTRAL",
        "sentiment_score": sentiment_score,
        "roas_fb": roas_fb,
        "roas_google": roas_google,
        "logs": logs,
        "sales_trend": {
            "x": ["10:00", "12:00", "14:00", "16:00", "18:00"],
            "hourly": [v * scale for v in [16000, 18000, 16000, 26000, 21000]],
            "daily":  [v * scale for v in [13000, 15000, 13000, 18000, 20000]],
            "anomaly": [v * scale for v in [23000, 24000, 18000, anomaly_val, 24000]],
        },
        "sentiment_polarity": {
            "x": ["08:00", "10:00", "12:00", "14:00", "16:00"],
            "y": [-0.6 + math.sin(t / 200) * 0.1, 0.1, 0.4, 0.6, 0.2 + math.sin(t / 150) * 0.05],
        },
        "latency": {
            "nodes": ["Node 1", "Node 2", "Node 3", "Node 4", "Node 5"],
            "fetch":  [30, 40, 50, 45, 60],
            "reason": [40, 50, 60, 55, 70],
            "action": [20, 30, 40, 35, 50],
        },
    }


@app.get("/api/state")
def api_state(timeframe: str = "Last 10 Min"):
    scale = {"Last 1 Hour": 5.0, "Last 24 Hours": 24.0}.get(timeframe, 1.0)
    return get_state(scale)


@app.get("/api/export_report")
def api_export(timeframe: str = "Last 10 Min"):
    s = get_state()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 15, "AuraCommerce - Agentic Business Report", ln=True, align="C")
    pdf.set_font("helvetica", "I", 12)
    pdf.cell(0, 10, f"Timeframe: {timeframe}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, f"Business Health Score: {s['health_score']:.1f}%", ln=True)
    pdf.cell(0, 10, f"Projected Inventory Runway: {s['inventory_days']} Days", ln=True)
    pdf.cell(0, 10, f"Customer Sentiment: {s['sentiment_text']} ({s['sentiment_score']:.1f}/5)", ln=True)
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "2. Agent Logs", ln=True)
    pdf.set_font("helvetica", "", 10)
    for log in s["logs"]:
        pdf.multi_cell(0, 8, log)
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "3. Advertising Performance", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, f"Google ROAS: {s['roas_google']:.2f}%", ln=True)
    pdf.cell(0, 10, f"Facebook ROAS: {s['roas_fb']:.2f}%", ln=True)
    pdf_bytes = pdf.output()
    fname = f"AuraCommerce_Report_{timeframe.replace(' ', '_')}.pdf"
    return Response(content=bytes(pdf_bytes), media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={fname}"})


@app.get("/")
def root():
    p = os.path.join(BASE_DIR, "ui", "index.html")
    if os.path.exists(p):
        return FileResponse(p)
    return HTMLResponse("<h1>AuraCommerce</h1>")


@app.get("/{path:path}")
def static_files(path: str):
    p = os.path.realpath(os.path.join(BASE_DIR, path))
    if p.startswith(os.path.realpath(BASE_DIR)) and os.path.exists(p):
        return FileResponse(p)
    return HTMLResponse("Not found", status_code=404)


handler = Mangum(app, lifespan="off")
