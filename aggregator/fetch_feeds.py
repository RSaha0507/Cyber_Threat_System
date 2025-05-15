import random
import datetime
from db.mongo_client import threats_collection

# Simulated threat sources
sources = ["AlienVault", "Cisco Talos", "AbuseIPDB", "ThreatCrowd", "Shodan"]

def generate_fake_threat():
    return {
        "source": random.choice(sources),
        "timestamp": datetime.datetime.utcnow(),
        "ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "threat_level": random.choice(["low", "medium", "high"]),
        "category": random.choice(["malware", "phishing", "ransomware", "ddos", "botnet"]),
        "status": "new"
    }

def ingest_threat():
    threat = generate_fake_threat()
    threats_collection.insert_one(threat)
    print(f"[+] Inserted Threat: {threat}")
