from flask import Blueprint, render_template, request
from include.verify import validar_cpf
from sqlalchemy import func, and_
from sqlalchemy.orm import aliased
from models import Pessoa, Atendimento, Procedimento, ProcedimentoRealizado, Paciente
from database import db
from sqlalchemy import exists
import database

atualizar_paciente_bp = Blueprint("atualizar_paciente", __name__)
listar_pacientes_sem_alto_bp = Blueprint("listar_pacientes_sem_alto", __name__)
paciente_ultima_consulta_bp = Blueprint("paciente_ultima_consulta", __name__)

# Método para atualizar endereço ou convênio de um paciente
@atualizar_paciente_bp.route('/atualizar_paciente', methods=['GET', 'POST'])
def atualizar_paciente():

    if request.method == 'GET':
        return render_template("atualizar_paciente.html")

    mensagem_erro = None

    cpf = request.form.get("cpf")

    cep = request.form.get("cep")
    logradouro = request.form.get("logradouro")
    numero = request.form.get("numero")
    complemento = request.form.get("complemento")
    bairro = request.form.get("bairro")
    cidade = request.form.get("cidade")
    uf = request.form.get("uf")

    convenio = request.form.get("convenio")

    if not validar_cpf(cpf):
        mensagem_erro = "Erro: CPF inválido."
        return render_template("atualizar_paciente.html", feedback=mensagem_erro)

    
    try:

        pessoa = Pessoa.query.filter_by(cpf=cpf).first()

        if not pessoa:
            mensagem_erro = "Paciente não encontrado."

        else:

            paciente = Paciente.query.filter_by(
                id_pessoa=pessoa.id_pessoa
            ).first()

            alterou = False

            if cep:
                pessoa.cep = cep
                alterou = True

            if logradouro:
                pessoa.logradouro = logradouro
                alterou = True

            if numero:
                pessoa.numero = numero
                alterou = True

            if complemento:
                pessoa.complemento = complemento
                alterou = True

            if bairro:
                pessoa.bairro = bairro
                alterou = True

            if cidade:
                pessoa.cidade = cidade
                alterou = True

            if uf:
                pessoa.uf = uf
                alterou = True

            if convenio:
                paciente.numero_convenio = convenio
                alterou = True

            if alterou:
                db.session.commit()
                mensagem_erro = "Paciente atualizado com sucesso."
            else:
                mensagem_erro = "Nenhuma alteração realizada."



    except Exception as e:
            db.session.rollback()
            mensagem_erro = f"Erro na operação: {e}"

    return render_template("atualizar_paciente.html", feedback=mensagem_erro)

# Lista pacientes que nunca realizaram procedimento de risco ALTO
@listar_pacientes_sem_alto_bp.route('/pacientes_sem_alto', methods=['GET'])
def listar_pacientes_sem_alto():

   subconsulta = (
        db.session.query(ProcedimentoRealizado.id_atendimento)
        .join(
            Atendimento,
            ProcedimentoRealizado.id_atendimento == Atendimento.id_atendimento
        )
        .join(
            Procedimento,
            ProcedimentoRealizado.id_procedimento == Procedimento.id_procedimento
        )
        .filter(
            Atendimento.id_paciente == Paciente.id_pessoa,
            Procedimento.nivel_risco == "ALTO",
            ProcedimentoRealizado.is_removido.is_(False)
        )
    )
   

   pacientes = (
        db.session.query(
            Pessoa.nome,
            Pessoa.cpf
        )
        .join(
            Paciente,
            Pessoa.id_pessoa == Paciente.id_pessoa
        )
        .filter(
            ~subconsulta.exists()
        )
        .order_by(
            Pessoa.nome
        )
        .all()
    )
   
   return render_template("pacientes_sem_alto.html",pacientes=pacientes)

# Lista, para cada paciente, os dados do seu atendimento mais recente
@paciente_ultima_consulta_bp.route('/paciente_ultima_consulta', methods=['GET'])
def paciente_ultima_consulta():
    # Pessoa é usada em 3 papéis diferentes na mesma consulta, por isso 3 aliases.
    PessoaPaciente = aliased(Pessoa)
    PessoaResidente = aliased(Pessoa)
    PessoaPreceptor = aliased(Pessoa)

    # Para cada paciente que TEM atendimento, a data/hora do mais recente
    ultima_data_sq = database.db.session.query(
        Atendimento.id_paciente,
        func.max(Atendimento.data_hora).label('ultima_data_hora')
    ).group_by(
        Atendimento.id_paciente
    ).subquery()

    # para pacientes que ainda não tiveram nenhum atendimento, eu vou incluir na exibição,
    # porém estaram vazios.
    query = database.db.session.query(
        PessoaPaciente.nome.label('paciente'),
        Atendimento.data_hora,
        PessoaResidente.nome.label('residente'),
        PessoaPreceptor.nome.label('preceptor'),
        func.string_agg(Procedimento.nome, ', ').label('procedimentos')
    ).select_from(
        Paciente
    ).join(
        PessoaPaciente, PessoaPaciente.id_pessoa == Paciente.id_pessoa
    ).outerjoin(
        # LEFT JOIN: paciente sem nenhum atendimento simplesmente não bate aqui
        ultima_data_sq, ultima_data_sq.c.id_paciente == Paciente.id_pessoa
    ).outerjoin(
        # LEFT JOIN: só existe atendimento a juntar se a subquery acima encontrou algo
        Atendimento,
        and_(
            Atendimento.id_paciente == Paciente.id_pessoa,
            Atendimento.data_hora == ultima_data_sq.c.ultima_data_hora
        )
    ).outerjoin(
        # LEFT JOIN: se não há atendimento, também não há residente/preceptor
        PessoaResidente, PessoaResidente.id_pessoa == Atendimento.id_residente
    ).outerjoin(
        PessoaPreceptor, PessoaPreceptor.id_pessoa == Atendimento.id_preceptor
    ).outerjoin(
        ProcedimentoRealizado,
        and_(
            ProcedimentoRealizado.id_atendimento == Atendimento.id_atendimento,
            ProcedimentoRealizado.is_removido == False
        )
    ).outerjoin(
        Procedimento, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento
    ).group_by(
        Paciente.id_pessoa,
        PessoaPaciente.nome,
        Atendimento.id_atendimento,
        Atendimento.data_hora,
        PessoaResidente.nome,
        PessoaPreceptor.nome
    ).order_by(
        PessoaPaciente.nome
    )
    
    consultas = query.all() 
    return render_template("paciente_ultima_consulta.html", consultas=consultas)
