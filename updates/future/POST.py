import requests
import numpy as np
import psutil
import json

url = 'http://localhost:8000/api/endpoint'
num_requests = 1000
timeout = 5
success_rate_threshold = 0.95


def make_request(session, url, response_times, cpu_percentages, memory_percentages, error_codes):
    data = {'foo': 'bar'}
    headers = {'Content-Type': 'application/json'}
    response = session.post(url, data=json.dumps(data), headers=headers)
    response_time = response.headers.get('x-response-time', 0)
    response_times.append(float(response_time))
    cpu_percentages.append(psutil.cpu_percent())
    memory_percentages.append(psutil.virtual_memory().percent)
    error_codes.append(response.status_code)


response_times = []
error_codes = []
cpu_percentages = []
memory_percentages = []

with requests.Session() as session:
    for i in range(num_requests):
        try:
            make_request(session, url, response_times, cpu_percentages, memory_percentages, error_codes)
        except requests.exceptions.Timeout:
            response_times.append(timeout)
            error_codes.append(408)

threshold = 2.0
apdex, classification = calculate_apdex(response_times, threshold)

satisfactory_count = len([x for x in response_times if x <= threshold])
success_rate = satisfactory_count / num_requests
if success_rate < success_rate_threshold:
    print(f'Test failed: success rate {success_rate:.2f} < threshold {success_rate_threshold:.2f}')
else:
    print(f'Test passed: APDEX {apdex:.2f}, success rate {success_rate:.2f}')

print(f'Response times: {response_times}')
print(f'CPU percentages: {cpu_percentages}')
print(f'Memory percentages: {memory_percentages}')
print(f'Error codes: {error_codes}')
print(f'Number of errors: {len([x for x in error_codes if x != 200])}')

if __name__ == '__main__':
    urls = [
        'https://api.cloudmersive.com'
    ]
    num_requests = 10

    loop = asyncio.get_event_loop()
    response_times, cpu_percentages, memory_percentages, error_codes, num_errors = loop.run_until_complete(main(num_requests, urls))

    request_times = response_times
    threshold = 2.0
    apdex, classification = calculate_apdex(request_times, threshold)
    print(f'URL: {urls}')
    print(f'Apdex: {apdex:.2f} - Classificação: {classification}')
    print(f'Response times: {response_times}')
    print(f'CPU percentages: {cpu_percentages}')
    print(f'Memory percentages: {memory_percentages}')
    print(f'Error codes: {error_codes}')
    print(f'Number of errors: {num_errors}')