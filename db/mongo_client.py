from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cyber_threat_db"]
    threats_collection = db["threats"]
except Exception as e:
    print("[!] MongoDB connection failed:", e)
