import requests
from db.mongo_client import threats_collection
from datetime import datetime
from utils.ip_geo import get_geo_location
from dotenv import load_dotenv
import os

load_dotenv()

OTX_API_KEY = os.getenv("OTX_API_KEY")
# OTX API key
OTX_API_KEY = "8f0a153cd77d391b94005d9220e90bd208894db1d989c037a1335311ec0b4c93"
OTX_URL = "https://otx.alienvault.com/api/v1/indicators/export?type=IPv4&pulse=1"

def fetch_and_store_otx_threats():
    headers = {"X-OTX-API-KEY": OTX_API_KEY}

    try:
        print("[*] Fetching real threat data from AlienVault OTX...")
        response = requests.get(OTX_URL, headers=headers)

        if response.status_code == 200:
            threats = response.text.splitlines()

            for ip in threats[:10]:  # limit for testing
                ip_address = ip.strip()

                # Get geolocation
                geo = get_geo_location(ip_address)

                # If failed, use default
                if geo is None:
                    geo = {
                        "lat": None,
                        "lon": None,
                        "city": "Unknown",
                        "country": "Unknown"
                    }

                # Construct and insert
                threat = {
                    "source": "AlienVault OTX",
                    "timestamp": datetime.utcnow(),
                    "ip": ip_address,
                    "threat_level": "high",
                    "category": "unknown",
                    "status": "new",
                    "location": geo 
                }

                threats_collection.insert_one(threat)

            print(f"[+] Inserted {len(threats[:10])} real IP threats into DB.")
        else:
            print(f"[!] Failed to fetch data: {response.status_code}")

    except Exception as e:
        print(f"[ERROR] {e}")
