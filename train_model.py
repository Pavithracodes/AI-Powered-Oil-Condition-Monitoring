# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

# Fetch data from Supabase
resp = client.table("sensor_readings").select("*").execute()
df = pd.DataFrame(resp.data)

if df.empty:
    print("⚠️ No data found in Supabase. Please run the simulator for a while first.")
    exit()

# Label oil health
def label(row):
    if row["oil_level_pct"] < 20:
        return "critical"
    elif row["oil_level_pct"] < 50:
        return "warning"
    else:
        return "good"

df["status"] = df.apply(label, axis=1)

# Select features and label
X = df[["oil_temp_c", "viscosity_cp", "pressure_kpa"]]
y = df["status"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "oil_health_model.pkl")
print("✅ Model trained and saved successfully as oil_health_model.pkl")
