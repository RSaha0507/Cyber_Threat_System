import pytest
from unittest.mock import MagicMock
from aggregator.otx_live_feed import fetch_and_store_otx_threats
from db.mongo_client import threats_collection
from detection.anomaly_detector import detect_best_anomaly_model
import pandas as pd

# 1. Test successful fetch and DB insertion
def test_fetch_and_store_inserts(mocker):
    # Mock the API response with sample IPs
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "192.168.1.1\n10.0.0.1\n"
    
    mocker.patch('aggregator.otx_live_feed.requests.get', return_value=mock_response)
    # Spy on insert_one to ensure DB insert calls
    mock_insert = mocker.patch('db.mongo_client.threats_collection.insert_one')
    
    fetch_and_store_otx_threats()
    assert mock_insert.call_count == 2  # 2 IPs inserted

# 2. Test empty API response
def test_fetch_empty_data(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = ""
    mock_insert = mocker.patch('db.mongo_client.threats_collection.insert_one')
    mocker.patch('aggregator.otx_live_feed.requests.get', return_value=mock_response)
    
    fetch_and_store_otx_threats()
    mock_insert.assert_not_called()  # No DB insert on empty data

# 3. Test anomaly detection correctness on sample data
def test_anomaly_detection_on_sample_data():
    data = {
        'category': ['unknown', 'malware', 'phishing', 'unknown'],
        'threat_level': ['high', 'medium', 'low', 'high']
    }
    df = pd.DataFrame(data)

    anomalies_df, model = detect_best_anomaly_model(df, model_choice="IForest")

    # Assert it's a DataFrame and has at least one anomaly
    assert not anomalies_df.empty
    assert 'is_anomaly' in anomalies_df.columns

# 4. Test malformed data handling
def test_malformed_data(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "not_an_ip\n1234\n"
    mocker.patch('aggregator.otx_live_feed.requests.get', return_value=mock_response)
    mock_insert = mocker.patch('db.mongo_client.threats_collection.insert_one')
    
    # Should not crash even if data malformed
    fetch_and_store_otx_threats()
    # Depending on your implementation, you can check if insert_one was called or not

# 5. Simulate network/API failure
def test_api_network_failure(mocker):
    mocker.patch('aggregator.otx_live_feed.requests.get', side_effect=Exception("Network Error"))
    # Should handle exception gracefully
    fetch_and_store_otx_threats()
