import time
import os
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client
import requests

# Load environment variables
load_dotenv()

# CONFIG
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
VEHICLES = os.getenv("VEHICLE_IDS", "truck-1,truck-2").split(",")
SLEEP_SECONDS = float(os.getenv("SLEEP_SECONDS", "5"))

# Alert thresholds
THRESHOLD_VISCOSITY_HIGH = float(os.getenv("THRESHOLD_VISCOSITY_HIGH", "120.0"))  # cP
THRESHOLD_OIL_LEVEL_LOW = float(os.getenv("THRESHOLD_OIL_LEVEL_LOW", "20.0"))    # percent

# Telegram config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Supabase client
client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def send_telegram(msg: str):
    """Send alert to Telegram if configured"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
        return resp.ok
    except Exception as e:
        print("Telegram error:", e)
        return False


def simulate_reading(vehicle_id: str):
    """Generate fake sensor reading"""
    oil_temp_c = round(random.uniform(60, 95), 2)       # degrees C
    viscosity_cp = round(random.uniform(40, 140), 2)    # centipoise
    oil_level_pct = round(random.uniform(5, 100), 2)    # percent
    pressure_kpa = round(random.uniform(60, 200), 2)

    raw = {"sim": True}
    return {
        "vehicle_id": vehicle_id,
        "oil_temp_c": oil_temp_c,
        "viscosity_cp": viscosity_cp,
        "oil_level_pct": oil_level_pct,
        "pressure_kpa": pressure_kpa,
        "raw_json": raw,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def insert_reading(payload: dict):
    """Insert sensor reading into Supabase"""
    try:
        resp = client.table("sensor_readings").insert(payload).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        print("Insert error:", e)
        return None


def insert_alert(reading_id, vehicle_id, severity, message):
    """Insert alert record into Supabase"""
    try:
        rec = {
            "reading_id": reading_id,
            "vehicle_id": vehicle_id,
            "severity": severity,
            "message": message,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        resp = client.table("alerts").insert(rec).execute()
        return resp
    except Exception as e:
        print("Alert insert error:", e)
        return None


if __name__ == "__main__":
    assert SUPABASE_URL and SUPABASE_SERVICE_KEY, "❌ Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env"

    print("✅ Starting simulator — sending data to", SUPABASE_URL)

    try:
        while True:
            for v in VEHICLES:
                r = simulate_reading(v)
                inserted = insert_reading(r)

                if inserted:
                    rid = inserted.get("id")
                    visc = r["viscosity_cp"]
                    lvl = r["oil_level_pct"]

                    if visc > THRESHOLD_VISCOSITY_HIGH and lvl < THRESHOLD_OIL_LEVEL_LOW:
                        msg = f"🚨 CRITICAL: {v} viscosity={visc}cP level={lvl}%"
                        print(msg)
                        insert_alert(rid, v, "critical", msg)
                        send_telegram(msg)

                    elif visc > THRESHOLD_VISCOSITY_HIGH:
                        msg = f"⚠️ WARNING: high viscosity for {v} → {visc}cP"
                        print(msg)
                        insert_alert(rid, v, "warning", msg)

                    elif lvl < THRESHOLD_OIL_LEVEL_LOW:
                        msg = f"⚠️ WARNING: low oil level for {v} → {lvl}%"
                        print(msg)
                        insert_alert(rid, v, "warning", msg)

            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print("🛑 Simulator stopped")
