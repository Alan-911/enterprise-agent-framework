import sqlite3
import time
import random
from datetime import datetime

DB_PATH = 'data/auracommerce.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

PRODUCTS = [
    ("Spark Plug A", "Automotive", 15.99),
    ("Brake Pads B", "Automotive", 45.50),
    ("Engine Oil 5W-30", "Fluids", 25.00),
    ("Air Filter C", "Automotive", 12.00),
    ("Wiper Blades", "Accessories", 20.00)
]

def stream_sales():
    conn = init_db()
    cursor = conn.cursor()
    print("Starting AuraCommerce Mock Engine... (Ctrl+C to stop)")
    try:
        while True:
            # Simulate a sale or a spike
            # 10% chance to simulate a sudden spike in 'Spark Plug A'
            if random.random() < 0.10:
                product = PRODUCTS[0] # Spark Plug A
                amount = product[2] * random.uniform(0.9, 1.1)
                print(f"[SPIKE] Inserting rapid sale for {product[0]}")
            else:
                product = random.choice(PRODUCTS)
                amount = product[2] * random.uniform(0.9, 1.1)
            
            cursor.execute(
                "INSERT INTO orders (product_name, category, amount) VALUES (?, ?, ?)",
                (product[0], product[1], amount)
            )
            conn.commit()
            print(f"[{datetime.now().isoformat()}] Sale generated: {product[0]} for ${amount:.2f}")
            
            # Sleep between 10 to 30 seconds
            time.sleep(random.uniform(10, 30))
    except KeyboardInterrupt:
        print("\nStopping Mock Engine.")
    finally:
        conn.close()

if __name__ == "__main__":
    stream_sales()
