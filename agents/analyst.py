import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def analyze_data(db_path: str):
    """
    Simulates the Analyst Agent.
    Pulls the last hour of sales data and computes metrics.
    """
    try:
        conn = sqlite3.connect(db_path)
        # Pull latest data
        one_hour_ago = datetime.now() - timedelta(hours=1)
        query = f"SELECT * FROM orders WHERE timestamp >= '{one_hour_ago.isoformat()}'"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return {"total_sales": 0, "order_count": 0, "top_product": None, "raw_data": []}

        total_sales = df['amount'].sum()
        order_count = len(df)
        top_product = df['product_name'].mode().iloc[0] if not df.empty else None

        # Convert to records for LLM context
        raw_data = df.to_dict('records')

        return {
            "total_sales": total_sales,
            "order_count": order_count,
            "top_product": top_product,
            "raw_data": raw_data[-10:] # send latest 10 for context
        }
    except Exception as e:
        print(f"Analyst Error: {e}")
        return {"total_sales": 0, "order_count": 0, "top_product": None, "raw_data": []}
