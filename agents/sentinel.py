import os
from openai import OpenAI
import json

def detect_anomalies(analyst_data: dict):
    """
    Simulates the Sentinel Agent.
    Evaluates current performance against baseline logic and returns a health score.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # We use a rule-based mock if no API key is provided for an easy demo
    if not api_key:
        health_score = 100
        anomalies = []
        
        top_product = analyst_data.get("top_product")
        if top_product == "Spark Plug A" and analyst_data.get("order_count", 0) > 3:
            health_score = 75
            anomalies.append("Warning: Product 'Spark Plug A' is selling 3x faster than predicted. Suggesting immediate restock.")
        
        if analyst_data.get("order_count", 0) == 0:
            health_score = 40
            anomalies.append("Alert: Zero sales detected in the last hour. Verify payment gateway.")
            
        return {
            "health_score": health_score,
            "anomalies": anomalies,
            "reasoning": "Mock reasoning applied."
        }
    
    # If API key exists, use LLM
    try:
        client = OpenAI(api_key=api_key)
        prompt = f"""
        You are the Sentinel AI for AuraCommerce. 
        Analyze the following recent sales data:
        Total Sales: ${analyst_data.get('total_sales', 0)}
        Order Count: {analyst_data.get('order_count', 0)}
        Top Product: {analyst_data.get('top_product', 'N/A')}
        
        Evaluate the business health. Return a JSON object with:
        - "health_score": (int from 0 to 100)
        - "anomalies": (list of strings, warnings if any)
        - "reasoning": (string)
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Sentinel LLM Error: {e}")
        return {"health_score": 50, "anomalies": [f"LLM Error: {str(e)}"], "reasoning": "Fallback"}
