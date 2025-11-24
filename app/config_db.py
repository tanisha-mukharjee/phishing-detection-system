# app/config_db.py
from pymongo import MongoClient
import certifi

def get_db_connection():
    try:
        # ✅ Step 1: Use your actual MongoDB Atlas connection string
        client = MongoClient(
            "mongodb+srv://mukharjeetanisha05_db_user:Lsceol8m7FaR7noH@cluster0.591exvf.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where()  # ✅ Ensures SSL certificate verification
        )

        # ✅ Step 2: Select the database name (you can choose any you like)
        db = client["phishing_detection_db"]
        print("✅ Connected to MongoDB Atlas successfully!")
        return db

    except Exception as e:
        print("❌ MongoDB Connection Failed:", e)
        return None
