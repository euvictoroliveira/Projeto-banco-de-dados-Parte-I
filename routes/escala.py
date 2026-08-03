from flask import Blueprint, render_template
from models import Pessoa, Escala, Unidade
from sqlalchemy.orm import aliased 
from sqlalchemy import func
from models import Escala
from database import db

escala_bp = Blueprint("escala", __name__)

@escala_bp.route('/escala', methods=['GET','POST'])
def escala():

    lista_escala = listar_escalas()
    return render_template("escala.html", lista_escala=lista_escala)

def listar_escalas():
    PessoaResidente = aliased(Pessoa)
    PessoaPreceptor = aliased(Pessoa)

    consulta = db.session.query(

        Escala.id_residente,
        Escala.dia_plantao.label('dia_atual'),
        Escala.turno.label('turno_atual'),    
        PessoaResidente.nome.label('nome_residente'),
        Escala.dia_semana,
        Escala.turno,
        PessoaPreceptor.nome.label('nome_preceptor'),
        Unidade.nome.label('nome_unidade')
    ).select_from(
        Escala
    ).join(
        PessoaResidente, PessoaResidente.id_pessoa == Escala.id_residente
    ).join(
        PessoaPreceptor, PessoaPreceptor.id_pessoa == Escala.id_preceptor
    ).join(
        Unidade, Unidade.id_unidade == Escala.id_unidade 
    ).order_by(
        Escala.ano_plantao.desc(), Escala.mes_plantao.desc(), Escala.dia_plantao.desc()
    )

    return consulta.all()


def atualizar_escala():
    
    id_residente = request.form.get('id_residente')
    dia_atual = request.form.get('dia_atual')
    turno_atual = request.form.get('turno_atual')
    dia_novo = request.form.get('dia_novo')
    turno_novo = request.form.get('turno_novo')


    if not (id_residente and dia_atual and turno_atual and dia_novo and turno_novo):
        return "Erro: Todos os campos são obrigatórios para reajustar a escala."

    try:

        comando_sql = text("""
            CALL sp_reajustar_escala(
                :p_id_res,
                :p_dia_atual,
                :p_turno_atual,
                :p_dia_novo,
                :p_turno_novo
            )
        """)

        parametros = {
            'p_id_res': int(id_residente),
            'p_dia_atual': dia_atual,
            'p_turno_atual': turno_atual,
            'p_dia_novo': dia_novo,
            'p_turno_novo': turno_novo
        }


        db.session.execute(comando_sql, parametros)
        db.session.commit()
        
        return "Escala reajustada com sucesso!"

    except Exception as e:

        db.session.rollback()
        return f"Erro na operação: {e}"