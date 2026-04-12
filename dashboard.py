import streamlit as st
import sqlite3
import pandas as pd
import requests
import time
import plotly.express as px

st.set_page_config(page_title="AuraCommerce Command Center", layout="wide")

# Connect to database
DB_PATH = 'data/auracommerce.db'

def get_db_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM orders ORDER BY timestamp DESC LIMIT 100", conn)
    conn.close()
    return df

def get_prometheus_metrics():
    try:
        response = requests.get("http://localhost:8000/metrics")
        content = response.text
        # Parse health score
        health_score = 100.0
        for line in content.split('\n'):
            if line.startswith('business_health_score'):
                health_score = float(line.split(' ')[1])
                break
        return health_score
    except:
        return 100.0

st.title("🤖 AuraCommerce Command Center")
st.markdown("Live Autonomous BI & Agentic Observability Stack")

# Auto-refresh logic utilizing st.empty()
placeholder = st.empty()

while True:
    try:
        df = get_db_data()
        health = get_prometheus_metrics()
        
        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="Business Health Score (AI)", value=f"{health}%", delta="-5%" if health < 90 else "+1%")
            with col2:
                total_orders = len(df)
                st.metric(label="Recent Volume (100 Window)", value=total_orders)
            with col3:
                sales = df['amount'].sum() if not df.empty else 0
                st.metric(label="Recent Revenue", value=f"${sales:,.2f}")
                
            st.divider()
            
            col_chart, col_data = st.columns([2, 1])
            
            with col_chart:
                st.subheader("Live Sales by Product")
                if not df.empty:
                    fig = px.bar(df, x='timestamp', y='amount', color='product_name', title="Live Sales Stream")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Awaiting initial data stream...")
            
            with col_data:
                st.subheader("Latest Agent Anomalies")
                if health < 90:
                    st.error("⚠️ Anomaly Detected! Sentinel AI flagged irregular volume spikes in Spark Plug A.")
                elif len(df) == 0:
                    st.warning("No sales volume. Check infrastructure.")
                else:
                    st.success("System Normal. Baseline metrics holding steady.")
                    
                st.subheader("Raw Stream")
                st.dataframe(df[['timestamp', 'product_name', 'amount']].head(10), use_container_width=True)
                
    except Exception as e:
        st.error(f"Waiting for backend... ({e})")
        
    time.sleep(2)
