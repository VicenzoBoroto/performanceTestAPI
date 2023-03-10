import sqlite3
import pandas as pd

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('dbTeste.db')
cursor = conn.cursor()

# Cria a tabela com as colunas necessárias
cursor.execute('''CREATE TABLE IF NOT EXISTS dbTeste (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                [Regiao - Sigla] TEXT,
                [Estado - Sigla] TEXT,
                [Municipio] TEXT,
                [Revenda] TEXT,
                [CNPJ da Revenda] TEXT,
                [Nome da Rua] TEXT,
                [Numero Rua] TEXT,
                [Complemento] TEXT,
                [Bairro] TEXT,
                [Cep] TEXT,
                [Produto] TEXT,
                [Data da Coleta] TEXT,
                [Valor de Venda] TEXT,
                [Valor de Compra] TEXT,
                [Unidade de Medida] TEXT,
                [Bandeira] TEXT)''')

# Lê o arquivo Excel e importa para a tabela SQLite
df = pd.read_excel('db_teste.xlsx')

for i, row in df.iterrows():
    # Monta a query de inserção
    query = f"INSERT INTO dbTeste ([Regiao - Sigla], [Estado - Sigla], [Municipio], [Revenda], [CNPJ da Revenda], [Nome da Rua], [Numero Rua], [Complemento], [Bairro], [Cep], [Produto], [Data da Coleta], [Valor de Venda], [Valor de Compra], [Unidade de Medida], [Bandeira]) \
             VALUES ('{row['Regiao - Sigla']}', '{row['Estado - Sigla']}', '{row['Municipio']}', '{row['Revenda']}', '{row['CNPJ da Revenda']}', '{row['Nome da Rua']}', '{row['Numero Rua']}', '{row['Complemento']}', '{row['Bairro']}', '{row['Cep']}', '{row['Produto']}', '{row['Data da Coleta']}', '{row['Valor de Venda']}', '{row['Valor de Compra']}', '{row['Unidade de Medida']}', '{row['Bandeira']}')"
    
    # Executa a query de inserção e commita a transação
    cursor.execute(query)
    conn.commit()

# Fecha a conexão com o banco de dados
conn.close()
