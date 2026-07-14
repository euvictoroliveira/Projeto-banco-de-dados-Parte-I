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

    return render_template(
        'estatisticas.html',
        ranking_residentes=ranking,
        preceptores_mais_de_5=preceptores,
        mes_selecionado=mes_selecionado
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