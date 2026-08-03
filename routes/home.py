#
# Arquivo para tratamento do endpoint da página inicial (dashboard)
#


from flask import Blueprint, render_template
from routes.estatisticas import get_ranking_residentes
import database

home_bp = Blueprint("home", __name__)


def contar_pacientes():
    cursor = database.conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM paciente")
    total = cursor.fetchone()[0]
    cursor.close()
    return total


def contar_atendimentos():
    cursor = database.conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM atendimento")
    total = cursor.fetchone()[0]
    cursor.close()
    return total


def contar_atendimentos_mes_atual():
    cursor = database.conexao.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM atendimento
        WHERE EXTRACT(YEAR FROM data_hora) = EXTRACT(YEAR FROM CURRENT_DATE)
          AND EXTRACT(MONTH FROM data_hora) = EXTRACT(MONTH FROM CURRENT_DATE)
    """)
    total = cursor.fetchone()[0]
    cursor.close()
    return total


def contar_procedimentos_realizados():
    cursor = database.conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM procedimento_realizado WHERE is_removido = FALSE")
    total = cursor.fetchone()[0]
    cursor.close()
    return total


@home_bp.route('/', methods=['GET'])
def home():

    total_pacientes = contar_pacientes()
    total_atendimentos = contar_atendimentos()
    atendimentos_mes = contar_atendimentos_mes_atual()
    total_procedimentos = contar_procedimentos_realizados()

    # reaproveita a mesma consulta de ranking usada em /estatisticas, pegando só o top 5
    ranking_completo = get_ranking_residentes()
    top_5 = ranking_completo[:5]

    ranking_labels = [linha[0] for linha in top_5]
    ranking_valores = [linha[1] for linha in top_5]

    return render_template(
        "index.html",
        total_pacientes=total_pacientes,
        total_atendimentos=total_atendimentos,
        atendimentos_mes=atendimentos_mes,
        total_procedimentos=total_procedimentos,
        ranking_labels=ranking_labels,
        ranking_valores=ranking_valores
    )