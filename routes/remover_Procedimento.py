from flask import Blueprint, render_template, request
from database import db
from models import Atendimento, Procedimento, ProcedimentoRealizado, Pessoa

remover_procedimento_bp = Blueprint("remover_procedimento", __name__)

@remover_procedimento_bp.route('/remover_procedimento', methods=['GET', 'POST'])
def remover_procedimento():
    feedback = None
    dados_atendimento = None
    lista_procedimentos = []
    
    # Capturando usando a nomenclatura do HTML
    id_atendimento = request.args.get('id_atendimento') or request.form.get('id_atendimento')
    id_procedimento = request.form.get('id_procedimento')

    try:

        if request.method == 'POST' and id_procedimento and id_atendimento:
            procedimento = ProcedimentoRealizado.query.filter_by(
                id_atendimento=id_atendimento,
                id_procedimento=id_procedimento,
                is_removido=False
            ).first()

            if not procedimento:
                feedback = "Erro: Procedimento não encontrado neste atendimento."

            elif procedimento.is_faturado:
                feedback = "Erro: Este procedimento já foi faturado e não pode ser removido."

            else:
                procedimento.is_removido = True
                db.session.commit()
                feedback = "Procedimento removido com sucesso!"

        # SE TEMOS UM ATENDIMENTO SENDO CONSULTADO/REMOVIDO
        if id_atendimento:
            
            paciente = Pessoa.__table__.alias("paciente")
            residente = Pessoa.__table__.alias("residente")
            preceptor = Pessoa.__table__.alias("preceptor")

            dados_atendimento = (
                db.session.query(
                    Atendimento.id_atendimento,
                    paciente.c.nome,
                    preceptor.c.nome,
                    residente.c.nome
                )
                .join(
                    paciente,
                    Atendimento.id_paciente == paciente.c.id_pessoa
                )
                .join(
                    preceptor,
                    Atendimento.id_preceptor == preceptor.c.id_pessoa
                )
                .join(
                    residente,
                    Atendimento.id_residente == residente.c.id_pessoa
                )
                .filter(
                    Atendimento.id_atendimento == id_atendimento
                )
                .first()
            )

            if dados_atendimento:
                # Busca os procedimentos vinculados na tabela "procedimento_realizado"
                lista_procedimentos = (
                    db.session.query(
                        Procedimento.id_procedimento,
                        Procedimento.nome,
                        ProcedimentoRealizado.quantidade,
                        ProcedimentoRealizado.tempo_real_minutos,
                        ProcedimentoRealizado.observacao,
                        ProcedimentoRealizado.is_faturado
                    )
                    .join(
                        ProcedimentoRealizado,
                        Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento
                    )
                    .filter(
                        ProcedimentoRealizado.id_atendimento == id_atendimento,
                        ProcedimentoRealizado.is_removido == False
                    )
                    .all()
                )

            else:
                feedback = "Erro: Atendimento não encontrado."

    except Exception as e:
        db.session.rollback()
        feedback = f"Erro na operação: {e}"
   
    # Retorna o HTML passando as variáveis padronizadas
    return render_template(
        "remover_procedimento.html", 
        dados_atendimento=dados_atendimento, 
        lista_procedimentos=lista_procedimentos, 
        feedback=feedback,
        id_atendimento_buscado=id_atendimento
    )