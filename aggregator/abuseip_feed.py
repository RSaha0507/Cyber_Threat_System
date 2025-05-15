import requests
from db.mongo_client import threats_collection
from datetime import datetime
from utils.ip_geo import get_geo_location
from dotenv import load_dotenv
import os

load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

ABUSEIPDB_API_KEY = "USE YOUR OWN"

def fetch_and_store_abuseip_threats():
    try:
        print("[INFO] Fetching AbuseIPDB blacklisted IPs...")
        url = "https://api.abuseipdb.com/api/v2/blacklist"
        headers = {
            "Key": ABUSEIPDB_API_KEY,
            "Accept": "application/json"
        }
        params = {
            "confidenceMinimum": 90,
            "limit": 10  # pull top 10 high-confidence threats
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            new_threats = []

            for ip in data["data"]:
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

                threat = {
                    "source": "AbuseIPDB",
                    "timestamp": datetime.utcnow(),
                    "ip": ip_address,
                    "threat_level": "critical",
                    "category": "abuse",
                    "status": "new",
                    "location": geo 
                }
                new_threats.append(threat)

            if new_threats:
                threats_collection.insert_many(new_threats)
                print(f"[+] Inserted {len(new_threats)} AbuseIPDB threats.")
        else:
            print(f"[!] API error: {response.status_code}")

    except Exception as e:
        print(f"[ERROR] {e}")
