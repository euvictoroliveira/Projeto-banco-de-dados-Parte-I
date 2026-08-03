#
# Arquivo para tratamento do endpoint da página inicial (dashboard)
#


from flask import Blueprint, render_template
from routes.estatisticas import get_ranking_residentes
from sqlalchemy import func, extract
from datetime import date
from models import Paciente, Atendimento, ProcedimentoRealizado
from routes.estatisticas import get_ranking_residentes
import database

home_bp = Blueprint("home", __name__)


def contar_pacientes():
   return database.db.session.query(
       func.count(Paciente.id_pessoa)
   ).scalar()

def contar_atendimentos():
   return database.db.session.query(
       func.count(Atendimento.id_atendimento)
   ).scalar()

def contar_atendimentos_mes_atual():
   hoje = date.today()

   return database.db.session.query(
        func.count(Atendimento.id_atendimento)
    ).filter(
        extract('year', Atendimento.data_hora) == hoje.year,
        extract('month', Atendimento.data_hora) == hoje.month
    ).scalar()


def contar_procedimentos_realizados():
    return database.db.session.query(
       func.count()
    ).select_from(
       ProcedimentoRealizado
    ).filter(
       ProcedimentoRealizado.is_removido == False
    ).scalar()


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