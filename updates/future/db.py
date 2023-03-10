import sqlite3

# Criar conexão com o banco de dados
conn = sqlite3.connect('dbTeste.db')

# Criar cursor para executar comandos SQL
cursor = conn.cursor()

# Criar tabela dbTeste com as colunas especificadas
cursor.execute('''
CREATE TABLE dbTeste (
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
    [Valor de Venda] REAL,
    [Valor de Compra] REAL,
    [Unidade de Medida] TEXT,
    [Bandeira] TEXT
);
''')

# Salvar as alterações e fechar a conexão com o banco de dados
conn.commit()
conn.close()
