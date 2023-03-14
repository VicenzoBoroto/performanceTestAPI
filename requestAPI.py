import os
import json
import psutil
import requests
import statistics
import time
import numpy as np
import matplotlib.pyplot as plt
from halo import Halo
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from jinja2 import Template
from urllib.parse import urlparse

# Recebe a URL digitada pelo usuário
url = input("Digite a URL da API: ")
# Analisa a URL
parsed_url = urlparse(url)
# Verifica se o esquema é http e substitui por https
if parsed_url.scheme == 'http':
    new_url = 'https://' + parsed_url.netloc + parsed_url.path
else:
    new_url = url
# Verifica se a URL começa com https:// e adiciona se não começar
if not new_url.startswith('https://'):
    new_url = 'https://' + new_url
# Converte a quantidade de solicitações para um número inteiro
while True:
    num_requests = input("Digite a quantidade de solicitações: ")
    if not num_requests.isdigit():
        print("Por favor, digite um número inteiro válido.")
        continue
    num_requests = int(num_requests)
    if num_requests <= 0:
        print("Por favor, digite um número inteiro maior que zero.")
        continue
    break

response_times = []
cpu_percentages = []
memory_percentages = []
error_count = 0
error_codes = []

start_time = time.time()
for i in tqdm(range(num_requests)):
    response = requests.get(new_url)
    response_time = response.elapsed.total_seconds()
    response_times.append(response_time)
    cpu_percentages.append(psutil.cpu_percent())
    memory_percentages.append(psutil.virtual_memory().percent)
    if response.status_code != 200:
        error_count += 1
        error_codes.append(response.status_code)
        print(" \033[91mErro na solicitação {}: status code {}\033[0m".format(i+1, response.status_code))
    # Verifica se o código 200 está presente na lista de erros
    if 200 not in error_codes:
        error_codes.append(200)
end_time = time.time()

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

total_time = end_time - start_time
mean_response_time = np.mean(response_times)
peak_response_time = max(response_times)
p90_response_time = np.percentile(response_times, 90)
requests_per_second = num_requests / total_time
error_rate = error_count / num_requests
average_latency = mean_response_time - (total_time / num_requests)
average_cpu_usage = np.mean(cpu_percentages)
average_memory_usage = np.mean(memory_percentages)
average_recovery_time = (end_time - start_time) / num_requests


request_times = response_times
threshold = 2.0
apdex, classification = calculate_apdex(request_times, threshold)

# Calcula a média de tempo de cada chamada
average_times = [statistics.mean(response_times[:i+1]) for i in range(len(response_times))]
# obtendo o caminho completo para a pasta 'reports' dentro do diretório atual
model_dir = 'model'
template_file = 'templateAPI.html'
template_path = os.path.join(model_dir, template_file)

# Criando dicionário com as métricas
metrics = {
    "URL": new_url,
    "APDEX": apdex,
    "Classification": classification,
    "total_requests": num_requests,
    "total_time": total_time,
    "mean_response_time": mean_response_time,
    "peak_response_time": peak_response_time,
    "p90_response_time": p90_response_time,
    "requests_per_second": requests_per_second,
    "error_rate": error_rate,
    "average_latency": average_latency,
    "average_cpu_usage": average_cpu_usage,
    "average_memory_usage": average_memory_usage,
    "average_recovery_time": average_recovery_time,
    "average_times": average_times,
    "error_count": error_count,
    "error_codes": error_codes,
}

# Salvando as métricas em um arquivo JSON na pasta 'reports'
reports_dir = os.path.join('reports')
os.makedirs(reports_dir, exist_ok=True)  # cria a pasta "reports" se ela não existir
metric = os.path.join(reports_dir, 'metricsAPI.json')
with open(metric, 'w') as f:
    json.dump(metrics, f)

# Preparando os dados para o gráfico de linhas
x = np.arange(len(metrics["average_times"]))
y = metrics["average_times"]
# Criando o gráfico de linhas
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('Requisições')
ax.set_ylabel('Tempo')
ax.set_title('Tempo x Requisição')

# Salvando o gráfico em um arquivo PNG na pasta 'reports'
filename = os.path.join(reports_dir, 'graphic.svg')
fig.savefig(filename, format="svg")

# Carregando o template HTML com Jinja2
with open(template_path) as f:
    template_str = f.read()
template = Template(template_str)

total_time = round(metrics["total_time"], 5)
total_requests = metrics["total_requests"]
classification = metrics["Classification"]
apdex = metrics["APDEX"]
mean_response_time = round(metrics["mean_response_time"], 5)
peak_response_time = round(metrics["peak_response_time"], 5)
p90_response_time = round(metrics["p90_response_time"], 5)
requests_per_second = round(metrics["requests_per_second"], 5)
error_rate = round(metrics["error_rate"], 5)
average_latency = round(metrics["average_latency"], 5)
average_cpu_usage = round(metrics["average_cpu_usage"], 5)
average_memory_usage = round(metrics["average_memory_usage"], 5)
average_recovery_time = round(metrics["average_recovery_time"], 5)
error_count = metrics["error_count"]
error_codes = metrics["error_codes"]
error_codes = list(set(error_codes))
error_info = "{}".format(", ".join(str(code) for code in error_codes))

rendered_html = template.render(
    url=metrics["URL"],
    apdex=apdex,
    classification=classification,
    total_time=total_time,
    total_requests=total_requests,
    mean_response_time=mean_response_time,
    peak_response_time=peak_response_time,
    p90_response_time=p90_response_time,
    requests_per_second=requests_per_second,
    error_rate=error_rate,
    average_latency=average_latency,
    average_cpu_usage=average_cpu_usage,
    average_memory_usage=average_memory_usage,
    average_recovery_time=average_recovery_time,
    error_info=error_info,
    error_codes=error_codes
)

# Salvando o HTML renderizado em um arquivo na pasta 'reports'
report = os.path.join('API_report.html')
with open(report, 'w') as f:
    f.write(rendered_html)

with Halo(text='Gerando evidências...', spinner='dots'):  
    # Configurações do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Executa o navegador em modo headless (sem interface gráfica)
    # options.add_argument('--start-maximized')
    options.add_argument('--window-size=1280,1080')

    # Cria o objeto do driver do Chrome
    driver = webdriver.Chrome(options=options)

    # Carrega o arquivo HTML
    file_path = os.path.join(os.getcwd(), 'API_report.html')
    driver.get('file:///' + file_path)

    # Espera um pouco para o HTML renderizar completamente
    time.sleep(10)

    # Tira um screenshot da primeira tela
    element1 = driver.find_element(By.ID, 'report-btn')
    element1.click()
    time.sleep(10)
    element1 = driver.find_element(By.TAG_NAME, 'body') 
    element1.screenshot(os.path.join(reports_dir, 'reportAPI.png'))

    # Tira um screenshot da segunda tela
    element2 = driver.find_element(By.ID, 'graph-btn')
    element2.click()
    time.sleep(10)
    element2 = driver.find_element(By.TAG_NAME, 'body')
    element2.screenshot(os.path.join(reports_dir, 'graphicAPI.png'))

    # Fecha o navegador
    driver.quit()
print("\033[94m" + 'Relatório criado com sucesso!\nObrigado por usar o RequestAPI.' + "\033[0m")