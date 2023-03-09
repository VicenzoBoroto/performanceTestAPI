import requests
import os
import json
import numpy as np
import pytest
from urllib.parse import urlparse
from requestAPI import main

@pytest.fixture
def url():
    return "http://api.cloudmersive.com"

@pytest.fixture
def https_url():
    return "https://api.cloudmersive.com"

def test_convert_http_to_https(url, https_url):
    parsed_url = urlparse(url)
    assert main.convert_to_https(url) == https_url
    assert main.convert_to_https(https_url) == https_url

def test_add_https_to_url(url, https_url):
    assert main.add_https(url) == https_url
    assert main.add_https(https_url) == https_url

def test_convert_num_requests():
    assert main.convert_num_requests("10") == 10
    assert main.convert_num_requests("0") == None
    assert main.convert_num_requests("-5") == None
    assert main.convert_num_requests("abc") == None

def test_calculate_metrics():
    metrics = main.calculate_metrics("https://api.cloudmersive.com", 1)
    assert isinstance(metrics, dict)
    assert set(metrics.keys()) == {'URL', 'total_requests', 'total_time', 'mean_response_time',
                                    'peak_response_time', 'p90_response_time', 'requests_per_second',
                                    'error_rate', 'average_latency', 'average_cpu_usage',
                                    'average_memory_usage', 'average_recovery_time', 'average_times',
                                    'error_count', 'error_codes'}

def test_create_json_file():
    metrics = {
        "URL": "https://api.cloudmersive.com",
        "total_requests": 1,
        "total_time": 1.0,
        "mean_response_time": 1.0,
        "peak_response_time": 1.0,
        "p90_response_time": 1.0,
        "requests_per_second": 1.0,
        "error_rate": 0.0,
        "average_latency": 1.0,
        "average_cpu_usage": 1.0,
        "average_memory_usage": 1.0,
        "average_recovery_time": 1.0,
        "average_times": [1.0],
        "error_count": 0,
        "error_codes": []
    }
    main.create_json_file(metrics)
    assert os.path.isfile('reports/metrics.json')
    with open('reports/metrics.json') as f:
        assert json.load(f) == metrics

def test_create_line_graph():
    metrics = {
        "average_times": np.array([1.0, 2.0, 3.0]),
    }
    main.create_line_graph(metrics, 'reports/graphic.svg')
    assert os.path.isfile('reports/graphic.svg')
