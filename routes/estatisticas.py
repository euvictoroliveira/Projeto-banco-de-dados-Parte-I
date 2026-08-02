#
# Arquivo para tratamento do endpoint relacionado as estatísticas
#

from flask import Blueprint, render_template, request
from datetime import date
from sqlalchemy import select, func, extract, and_, case, cast, Numeric
from sqlalchemy.orm import Session
from models import Residente, Pessoa, Atendimento, Preceptor, Unidade, Escala, Procedimento, ProcedimentoRealizado
import database

#ranking_residentes_bp = Blueprint("ranking_residentes", __name__)
estatisticas_bp = Blueprint("Estatisticas", __name__)

def get_ranking_residentes():

    query = database.db.session.query(
        Pessoa.nome, 
        func.count(Atendimento.id_atendimento)   
    ).join(
        Residente, Residente.id_profissional == Pessoa.id_pessoa
    ).outerjoin(
        Atendimento, Atendimento.id_residente == Residente.id_profissional
    ).group_by(
        Pessoa.id_pessoa, Pessoa.nome
    ).order_by(
        func.count(Atendimento.id_atendimento).desc())       

    ranking = query.all()

    return ranking

# Preceptores que supervisionaram mais de 5 atendimentos em um determinado mês
def get_preceptores_mais_de_5_atendimentos(ano, mes):
    query = database.db.session.query(
        Pessoa.nome,
        func.count(Atendimento.id_atendimento)
    ).select_from(Preceptor).join(
        Pessoa, Pessoa.id_pessoa == Preceptor.id_profissional
    ).outerjoin(
        Atendimento, Atendimento.id_preceptor == Preceptor.id_profissional
    ).filter(
        extract('year', Atendimento.data_hora) == ano,
        extract('month', Atendimento.data_hora) == mes
    ).group_by(
        Pessoa.id_pessoa, Pessoa.nome
    ).having(
        func.count(Atendimento.id_atendimento) > 5
    ).order_by(
        func.count(Atendimento.id_atendimento).desc()
    )

    return query.all()

# Lista de residentes cadastrados, para popular o dropdown de filtro.
def get_lista_residentes():
    query = database.db.session.query(
        Residente.id_profissional, 
        Pessoa.nome
    ).join(
        Pessoa, Pessoa.id_pessoa == Residente.id_profissional
    ).order_by(
        Pessoa.nome
    )
    
    return query.all()

# Quantidade de plantões escalados por unidade, em um mês/ano.
# Se id_residente for informado, filtra apenas os plantões daquele residente;
# caso contrário, soma os plantões de todos os residentes.
def get_plantoes_por_unidade(ano, mes, id_residente=None):
    # Cria uma lista base de condições para o LEFT JOIN (outerjoin)
    condicoes_join = [
        Unidade.id_unidade == Escala.id_unidade,
        Escala.mes_plantao == mes,
        Escala.ano_plantao == ano
    ]

    # Adiciona a condição do residente, se ele foi selecionado
    if id_residente:
        condicoes_join.append(Escala.id_residente == id_residente)

    query = database.db.session.query(
        Unidade.nome, 
        func.count(Escala.id_escala)
    ).outerjoin(
        # Aplica todas as condições do JOIN juntas
        Escala, and_(*condicoes_join) 
    ).group_by(
        Unidade.id_unidade, Unidade.nome
    ).order_by(
        Unidade.nome
    )
    
    return query.all()

# percentual de procedimentos de alto risco realizados por cada residente
def get_percentual_alto_risco_por_residente():
    # Total de procedimentos realizados pelo residente
    # se o residente não tem nenhum procedimento, vira 0
    total_procedimentos = func.coalesce(
        func.sum(ProcedimentoRealizado.quantidade), 0
    )

    # Total de procedimentos de risco alto
    procedimentos_alto_risco = func.coalesce(
        func.sum(
            case(
                (Procedimento.nivel_risco == 'ALTO', ProcedimentoRealizado.quantidade),
                else_=0
            )
        ), 0
    )

    # NULLIF evita divisão por zero.
    # COALESCE por fora transforma o resultado nulo (quando o residente não tem nenhum
    # procedimento) em 0%, em vez de deixar como "sem dado".
    percentual_alto_risco = func.coalesce(
        func.round(
            cast(procedimentos_alto_risco, Numeric) * 100 /
            cast(func.nullif(total_procedimentos, 0), Numeric),
            2
        ), 0
    )

    query = database.db.session.query(
        Pessoa.nome,
        total_procedimentos.label('total_procedimentos'),
        percentual_alto_risco.label('percentual_alto_risco')
    ).select_from(Residente).outerjoin(
        Atendimento, Atendimento.id_residente == Residente.id_profissional
    ).outerjoin(
        ProcedimentoRealizado,
        and_(
            ProcedimentoRealizado.id_atendimento == Atendimento.id_atendimento,
            ProcedimentoRealizado.is_removido == False
        )
    ).outerjoin(
        Procedimento, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento
    ).outerjoin(
        Pessoa, Pessoa.id_pessoa == Residente.id_profissional
    ).group_by(
        Pessoa.id_pessoa, Pessoa.nome
    ).order_by(
        Pessoa.nome
    )

    return query.all()

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
    percentual_alto_risco = get_percentual_alto_risco_por_residente()

    return render_template(
        'estatisticas.html',
        ranking_residentes=ranking,
        preceptores_mais_de_5=preceptores,
        mes_selecionado=mes_selecionado,
        plantoes_por_unidade=plantoes_por_unidade,
        mes_plantoes_selecionado=mes_plantoes_selecionado,
        lista_residentes=lista_residentes,
        id_residente_selecionado=id_residente_selecionado,
        percentual_alto_risco=percentual_alto_risco
    )

# Tempo médio de duração dos atendimentos por residente
@estatisticas_bp.route("/tempo_medio_residentes", methods=["GET"])
def tempo_medio_residentes():

    query = database.db.session.query(
        Pessoa.nome,
        func.coalesce(func.round(func.avg(Atendimento.duracao_minutos), 2), 0).label('tempo_medio')
    ).select_from(Residente).outerjoin(
        Atendimento, Atendimento.id_residente == Residente.id_profissional
    ).outerjoin(
        Pessoa, Pessoa.id_pessoa == Residente.id_profissional
    ).group_by(
        Pessoa.id_pessoa, Pessoa.nome
    ).order_by(
        Pessoa.nome
    )

    residentes = query.all()

    return render_template("tempo_medio_residentes.html", residentes=residentes)