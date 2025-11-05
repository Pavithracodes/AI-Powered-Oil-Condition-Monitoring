# 🛢️ Oil Condition Monitoring System

A real-time **IoT + Data Engineering + Machine Learning** project that monitors vehicle oil condition and alerts for maintenance needs using **Streamlit, Supabase, and Telegram Bot**.

---

## 🚀 Project Overview

This project simulates live **sensor data** (oil viscosity, temperature, and level) from trucks and stores it in a **Supabase (PostgreSQL)** database.  
A **Streamlit dashboard** visualizes these readings in real-time and triggers **Telegram alerts** when thresholds are crossed.

The system demonstrates a modern **data engineering workflow** — from data generation → storage → transformation → visualization → ML-based prediction.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Data Simulation** | Python (`simulator.py`) |
| **Database** | Supabase (PostgreSQL) |
| **Backend / ETL** | Python + Supabase client |
| **Dashboard** | Streamlit + Matplotlib + Plotly |
| **Machine Learning** | Scikit-learn (Predictive maintenance model) |
| **Alerts** | Telegram Bot API |
| **Environment Variables** | dotenv (`.env` file) |
| **Version Control** | Git + GitHub |

---

## ⚙️ Features

- 🔄 **Live Data Streaming** from multiple vehicles  
- 🗃️ **Real-time Database Storage** using Supabase  
- 📊 **Interactive Dashboard** built with Streamlit  
- 🤖 **Machine Learning Prediction** of oil failure risk  
- 🚨 **Automated Telegram Alerts** for critical conditions  
- 🧱 **Modular Architecture** (Simulator → Database → Dashboard → ML)  
- ☁️ **Environment-based Configuration** with `.env`  

---

## 🧠 System Architecture

```text
+-----------------+       +----------------+       +----------------+       +----------------+
|  Data Simulator | --->  | Supabase (DB)  | --->  | ML Model (ETL) | --->  | Streamlit Dash |
+-----------------+       +----------------+       +----------------+       +----------------+
                                     |
                                     v
                             🚨 Telegram Alerts


🧪 How to Run Locally

1️⃣ Clone the Repository
git clone https://github.com/<yourusername>/oil-condition-monitoring.git
cd oil-condition-monitoring

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Environment Variables
Create a .env file and add:
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

5️⃣ Start Components
Start Data Simulator:
python simulator.py
Start Dashboard:
streamlit run dashboard.py

🧮 Machine Learning Component
The ML module uses Random Forest Classifier to predict potential oil degradation or failure based on:
Viscosity
Temperature
Oil Level
Predictions are visualized in the dashboard and used to trigger alerts.

📬 Telegram Alerts
When the ML model predicts a critical oil condition, the system sends an alert to your Telegram bot.
To test manually:
python test_telegram.py

📁 Folder Structure
oil-condition-monitoring/
│
├── simulator.py             # Data generator (IoT simulation)
├── dashboard.py             # Streamlit dashboard
├── ml_model.py              # Machine learning predictive model
├── test_telegram.py         # Test Telegram alert system
├── requirements.txt         # Dependencies
├── .env                     # Environment variables (not pushed)
├── .gitignore               # Ignore sensitive files
└── README.md                # Project documentation

🧠 Future Enhancements
Add Kafka or MQTT for real-time data streaming
Integrate Airflow for orchestration
Containerize with Docker
Deploy Streamlit app on AWS/GCP

👨‍💻 Author
Pavithra P
📧 [Email : (pavithrap1176@gmail.com)]
🔗 [LinkedIn Profile:]((https://www.linkedin.com/in/pavithra-p-36431b244/))

⭐ Contribute
If you’d like to improve this project:
Fork this repo
Create a new branch (feature/new-feature)
Submit a PR!

📜 License
License © 2025 [Pavithra P]
