import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
from unittest.mock import patch, Mock
from fetch_data import fetch_and_process_data


def test_fetch_and_process_data_success():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "mfrrRequest": [
            {
                "timeStamp": "2026-03-17T10:00:00",
                "mtuStart": "2026-03-17T10:00:00",
                "values": [
                    {"area": "DK1", "value": 100},
                    {"area": "DK2", "value": 200}
                ]
            }
        ]
    }

    with patch("fetch_data.requests.get", return_value=mock_response):
        result = fetch_and_process_data()

    assert len(result) == 2
    assert result[0]["area"] == "DK1"
    assert result[1]["area"] == "DK2"


def test_fetch_and_process_data_api_error():
    with patch("fetch_data.requests.get", side_effect=requests.exceptions.RequestException("API error")):
        result = fetch_and_process_data()

    assert result == []


def test_fetch_and_process_data_invalid_json():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch("fetch_data.requests.get", return_value=mock_response):
        result = fetch_and_process_data()

    assert result == []


def test_fetch_and_process_data_missing_fields():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "mfrrRequest": [
            {
                "timeStamp": "2026-03-17T10:00:00",
                "mtuStart": "2026-03-17T10:00:00",
                "values": [
                    {"area": "DK1"},
                    {"value": 200}
                ]
            }
        ]
    }

    with patch("fetch_data.requests.get", return_value=mock_response):
        result = fetch_and_process_data()

    assert result == []