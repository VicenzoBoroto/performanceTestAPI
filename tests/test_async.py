import asyncio
import aiohttp
import psutil
import pytest
from updates.requestAsync import make_request, calculate_apdex, main

@pytest.mark.asyncio
async def test_make_request():
    session = aiohttp.ClientSession()
    url = 'https://httpbin.org/status/200'
    response_times = []
    cpu_percentages = []
    memory_percentages = []
    error_codes = []
    await make_request(session, url, response_times, cpu_percentages, memory_percentages, error_codes)
    assert response_times[0] > 0
    assert cpu_percentages[0] >= 0 and cpu_percentages[0] <= 100
    assert memory_percentages[0] >= 0 and memory_percentages[0] <= 100
    assert error_codes[0] == 200
    await session.close()

def test_calculate_apdex():
    request_times = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    threshold = 2.0
    apdex, classification = calculate_apdex(request_times, threshold)
    assert apdex == 0.5
    assert classification == 'Questionável'

@pytest.mark.asyncio
async def test_main():
    urls = [
        'https://httpbin.org/status/200'
    ]
    num_requests = 10
    response_times, cpu_percentages, memory_percentages, error_codes, num_errors = await main(num_requests, urls)
    assert len(response_times) == num_requests
    assert len(cpu_percentages) == num_requests
    assert len(memory_percentages) == num_requests
    assert len(error_codes) == num_requests
    assert num_errors == 0

