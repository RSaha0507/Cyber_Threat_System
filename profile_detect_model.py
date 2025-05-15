import cProfile
import pandas as pd
from detection.anomaly_detector import detect_best_anomaly_model  # update path as needed

# Create realistic test data
data = {
    'category': ['unknown', 'malware', 'phishing', 'ransomware', 'botnet'] * 2000,
    'threat_level': ['high', 'medium', 'low', 'high', 'low'] * 2000
}
df = pd.DataFrame(data)

# Profile the function
cProfile.run('detect_best_anomaly_model(df, model_choice="IForest")', 'profile_result.prof')
