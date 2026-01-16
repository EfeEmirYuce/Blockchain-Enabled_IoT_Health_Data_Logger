import json
import os
from hashlib import sha256

# Docker volume ile buraya bağlamıştık
LOG_FILE = "data/sensor_logs.jsonl"

def verify_data():
    if not os.path.exists(LOG_FILE):
        print("Veri dosyası bulunamadı!")
        return

    print(f"{'Zaman Damgası (JSON)':<30} | {'Hesaplanan Hash (SHA256)'}")
    print("-" * 100)

    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                # 1. Satırı oku
                data = json.loads(line)
                timestamp = data.get('received_at', 'Bilinmiyor')
                
                # 2. Birebir aynı yöntemle tekrar Hash'le
                # (Main.py'deki sıralama mantığıyla aynı olmalı: sort_keys=True)
                data_string = json.dumps(data, sort_keys=True)
                recalculated_hash = sha256(data_string.encode('utf-8')).hexdigest()
                
                print(f"{timestamp:<30} | {recalculated_hash}")
            except Exception as e:
                print(f"Hata: {e}")

if __name__ == "__main__":
    verify_data()