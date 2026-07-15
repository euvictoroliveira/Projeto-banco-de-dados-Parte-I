#
# Arquivo para tratamento do endpoint relacionado as estatísticas
#

from flask import Blueprint, render_template, request
from datetime import date
import database

#ranking_residentes_bp = Blueprint("ranking_residentes", __name__)
estatisticas_bp = Blueprint("Estatisticas", __name__)

#@ranking_residentes_bp.route('/ranking_residentes', methods=['POST'])
def get_ranking_residentes():
    cursor = database.conexao.cursor()

    consulta = """
        SELECT p.nome, count(*)
        FROM residente r
        INNER JOIN pessoa p ON p.id_pessoa  = r.id_profissional
        inner join atendimento a on a.id_residente = r.id_profissional
        group by p.id_pessoa, p.nome 
        order by count(*) desc
    """

    cursor.execute(consulta)
    ranking = cursor.fetchall()
    cursor.close()

    return ranking

# Preceptores que supervisionaram mais de 5 atendimentos em um determinado mês
def get_preceptores_mais_de_5_atendimentos(ano, mes):
    cursor = database.conexao.cursor()

    consulta = """
        SELECT p.nome, count(*)
        FROM preceptor pr
        INNER JOIN pessoa p ON p.id_pessoa = pr.id_profissional
        INNER JOIN atendimento a ON a.id_preceptor = pr.id_profissional
        WHERE EXTRACT(YEAR FROM a.data_hora) = %s
          AND EXTRACT(MONTH FROM a.data_hora) = %s
        GROUP BY p.id_pessoa, p.nome
        HAVING count(*) > 5
        ORDER BY count(*) DESC
    """

    cursor.execute(consulta, (ano, mes))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

# Lista de residentes cadastrados, para popular o dropdown de filtro.
def get_lista_residentes():
    cursor = database.conexao.cursor()

    consulta = """
        SELECT r.id_profissional, p.nome
        FROM residente r
        INNER JOIN pessoa p ON p.id_pessoa = r.id_profissional
        ORDER BY p.nome
    """

    cursor.execute(consulta)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

# Quantidade de plantões escalados por unidade, em um mês/ano.
# Se id_residente for informado, filtra apenas os plantões daquele residente;
# caso contrário, soma os plantões de todos os residentes.
def get_plantoes_por_unidade(ano, mes, id_residente=None):
    cursor = database.conexao.cursor()

    consulta = """
        SELECT u.nome, count(*)
        FROM escala e
        INNER JOIN unidade u ON u.id_unidade = e.id_unidade
        WHERE e.mes_plantao = %s
          AND e.ano_plantao = %s
    """
    parametros = [mes, ano]

    if id_residente:
        consulta += " AND e.id_residente = %s"
        parametros.append(id_residente)

    consulta += """
        GROUP BY u.id_unidade, u.nome
        ORDER BY u.nome
    """

    cursor.execute(consulta, tuple(parametros))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@estatisticas_bp.route('/estatisticas', methods=['GET'])
def estatisticas():

    ranking = get_ranking_residentes()

    # Mês vindo do <input type="month"> no formato "AAAA-MM".
    # Se não vier (ou vier inválido), cai no mês corrente.
    mes_selecionado = request.args.get('mes')

    try:
        ano, mes = mes_selecionado.split('-')
        ano, mes = int(ano), int(mes)
    except (AttributeError, ValueError):
        hoje = date.today()
        ano, mes = hoje.year, hoje.month

    mes_selecionado = f"{ano:04d}-{mes:02d}"

    preceptores = get_preceptores_mais_de_5_atendimentos(ano, mes)

    # Filtros próprios da seção de plantões (mês/ano + residente),
    # independentes do filtro de preceptores acima.
    mes_plantoes_raw = request.args.get('mes_plantoes')

    try:
        ano_plantoes, mes_plantoes = mes_plantoes_raw.split('-')
        ano_plantoes, mes_plantoes = int(ano_plantoes), int(mes_plantoes)
    except (AttributeError, ValueError):
        hoje = date.today()
        ano_plantoes, mes_plantoes = hoje.year, hoje.month

    mes_plantoes_selecionado = f"{ano_plantoes:04d}-{mes_plantoes:02d}"

    id_residente_raw = request.args.get('id_residente')
    id_residente_selecionado = int(id_residente_raw) if id_residente_raw and id_residente_raw.isdigit() else None

    lista_residentes = get_lista_residentes()
    plantoes_por_unidade = get_plantoes_por_unidade(ano_plantoes, mes_plantoes, id_residente_selecionado)

    return render_template(
        'estatisticas.html',
        ranking_residentes=ranking,
        preceptores_mais_de_5=preceptores,
        mes_selecionado=mes_selecionado,
        plantoes_por_unidade=plantoes_por_unidade,
        mes_plantoes_selecionado=mes_plantoes_selecionado,
        lista_residentes=lista_residentes,
        id_residente_selecionado=id_residente_selecionado
    )

# Tempo médio de duração dos atendimentos por residente
@estatisticas_bp.route("/tempo_medio_residentes", methods=["GET"])
def tempo_medio_residentes():

    cursor = database.conexao.cursor()

    consulta = """
        SELECT
            p.nome,
            ROUND(AVG(a.duracao_minutos), 2) AS tempo_medio
        FROM atendimento a
        INNER JOIN residente r
            ON r.id_profissional = a.id_residente
        INNER JOIN profissional prof
            ON prof.id_pessoa = r.id_profissional
        INNER JOIN pessoa p
            ON p.id_pessoa = prof.id_pessoa
        GROUP BY p.nome
        ORDER BY p.nome;
    """

    cursor.execute(consulta)

    residentes = cursor.fetchall()

    cursor.close()

    return render_template("tempo_medio_residentes.html", residentes=residentes)