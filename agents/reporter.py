def generate_report(sentinel_data: dict, analyst_data: dict):
    """
    Simulates the Reporter Agent.
    Formats insights for Grafana parsing (and logging).
    """
    latest_insight = "System Normal. Sales are tracking to baseline."
    
    anomalies = sentinel_data.get("anomalies", [])
    if anomalies:
        latest_insight = " | ".join(anomalies)
        
    return {
        "latest_insight": latest_insight,
        "health_score": sentinel_data.get("health_score", 100),
        "total_sales": analyst_data.get("total_sales", 0),
        "order_count": analyst_data.get("order_count", 0)
    }
