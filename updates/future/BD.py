import time
import random
import psycopg2

class TesteBanco:

    def __init__(self, database):
        self.conn = psycopg2.connect(database=database)
        self.cur = self.conn.cursor()

    def executar_consultas(self, num_consultas):
        tempos = []
        for i in range(num_consultas):
            consulta = "SELECT * FROM tabela WHERE id = %s" % random.randint(1, 10000)
            inicio = time.time()
            self.cur.execute(consulta)
            fim = time.time()
            tempos.append(fim - inicio)
        return tempos

    def calcular_metricas(self, tempos):
        media = sum(tempos) / len(tempos)
        mediana = sorted(tempos)[len(tempos) // 2]
        variancia = sum((t - media) ** 2 for t in tempos) / len(tempos)
        desvio_padrao = variancia ** 0.5
        return media, mediana, variancia, desvio_padrao

    def avaliar_desempenho(self, media):
        if media < 0.1:
            return "Excelente"
        elif media < 0.5:
            return "Bom"
        elif media < 1.0:
            return "Tolerável"
        else:
            return "Péssimo"

if __name__ == '__main__':
    teste = TesteBanco("nome_do_banco")
    tempos = teste.executar_consultas(100)
    media, mediana, variancia, desvio_padrao = teste.calcular_metricas(tempos)
    avaliacao = teste.avaliar_desempenho(media)
    print("Média: %.3f" % media)
    print("Mediana: %.3f" % mediana)
    print("Variância: %.3f" % variancia)
    print("Desvio Padrão: %.3f" % desvio_padrao)
    print("Avaliação: %s" % avaliacao)
