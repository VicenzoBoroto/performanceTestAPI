import asyncio
import json
import logging
import aiohttp
import psutil
import requests
from typing import List, Tuple


# Constantes para configurar o teste
num_requests = 1000
timeout = 5
success_rate_threshold = 0.95
response_time_threshold = 2.0
urls = [
    'https://api.cloudmersive.com'
]


def make_request(session: requests.Session, url: str) -> Tuple[float, int, float, int]:
    """Realiza uma requisição HTTP POST para a URL fornecida e retorna informações da resposta.

    Args:
        session: objeto de sessão do requests
        url: URL para fazer a requisição

    Returns:
        Tupla com informações da resposta:
        - Tempo de resposta (em segundos)
        - Código de status HTTP
        - Uso de CPU (em porcentagem)
        - Uso de memória (em porcentagem)
    """
    data = {'foo': 'bar'}
    headers = {'Content-Type': 'application/json'}
    response = session.post(url, data=json.dumps(data), headers=headers, timeout=timeout)
    response_time = float(response.headers.get('x-response-time', 0))
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    status_code = response.status_code
    return response_time, status_code, cpu_percent, memory_percent


def calculate_apdex(response_times: List[float], threshold: float) -> Tuple[float, str]:
    """Calcula o valor APDEX e a classificação do teste com base nos tempos de resposta e no limiar de tempo.

    Args:
        response_times: Lista com os tempos de resposta (em segundos) de cada requisição
        threshold: Limiar de tempo (em segundos) para definir se a requisição foi satisfatória ou não

    Returns:
        Tupla com o valor APDEX e a classificação do teste
    """
    satisfactory_count = len([x for x in response_times if x <= threshold])
    apdex = (satisfactory_count + 0.5 * len([x for x in response_times if x > threshold])) / len(response_times)
    classification = 'Fail' if apdex < 0.5 else 'Satisfactory' if apdex < 0.75 else 'Good'
    return apdex, classification


async def main(num_requests: int, urls: List[str]) -> Tuple[List[float], List[int], List[float], List[int], int]:
    """Executa o teste de carga para as URLs fornecidas e retorna as informações coletadas.

    Args:
        num_requests: Número de requisições a serem feitas para cada URL
        urls:
    Returns:
        Uma tupla contendo as listas de tempo de resposta, porcentagem de uso de CPU,
        porcentagem de uso de memória, códigos de erro e o número total de erros encontrados
    """
    response_times = []
    error_codes = []
    cpu_percentages = []
    memory_percentages = []
    num_errors = 0

    async with aiohttp.ClientSession() as session:
        for url in urls:
            for i in range(num_requests):
                try:
                    response_time, cpu_percentage, memory_percentage, error_code = await make_request(session, url)
                    response_times.append(response_time)
                    cpu_percentages.append(cpu_percentage)
                    memory_percentages.append(memory_percentage)
                    error_codes.append(error_code)
                except aiohttp.ClientError:
                    response_times.append(timeout)
                    error_codes.append(408)
                    num_errors += 1

                threshold = 2.0
                apdex, classification = calculate_apdex(response_times, threshold)

                satisfactory_count = len([x for x in response_times if x <= threshold])
                success_rate = satisfactory_count / (len(urls) * num_requests)
                if success_rate < success_rate_threshold:
                    print(f'Test failed: success rate {success_rate:.2f} < threshold {success_rate_threshold:.2f}')
                else:
                    print(f'Test passed: APDEX {apdex:.2f}, success rate {success_rate:.2f}')

                print(f'Response times: {response_times}')
                print(f'CPU percentages: {cpu_percentages}')
                print(f'Memory percentages: {memory_percentages}')
                print(f'Error codes: {error_codes}')
                print(f'Number of errors: {num_errors}')

                return response_times, cpu_percentages, memory_percentages, error_codes, num_errors
