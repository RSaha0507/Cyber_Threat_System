import time
import random

# Define different types of simulated anomalies
ANOMALY_TYPES = [
    "Port Scan Detected",
    "Multiple Failed Logins",
    "Unusual Data Exfiltration",
    "Malware Signature Match",
    "Suspicious IP Communication"
]

# Predefined severity levels
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]

class Alert:
    def __init__(self, anomaly_type, severity):
        self.anomaly_type = anomaly_type
        self.severity = severity
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.alert_id = f"ALERT-{random.randint(1000, 9999)}"

    def display_alert(self):
        print(f"-----------------------------------------")
        print(f"ALERT ID    : {self.alert_id}")
        print(f"Anomaly     : {self.anomaly_type}")
        print(f"Severity    : {self.severity}")
        print(f"Timestamp   : {self.timestamp}")
        print(f"-----------------------------------------\n")

def generate_alert():
    """
    Simulates real-time detection of an anomaly
    and generates an alert based on random selection.
    """
    print("\n[INFO] Cyber Threat Monitoring Active...\n")

    while True:
        # Simulate random wait time between anomalies
        wait_time = random.randint(3, 8)
        time.sleep(wait_time)

        # Randomly pick an anomaly and severity
        selected_anomaly = random.choice(ANOMALY_TYPES)
        selected_severity = random.choice(SEVERITY_LEVELS)

        # Generate and display the alert
        alert = Alert(selected_anomaly, selected_severity)
        alert.display_alert()

        # After generating 5 alerts, stop the simulation
        if input("Generate another alert? (yes/no): ").lower() != "yes":
            print("\n[INFO] Alert Generation Simulation Ended.\n")
            break

if __name__ == "__main__":
    generate_alert()
