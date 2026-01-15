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

    Login by "admin" as username and "123" as password (just demo)

    View the incoming live sensor data.

🌟 Key Features

    IoT & MQTT: Real-time data simulation and collection.

    Automated Hashing: Python bridge automatically hashes and signs transactions.

    Smart Contract: Solidity-based immutable registry on Ethereum (Ganache).

👥 Team

Developed for Muğla Sıtkı Koçman University - CENG 3550.

    İbrahim Yörük - Hardware & IoT

    Efe Emir Yüce - Blockchain & Software Architectureß
