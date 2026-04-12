import time
import os
import threading
from prometheus_client import start_http_server, Counter, Gauge, Histogram
from dotenv import load_dotenv

from agents.analyst import analyze_data
from agents.sentinel import detect_anomalies
from agents.reporter import generate_report

# Load environment variables
load_dotenv()

# --- Prometheus Metrics ---
ORDER_VOLUME_TOTAL = Counter('order_volume_total', 'Total number of orders processed in window')
AVG_ORDER_VALUE = Gauge('avg_order_value', 'Average order value in window')
AGENT_REASONING_LATENCY = Histogram('agent_reasoning_latency_seconds', 'Time spent in agent reasoning loop')
BUSINESS_HEALTH_SCORE = Gauge('business_health_score', 'Calculated AI business health score (0-100)')

DB_PATH = 'data/auracommerce.db'

def run_agent_workflow():
    print("AuraCommerce Agent Loop Started...")
    while True:
        try:
            start_time = time.time()
            
            # Node A: Analyst (Data retrieval)
            analyst_data = analyze_data(DB_PATH)
            
            # Node B: Sentinel (AI Reasoning)
            sentinel_data = detect_anomalies(analyst_data)
            
            # Node C: Reporter (Metric Formatting)
            final_report = generate_report(sentinel_data, analyst_data)
            
            # Record Metrics
            orders = final_report['order_count']
            sales = final_report['total_sales']
            
            # Only update if there are orders
            if orders > 0:
                # We record the current window's volume
                ORDER_VOLUME_TOTAL.inc(orders)
                AVG_ORDER_VALUE.set(sales / orders)
            
            BUSINESS_HEALTH_SCORE.set(final_report['health_score'])
            
            # Log the text insight
            insight = final_report['latest_insight']
            print(f"[{time.strftime('%X')}] Health: {final_report['health_score']} | Insight: {insight}")
            
            # Record Latency
            duration = time.time() - start_time
            AGENT_REASONING_LATENCY.observe(duration)
            
            # Wait for next reasoning cycle (e.g., 15 seconds)
            time.sleep(15)
            
        except Exception as e:
            print(f"Orchestration Error: {e}")
            time.sleep(15)

if __name__ == '__main__':
    # Make sure DB exists by calling mock engine's init_db
    from data.mock_engine import init_db
    init_db()

    # Start Prometheus HTTP Server on port 8000
    start_http_server(8000)
    print("Prometheus metrics exposed on http://localhost:8000/metrics")

    # Start the LangGraph-style autonomous loop
    run_agent_workflow()
