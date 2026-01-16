🏥 Blockchain-Enabled IoT Health Data Logger

This project ensures the integrity of health data collected from IoT devices by logging their SHA-256 hashes onto the Ethereum blockchain. It prevents data manipulation by creating an immutable ledger and allows real-time verification via a Web DApp.

The entire system is containerized with Docker, making it easy to deploy and test.
🚀 Quick Start (Docker)

You can bring up the entire stack (IoT Simulator, Blockchain Bridge, Web Dashboard) with a single command.

1. Start the System: Builds images and starts containers in the background.
Bash

docker-compose up -d --build

2. Watch Live Logs: Monitor the data flow and blockchain transactions in real-time.
Bash

docker-compose logs -f

3. Stop the System: Stops and removes the containers.
Bash

docker-compose down
4. Check logs: check system logs.

docker-compose logs -f app

5. Blockchain: Read data from blokchain.

docker-compose exec app
🔍 How to Verify Data

Once the system is running:

    Open your browser and go to http://localhost:8501.

    Click "Connect Wallet"

    Approve the connection request in the MetaMask popup.

        Once connected, click "Verify" on any data row to perform an on-chain check using your own account.

    View the incoming live sensor data.

🌟 Key Features

    IoT & MQTT: Real-time data simulation and collection.

    Automated Hashing: Python bridge automatically hashes and signs transactions.

    Smart Contract: Solidity-based immutable registry on Ethereum (Ganache).

    Wallet Integration: Users can connect their MetaMask wallets to the web dashboard.

    Decentralized Verification: Verification requests are signed and executed directly via the user's wallet, ensuring non-repudiation.

👥 Team

Developed for Muğla Sıtkı Koçman University - CENG 3550.

    İbrahim Yörük - Hardware & IoT

    Efe Emir Yüce - Blockchain & Software Architecture

<img width="2816" height="1536" alt="System Architecture" src="https://github.com/user-attachments/assets/bc394034-101c-4fe8-b97e-d5a433ec659d" />

