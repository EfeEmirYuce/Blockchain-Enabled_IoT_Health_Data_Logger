import os
import json
import time
from hashlib import sha256
from datetime import datetime
from web3 import Web3
import paho.mqtt.client as mqtt
from solcx import compile_standard, install_solc

# --- CONFIGURATION FROM ENV ---
GANACHE_URL = os.getenv('GANACHE_URL', 'http://127.0.0.1:8545')
MQTT_BROKER = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'test/topic')

# File Paths
DATA_DIR = "/app/data"
LOG_FILE = os.path.join(DATA_DIR, "sensor_logs.jsonl")
SOL_FILE = "HealthLogger.sol"

# --- 1. BLOCKCHAIN CONNECTION ---
print("[SYSTEM] Connecting to Blockchain...")
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Wait for Ganache to start up
while not w3.is_connected():
    print("[SYSTEM] Waiting for Blockchain... (Retrying in 3s)")
    time.sleep(3)

print(f"[SYSTEM] Blockchain Connected: {GANACHE_URL}")
w3.eth.default_account = w3.eth.accounts[0] 

# --- 2. SMART CONTRACT DEPLOYMENT ---
def deploy_contract():
    print(f"[SYSTEM] Compiling and Deploying {SOL_FILE}...")
    
    install_solc('0.8.0')
    
    with open(SOL_FILE, "r") as file:
        source_content = file.read()

    # Derleme ayarları
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {SOL_FILE: {"content": source_content}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    }, solc_version='0.8.0')

    # --- DÜZELTME BURADA YAPILDI ---
    # Eski hatalı satır: abi = json.loads(...metadata...)["output"]["abi"]
    # Yeni doğrusu: Doğrudan ["abi"] anahtarını alıyoruz.
    
    contract_interface = compiled_sol["contracts"][SOL_FILE]["HealthLogger"]
    bytecode = contract_interface["evm"]["bytecode"]["object"]
    abi = contract_interface["abi"]

    # Deploy
    HealthLogger = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = HealthLogger.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"[SYSTEM] Contract Deployed at: {tx_receipt.contractAddress}")
    
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Initialize Contract
contract_instance = deploy_contract()

# --- HELPER FUNCTIONS ---

def save_to_local_disk(payload_dict):
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        payload_dict['received_at'] = datetime.now().isoformat()
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(payload_dict) + "\n")
        print("[DISK] Data saved locally.")
    except Exception as e:
        print(f"[ERROR] Disk Write Failed: {e}")

def send_hash_to_blockchain(payload_dict):
    try:
        data_string = json.dumps(payload_dict, sort_keys=True)
        data_hash = sha256(data_string.encode('utf-8')).hexdigest()
        
        print(f"[CHAIN] Sending Hash: {data_hash}...")
        
        tx_hash = contract_instance.functions.addHash(data_hash).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"[CHAIN] Transaction Confirmed.")
        
    except Exception as e:
        print(f"[ERROR] Blockchain Transaction Failed: {e}")

# --- 3. MQTT CLIENT SETUP ---

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"[MQTT] Connection Failed. Code: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode('utf-8')
        print(f"\n[MQTT] Received Message: {payload_str}")
        payload_data = json.loads(payload_str)
        save_to_local_disk(payload_data)
        send_hash_to_blockchain(payload_data)
    except json.JSONDecodeError:
        print("[WARNING] Received non-JSON data. Ignored.")
    except Exception as e:
        print(f"[ERROR] Processing Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"[SYSTEM] Connecting to MQTT Broker: {MQTT_BROKER}...")

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"[FATAL] Could not connect to MQTT: {e}")