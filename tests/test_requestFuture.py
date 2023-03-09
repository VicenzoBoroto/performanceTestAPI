import pytest
import asyncio
from unittest.mock import patch, Mock
from requests.exceptions import RequestException

from requestFuture import make_request, main


def test_make_request():
    url = 'https://api.cloudmersive.com'
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.headers.get.return_value = '0.123'
    session_mock = Mock()
    session_mock.get.return_value.__aenter__.return_value = response_mock
    response_time_list = []
    cpu_percentages = []
    memory_percentages = []
    error_codes = []
    asyncio.run(make_request(session_mock, url, response_time_list, cpu_percentages, memory_percentages, error_codes))
    assert len(response_time_list) == 1
    assert response_time_list[0] == 0.123


def test_make_request_error():
    url = 'https://httpstat.us/404'
    session_mock = Mock()
    session_mock.get.side_effect = RequestException
    response_time_list = []
    cpu_percentages = []
    memory_percentages = []
    error_codes = []
    asyncio.run(make_request(session_mock, url, response_time_list, cpu_percentages, memory_percentages, error_codes))
    assert len(response_time_list) == 0


@patch('requestFuture.psutil')
@patch('requestFuture.aiohttp')
def test_main(aiohttp_mock, psutil_mock):
    url = 'https://api.cloudmersive.com'
    num_requests = 10

    response_mock = Mock()
    response_mock.status = 200
    response_mock.headers.get.return_value = '0.123'
    session_mock = Mock()
    session_mock.get.return_value.__aenter__.return_value = response_mock
    aiohttp_mock.ClientSession.return_value.__aenter__.return_value = session_mock

    psutil_mock.cpu_percent.return_value = 10
    psutil_mock.virtual_memory.return_value.percent = 20

    response_times, cpu_percentages, memory_percentages, error_codes, num_errors = asyncio.run(main(num_requests, [url]))
    assert len(response_times) == num_requests
    assert all([response_time == 0.123 for response_time in response_times])
    assert len(cpu_percentages) == num_requests
    assert len(memory_percentages) == num_requests
    assert len(error_codes) == num_requests
    assert num_errors == 0


def test_main_empty_urls():
    response_times, cpu_percentages, memory_percentages, error_codes, num_errors = asyncio.run(main(10, []))
    assert len(response_times) == 0
    assert len(cpu_percentages) == 0
    assert len(memory_percentages) == 0
    assert len(error_codes) == 0
    assert num_errors == 0
