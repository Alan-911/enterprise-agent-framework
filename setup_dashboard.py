import urllib.request
import zipfile
import os
import shutil

def setup():
    os.makedirs("monitoring/bin", exist_ok=True)
    
    # 1. Prometheus
    prom_url = "https://github.com/prometheus/prometheus/releases/download/v2.51.1/prometheus-2.51.1.windows-amd64.zip"
    prom_zip = "monitoring/bin/prom.zip"
    if not os.path.exists("monitoring/bin/prometheus"):
        print("Downloading Prometheus...")
        urllib.request.urlretrieve(prom_url, prom_zip)
        print("Extracting Prometheus...")
        with zipfile.ZipFile(prom_zip, 'r') as zip_ref:
            zip_ref.extractall("monitoring/bin/prometheus")
        os.remove(prom_zip)
    
    # 2. Grafana
    grafana_url = "https://dl.grafana.com/oss/release/grafana-10.4.1.windows-amd64.zip"
    grafana_zip = "monitoring/bin/grafana.zip"
    if not os.path.exists("monitoring/bin/grafana"):
        print("Downloading Grafana...")
        urllib.request.urlretrieve(grafana_url, grafana_zip)
        print("Extracting Grafana...")
        with zipfile.ZipFile(grafana_zip, 'r') as zip_ref:
            zip_ref.extractall("monitoring/bin/grafana")
        os.remove(grafana_zip)

    print("Download and extraction complete!")

if __name__ == "__main__":
    setup()
