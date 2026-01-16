import sys
import json
import time
from web3 import Web3
from solcx import compile_standard, install_solc
from datetime import datetime

GANACHE_URL = "http://ganache:8545"
SOL_FILE = "HealthLogger.sol"

def read_contract_data(contract_address):
    print(f"Connecting to Blockchain at {GANACHE_URL}...")
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    
    if not w3.is_connected():
        print("Error: Could not connect to Ganache.")
        return

    # Compile to get ABI
    install_solc('0.8.0')
    with open(SOL_FILE, "r") as file:
        source_content = file.read()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {SOL_FILE: {"content": source_content}},
        "settings": {"outputSelection": {"*": {"*": ["abi"]}}},
    }, solc_version='0.8.0')

    # --- DÜZELTME BURADA ---
    # Metadata parsing yerine doğrudan ABI alıyoruz
    abi = compiled_sol["contracts"][SOL_FILE]["HealthLogger"]["abi"]

    address = w3.to_checksum_address(contract_address)
    contract = w3.eth.contract(address=address, abi=abi)

    try:
        count = contract.functions.getLogCount().call()
        print(f"\nTotal Logs: {count}")
        print("-" * 60)
        print(f"{'Index':<5} | {'Timestamp':<20} | {'Data Hash (SHA256)'}")
        print("-" * 60)

        for i in range(count):
            log_data = contract.functions.logs(i).call()
            data_hash = log_data[0]
            timestamp_raw = log_data[1]
            readable_time = datetime.fromtimestamp(timestamp_raw).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{i:<5} | {readable_time:<20} | {data_hash}")
            
    except Exception as e:
        print(f"Error reading contract: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reader.py <CONTRACT_ADDRESS>")
    else:
        read_contract_data(sys.argv[1])