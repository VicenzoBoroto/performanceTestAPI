import concurrent.futures
import requests
import time

num_requests = 200
base_url = "https://api.cloudmersive.com"

def make_request(url):
    try:
        start_time = time.monotonic()
        response = requests.get(url)
        end_time = time.monotonic()
        response_time = end_time - start_time
        if response.status_code == 200:
            return response_time
    except requests.exceptions.RequestException:
        pass

def main():
    response_times = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        urls = [base_url for _ in range(num_requests)]
        for response_time in executor.map(make_request, urls):
            if response_time:
                response_times.append(response_time)

    if response_times:
        print(f"Peak response time: {max(response_times):.3f} seconds")
        print(f"Average response time: {sum(response_times) / len(response_times):.3f} seconds")
    else:
        print("No successful requests were made.")

if __name__ == "__main__":
    main()
