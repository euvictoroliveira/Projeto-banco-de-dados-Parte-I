#
# Arquivo responsável por armazenar a lógica de conexão com o banco de dados
#

import psycopg2

conexao = psycopg2.connect(
    dbname="projeto_hospital",
    user="postgres",
    password="",
    host="localhost"
)