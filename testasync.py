import asyncio
import aiohttp
import psutil


async def make_request(session, url, response_times, cpu_percentages, memory_percentages, error_codes):
    async with session.get(url) as response:
        response_time = response.headers.get('x-response-time', 0)
        response_times.append(float(response_time))
        cpu_percentages.append(psutil.cpu_percent())
        memory_percentages.append(psutil.virtual_memory().percent)
        error_codes.append(response.status)


async def main(num_requests, urls):
    response_times = []
    cpu_percentages = []
    memory_percentages = []
    error_codes = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_requests):
            if i >= len(urls):  # check that urls list has enough items
                break
            task = asyncio.create_task(make_request(session, urls[i], response_times, cpu_percentages, memory_percentages, error_codes))
            tasks.append(task)

        await asyncio.gather(*tasks)

    num_errors = len([x for x in error_codes if x != 200])
    return response_times, cpu_percentages, memory_percentages, error_codes, num_errors


if __name__ == '__main__':
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/3',
        'https://httpbin.org/delay/4',
        'https://httpbin.org/delay/5'
    ]
    num_requests = 10

    loop = asyncio.get_event_loop()
    response_times, cpu_percentages, memory_percentages, error_codes, num_errors = loop.run_until_complete(main(num_requests, urls))

    print(f'Response times: {response_times}')
    print(f'CPU percentages: {cpu_percentages}')
    print(f'Memory percentages: {memory_percentages}')
    print(f'Error codes: {error_codes}')
    print(f'Number of errors: {num_errors}')
