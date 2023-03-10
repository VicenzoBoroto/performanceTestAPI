import pyodbc
import time
import halo

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
    teste = TesteSQL(server='nome_servidor.database.windows.net',
                     database='nome_banco',
                     username='nome_usuario',
                     password='senha')
    print("Conectado ao servidor, enviando requisições...")
    with halo.Halo(text='Executando consultas', spinner='dots'):
        tempos = teste.executar_consultas(100)
    # tempos = teste.executar_consultas(100) #altere o valor para a quantidade de consultas desejadas
    print(f"Média de tempo de consulta: {sum(tempos)/len(tempos):.6f} segundos")
    media, mediana, variancia, desvio_padrao = teste.calcular_metricas(tempos)
    avaliacao = teste.avaliar_desempenho(media)
    print("Total de consultas realizadas:", len(tempos))
    print("Média: %.3f" % media)
    print("Mediana: %.3f" % mediana)
    print("Variância: %.3f" % variancia)
    print("Desvio Padrão: %.3f" % desvio_padrao)
    print("Avaliação: %s" % avaliacao)
    print("Consultas individuais (segundos): %s" % tempos)