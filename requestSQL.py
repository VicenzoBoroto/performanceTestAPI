import os
import json
import pyodbc
import time
import os
import json
import time
import getpass
from halo import Halo
from selenium import webdriver
from selenium.webdriver.common.by import By
from jinja2 import Template

class TesteSQL:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        #Instale o Driver ODBC antes de rodar a apalicação
        self.cnxn = pyodbc.connect(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}")
        self.cur = self.cnxn.cursor()
    
    def executar_consultas(self, qtd_consultas):
        tempos = []
        consulta = "SELECT * FROM INFORMATION_SCHEMA.TABLES" # Alteração: busca em todas as tabelas
        for i in range(qtd_consultas):
            inicio = time.perf_counter()
            self.cur.execute(consulta)
            resultado = self.cur.fetchall()
            fim = time.perf_counter()
            tempo_total = fim - inicio
            tempos.append(tempo_total)
        return tempos
    
    def calcular_metricas(self, tempos):
        media = sum(tempos) / len(tempos)
        mediana = sorted(tempos)[len(tempos) // 2]
        variancia = sum((t - media) ** 2 for t in tempos) / len(tempos)
        desvio_padrao = variancia ** 0.5
        return media, mediana, variancia, desvio_padrao
    #Função de avaliação da Métrica.
    def avaliar_desempenho(self, media):
        if media < 0.1:
            return "Excelente"
        elif media < 0.5:
            return "Bom"
        elif media < 1.0:
            return "Tolerável"
        else:
            return "Péssimo"
if __name__ == "__main__":
    #Altere as informações para o banco desejado "nome_servidor.database.windows.net", "nome_banco", "nome_usuario", "senha"
    server = input("Insira o nome do servidor: ")
    database = input("Insira o nome do banco de dados: ")
    username = input("Insira o nome de usuário: ")
    password = getpass.getpass("Insira a senha: ")
    while True:
        consult = input("Insira o número de consultas: ")
        try:
            consult = int(consult)
            break  # Exit the loop if the input is an integer
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
    teste = TesteSQL(server=server,
                     database=database,
                     username=username,
                     password=password)
    print("Conectado ao servidor, enviando requisições...")
    with Halo(text='Executando consultas', spinner='dots'):
        tempos = teste.executar_consultas(consult)
    media, mediana, variancia, desvio_padrao = teste.calcular_metricas(tempos)
    avaliacao = teste.avaliar_desempenho(media)

# obtendo o caminho completo para a pasta 'reports' dentro do diretório atual
model_dir = 'model'
template_file = 'templateSQL.html'
template_path = os.path.join(model_dir, template_file)

# Criando dicionário com as métricas
metrics = {
    "URL": server,
    "Database": database,
    "Consultas": consult,
    "Media": media,
    "Mediana": mediana,
    "Variancia": variancia,
    "Desvio Padrao": desvio_padrao,
    "Avaliacao": avaliacao,
    "Tempos": tempos
}
# Salvando as métricas em um arquivo JSON na pasta 'reports'
reports_dir = os.path.join('reports')
os.makedirs(reports_dir, exist_ok=True)  # cria a pasta "reports" se ela não existir
metric = os.path.join(reports_dir, 'metricsSQL.json')
with open(metric, 'w') as f:
    json.dump(metrics, f)

# Carregando o template HTML com Jinja2
with open(template_path) as f:
    template_str = f.read()
template = Template(template_str)

database = metrics["Database"]
media = metrics["Media"]
consult = metrics["Consultas"]
mediana = metrics["Mediana"]
variancia = metrics["Variancia"]
desvio_padrao = metrics["Desvio Padrao"]
tempos = metrics["Tempos"]
avaliacao = metrics["Avaliacao"]

rendered_html = template.render(
    url=metrics["URL"],
    avaliacao=avaliacao,
    consult=consult,
    database=database,
    media=media,
    mediana=mediana,
    variancia=variancia,
    desvio_padrao=desvio_padrao,
    tempos=tempos
)
# Salvando o HTML renderizado em um arquivo na pasta 'reports'
report = os.path.join('SQL_report.html')
with open(report, 'w') as f:
    f.write(rendered_html)

with Halo(text='Gerando evidências...', spinner='dots'):  
    # Configurações do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Executa o navegador em modo headless (sem interface gráfica)
    options.add_argument('--window-size=1280,1080')
    # Cria o objeto do driver do Chrome
    driver = webdriver.Chrome(options=options)
    # Carrega o arquivo HTML
    file_path = os.path.join(os.getcwd(), 'SQL_report.html')
    driver.get('file:///' + file_path)
    # Espera um pouco para o HTML renderizar completamente
    time.sleep(10)
    # Tira um screenshot da primeira tela
    element1 = driver.find_element(By.TAG_NAME, 'body') 
    element1.screenshot(os.path.join(reports_dir, 'reportSQL.png'))
    # Fecha o navegador
    driver.quit()

print("\033[94m" + 'Relatório criado com sucesso!\nObrigado por usar o RequestSQL.' + "\033[0m")