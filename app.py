import psycopg2

# 1. Conectar ao banco de dados
conexao = psycopg2.connect(
    dbname="projeto_hospital",
    user="postgres",
    password="",
    host="localhost"
)
cursor = conexao.cursor()

# 2. Escrever a consulta em SQL Puro
# Exemplo do projeto: Listar todos os atendimentos de um paciente específico
consulta_sql = """
    SELECT * FROM atendimento;
"""
id_do_paciente = (1,) # Tupla com o ID que você quer buscar

# 3. Executar e buscar os resultados
cursor.execute(consulta_sql, id_do_paciente)
atendimentos = cursor.fetchall()

# 4. Mostrar os resultados no terminal
for atendimento in atendimentos:
    print(f"Data: {atendimento[0]}, Duração: {atendimento[1]} min")

# 5. Fechar a conexão
cursor.close()
conexao.close()