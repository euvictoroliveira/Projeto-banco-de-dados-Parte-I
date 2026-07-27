#
# Arquivo responsável por armazenar a lógica de conexão com o banco de dados
#

from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os

db = SQLAlchemy()

conexao = psycopg2.connect(
    dbname="projeto_hospital",
    user="postgres",
    password="",
    host="localhost"
)