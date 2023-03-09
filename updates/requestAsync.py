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


def calculate_apdex(request_times, threshold, base_threshold=5):
    num_requests = len(request_times)
    satisfactory_count = 0
    tolerable_count = 0
    for time in request_times:
        if time <= threshold:
            satisfactory_count += 1
        elif time <= 4*threshold:
            tolerable_count += 1
    frustrated_count = num_requests - satisfactory_count - tolerable_count
    apdex = (satisfactory_count + tolerable_count/2) / num_requests
    if apdex >= 0.95:
        classification = 'Excelente'
    elif apdex >= 0.85:
        classification = 'Boa'
    elif apdex >= 0.70:
        classification = 'Razoável'
    elif apdex >= 0.50:
        classification = 'Questionável'
    else:
        classification = 'Não aceitável'
    return apdex, classification


if __name__ == '__main__':
    urls = input("Digite a URL da API: ")
    num_requests = int(input("Digite a quantidade de Requisições: "))
    threshold = float(input("Digite o tempo em segundos do Threshold [Por padrão digite 2]: ") or "2")
    loop = asyncio.get_event_loop()
    response_times, cpu_percentages, memory_percentages, error_codes, num_errors = loop.run_until_complete(main(num_requests, urls.split()))

    request_times = response_times

    apdex, classification = calculate_apdex(request_times, threshold)
    print(f'URL: {urls}')
    print(f'Apdex: {apdex:.2f} - Classificação: {classification}')
    print(f'Response times: {response_times}')
    print(f'CPU percentages: {cpu_percentages}')
    print(f'Memory percentages: {memory_percentages}')
    print(f'Error codes: {error_codes}')
    print(f'Number of errors: {num_errors}')
    
    # esperando todas as tarefas do asyncio serem concluídas antes de fechar o loop de eventos
    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
