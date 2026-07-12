#
# Arquivo responsável por armazenar a lógica de conexão com o banco de dados
#
import os
import psycopg2

os.environ['PGCLIENTECODING'] = 'UTF-8'
os.environ['LC_MESSAGES'] = 'English'

conexao = psycopg2.connect(
    dbname="projeto_hospital",
    user="postgres",
    password="",
    host="localhost"
)