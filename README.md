# AuraCommerce — Agentic Business Intelligence Dashboard

> A 3-agent pipeline that monitors an e-commerce business in real time: an Analyst reads the database, a Sentinel detects anomalies (via OpenAI or rule-based fallback), and a Reporter formats insights for the live dashboard.

**[🚀 Live Demo →](https://enterprise-agent-framework.vercel.app)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-monitoring-e6522c.svg)](https://prometheus.io)
[![Live Demo](https://img.shields.io/badge/Demo-Live-22c55e.svg)](https://enterprise-agent-framework.vercel.app)

---

## What It Does

AuraCommerce is a business intelligence system built for an auto-parts e-commerce platform. Three independent agents run continuously:

1. **Analyst Agent** — queries the SQLite order database, computes sales totals, order counts, and top products for the last hour
2. **Sentinel Agent** — evaluates the Analyst's output against business baselines, flags anomalies (e.g. a product selling 3× faster than forecast = restock alert). Uses GPT-4o-mini if an API key is present; falls back to deterministic rule logic for zero-cost demos
3. **Reporter Agent** — formats the Sentinel's findings into structured insight strings consumed by the live dashboard

The FastAPI backend polls these agents and streams live state to a Plotly.js frontend.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Background Thread (run_agent_loop)                     │
│                                                         │
│  SQLite DB (orders)                                     │
│       │                                                 │
│       ▼                                                 │
│  analyst.py → analyze_data()                           │
│       │  total_sales / order_count / top_product        │
│       ▼                                                 │
│  sentinel.py → detect_anomalies()                      │
│       │  [no API key] rule-based health scoring         │
│       │  [OPENAI_API_KEY set] GPT-4o-mini reasoning     │
│       │  → health_score (0-100) + anomaly list          │
│       ▼                                                 │
│  reporter.py → generate_report()                       │
│       └─ formats insight string for dashboard           │
└──────────────────────────┬──────────────────────────────┘
                           │  in-memory shared state dict
                           ▼
               FastAPI  /api/state?timeframe=...
                           │
                           ▼
              ┌────────────────────────┐
              │   Plotly.js Frontend   │
              │  (polling every 2s)    │
              │                        │
              │  • Sales trend chart   │
              │  • Health score gauge  │
              │  • Inventory gauge     │
              │  • Sentiment polarity  │
              │  • Google/FB ROAS      │
              │  • Agent latency chart │
              └────────────────────────┘
                           │
               FastAPI  /api/export_report
                           │
                           ▼
                    PDF Report (fpdf2)
                  auto-generated on demand
```

---

## Agent Details

### Analyst Agent (`agents/analyst.py`)

Queries the last hour of orders from SQLite and computes:
- `total_sales` — revenue sum
- `order_count` — number of orders
- `top_product` — mode of `product_name` column
- `raw_data` — last 10 order records (passed as LLM context to Sentinel)

```python
query = f"SELECT * FROM orders WHERE timestamp >= '{one_hour_ago.isoformat()}'"
df = pd.read_sql_query(query, conn)
top_product = df['product_name'].mode().iloc[0]
```

### Sentinel Agent (`agents/sentinel.py`)

**Dual-mode design** — works with or without an API key:

```python
if not api_key:
    # Rule-based: fast, zero-cost, always available
    if top_product == "Spark Plug A" and order_count > 3:
        health_score = 75
        anomalies.append("Warning: Spark Plug A selling 3× faster — suggest restock")
    if order_count == 0:
        health_score = 40
        anomalies.append("Alert: Zero sales detected — verify payment gateway")
else:
    # LLM mode: GPT-4o-mini evaluates open-ended business context
    prompt = f"Analyze: Total Sales ${total_sales}, Orders {order_count}, Top Product {top_product}..."
    # Returns: { health_score, anomalies: [], reasoning: "..." }
```

This pattern — rule-based fallback + optional LLM upgrade — is a production reliability technique: the system never goes down because an API call fails.

### Reporter Agent (`agents/reporter.py`)

Aggregates Sentinel + Analyst outputs into a single insight string:

```python
def generate_report(sentinel_data, analyst_data):
    if sentinel_data.get("anomalies"):
        latest_insight = " | ".join(sentinel_data["anomalies"])
    else:
        latest_insight = "System Normal. Sales tracking to baseline."
    return { "latest_insight": latest_insight, "health_score": ..., "total_sales": ... }
```

---

## Dashboard Features

**6 live Plotly.js charts** update every 2 seconds via polling:

| Chart | What it shows |
|---|---|
| Sales Trend | Hourly / daily revenue + anomaly overlay |
| Health Score | Gauge (0–100) updated by Sentinel |
| Inventory Runway | Days of stock remaining (gauge) |
| Sentiment Polarity | Customer sentiment over time (line chart) |
| ROAS | Google vs Facebook return on ad spend (bar) |
| Agent Latency | Per-node fetch / reasoning / action times |

**Timeframe scaling** — `/api/state?timeframe=Last 24 Hours` scales all metrics proportionally, demonstrating multi-window analysis without a time-series database.

**PDF Report Export** — `/api/export_report` auto-generates a business report with executive summary, deep reason logs, and advertising performance data using `fpdf2`. Served as a direct download.

**Theme switching** — dashboard supports 3 color themes (default/red/blue) applied dynamically via CSS variables + Plotly chart redraw.

---

## Quick Start

```bash
git clone https://github.com/Alan-911/enterprise-agent-framework
cd enterprise-agent-framework
pip install fastapi uvicorn fpdf2 pandas openai python-dotenv

# Optional: set OPENAI_API_KEY for LLM-powered Sentinel
# Without it, rule-based fallback runs automatically
cp .env.example .env

python main.py
# Server live at http://localhost:8000
# Dashboard: http://localhost:8000/
# State API:  http://localhost:8000/api/state
# PDF export: http://localhost:8000/api/export_report
```

**Generate mock order data:**
```bash
python data/mock_engine.py
# Populates data/auracommerce.db with synthetic order records
```

---

## Monitoring

Prometheus scrape config included at `monitoring/prometheus.yml`. Point a Prometheus instance at `http://localhost:8000/metrics` to track agent health, response latency, and anomaly frequency over time.

---

## Repo Structure

```
├── agents/
│   ├── analyst.py       # SQL queries → sales metrics
│   ├── reporter.py      # Formats Sentinel + Analyst output
│   └── sentinel.py      # Anomaly detection: rule-based or GPT-4o-mini
├── data/
│   ├── auracommerce.db  # SQLite order database
│   └── mock_engine.py   # Populates DB with synthetic orders
├── monitoring/
│   └── prometheus.yml   # Prometheus scrape config
├── ui/
│   ├── index.html       # Dashboard shell
│   ├── app.js           # Plotly.js charts + polling loop
│   └── style.css        # Dark theme
├── main.py              # FastAPI app + background agent loop
├── dashboard.py         # Dashboard setup helper
└── execute.sh           # One-command startup script
```

## Stack

`Python 3.11` · `FastAPI` · `Uvicorn` · `SQLite` · `pandas` · `OpenAI API (GPT-4o-mini)` · `fpdf2` · `Plotly.js` · `Prometheus`

---

Built by [Yves Alain Iragena](https://alan-911.github.io/my-portfolio) · MAIL Lab, Catholic University of America · iragena@cua.edu
