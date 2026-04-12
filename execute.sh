#!/bin/bash
# AuraCommerce Initialization Script
echo "Initializing AuraCommerce Environment..."

# 1. Create Directories (ensure they exist)
mkdir -p agents data monitoring/grafana

# 2. Install Dependencies
pip install langgraph pandas prometheus_client sqlalchemy psycopg2-binary openai python-dotenv

# 3. Create Prometheus Config (if not exists)
if [ ! -f "monitoring/prometheus.yml" ]; then
cat <<EOF > monitoring/prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'auracommerce_agents'
    static_configs:
      - targets: ['host.docker.internal:8000']
EOF
fi

# 4. Generate Docker Compose for Grafana & Prometheus (Optional for local dashboard)
if [ ! -f "docker-compose.yml" ]; then
cat <<EOF > docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    extra_hosts:
      - "host.docker.internal:host-gateway"
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
EOF
fi

echo "AuraCommerce Initialized. Navigate to localhost:3000 for Grafana once docker-compose is running."
