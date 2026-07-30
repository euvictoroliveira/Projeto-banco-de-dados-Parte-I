#
# Arquivo para tratamento do endpoint relacionado aos atendimentos
#

from flask import Blueprint, render_template, request
from include.verify import validar_cpf, validar_crm
from sqlalchemy import select
from sqlalchemy.orm import aliased
from models import *
import database
import time

listar_atendimentos_bp = Blueprint("listar_atendimentos", __name__)
novo_atendimento_bp = Blueprint("novo_atendimento", __name__)
listar_procedimentos_bp = Blueprint("listar_procedimentos", __name__)


#
# Método para listar todos os atendimentos de um paciente
#
@listar_atendimentos_bp.route('/listar_atendimentos', methods=['GET'])
def listar_atendimento():

    if request.method == 'GET':

        # Variáveis
        atendimentos = []
        mensagem_erro = None

        # Recebe o atributo cpf enviado pela requisição
        paciente_cpf = request.args.get('cpf')

        # Verifica se o atributo existe
        if not paciente_cpf:
            return render_template("listar_atendimento.html")

        # Realiza a validação do cpf
        if not validar_cpf(paciente_cpf):
            mensagem_erro = "Erro: CPF inválido"
            return render_template("listar_atendimento.html", feedback=mensagem_erro)
        
        # Cria apelidos para as tabelas
        PessoaPaciente = aliased(Pessoa)
        PessoaPreceptor = aliased(Pessoa)
        PessoaResidente = aliased(Pessoa)

        # Monta a pesquisa
        query = database.db.session.query(
            Atendimento.id_atendimento,
            Atendimento.data_hora,
            Atendimento.duracao_minutos,
            PessoaPaciente.nome.label('nome_paciente'),
            PessoaPreceptor.nome.label('nome_preceptor'),
            PessoaResidente.nome.label('nome_residente')
        ).join(
            PessoaPaciente, Atendimento.id_paciente == PessoaPaciente.id_pessoa
        ).join(
            PessoaPreceptor, Atendimento.id_preceptor == PessoaPreceptor.id_pessoa
        ).join(
            PessoaResidente, Atendimento.id_residente == PessoaResidente.id_pessoa
        ).filter(
            PessoaPaciente.cpf == paciente_cpf
        ).order_by(
            Atendimento.data_hora.desc()
        )


        atendimentos = query.all()

        return render_template("listar_atendimento.html", lista_atendimentos=atendimentos, feedback=mensagem_erro)


#
# Método para buscar as unidades e popular o dropdown
#
def get_lista_unidade():
    cursor = database.conexao.cursor()

    consulta = """
        select u.id_unidade, u.nome
        from unidade u
    """

    cursor.execute(consulta)
    resultado = cursor.fetchall()

    return resultado

#
# Método para criar um novo atendimento
#
@novo_atendimento_bp.route('/novo_atendimento', methods=['GET','POST'])
def novo_atendimento():
    
    lista_unidades = get_lista_unidade()
    mensagem_erro = None

    if request.method == 'GET':

        return render_template("novo_atendimento.html", unidades=lista_unidades)

    else:
        paciente_cpf = request.form.get('cpf')
        preceptor_crm = request.form.get('preceptor')
        residente_crm = request.form.get('residente')
        duracao = request.form.get('duracao')
        data_hora = time.strftime('%Y-%m-%d %H:%M:%S')
        id_unidade = request.form.get('id_unidade')

        # Realiza a validação do cpf
        if not validar_cpf(paciente_cpf):
            mensagem_erro = "Erro: CPF inválido"
            return render_template("novo_atendimento.html", feedback=mensagem_erro)

        # Validação do crm do preceptor
        if not validar_crm(preceptor_crm):
            mensagem_erro = "Erro: CRM preceptor inválido"
            return render_template("novo_atendimento.html", feedback=mensagem_erro)

        # Validação do crm do residente
        if not validar_crm(residente_crm):
            mensagem_erro = "Erro: CRM residente inválido"
            return render_template("novo_atendimento.html", feedback=mensagem_erro)

        if paciente_cpf and preceptor_crm and residente_crm and duracao and id_unidade:
            
            try:
                
                # Verifica se existe e pega o id do paciente, preceptor e residente
                resultado_paciente = database.db.session.scalar(select(Pessoa.id_pessoa).where(paciente_cpf == Pessoa.cpf))
                if not resultado_paciente:
                    mensagem_erro = "Erro: Paciente não encontrado."

                resultado_preceptor = database.db.session.scalar(select(Profissional.id_pessoa).where(preceptor_crm == Profissional.crm))
                if not resultado_preceptor:
                    mensagem_erro = "Erro: Preceptor não encontrado."

                resultado_residente = database.db.session.scalar(select(Profissional.id_pessoa).where(residente_crm == Profissional.crm))
                if not resultado_residente:
                    mensagem_erro = "Erro: Residente não encontrado."

                if mensagem_erro is None:
                    
                    Novo_Atendimento = Atendimento(
                        id_paciente = resultado_paciente,
                        id_preceptor = resultado_preceptor,
                        id_residente = resultado_residente,
                        duracao_minutos = duracao,
                        data_hora = data_hora,
                        id_unidade = id_unidade
                    )

                    database.db.session.add(Novo_Atendimento)
                    database.db.session.commit()
                    
                    mensagem_erro = "Atendimento registrado com sucesso!"

            # Captura falhas e faz rollback do banco
            except Exception as e:
                database.conexao.rollback()
                mensagem_erro = f"Erro na operação: {e}"

        else:
            mensagem_erro = "Preencha todos os campos."
            
        return render_template("novo_atendimento.html", unidades=lista_unidades, feedback=mensagem_erro)


#
# Método para listar todos os procedimentos realizados em um atendimento
#
@listar_procedimentos_bp.route('/listar_procedimentos', methods=['GET'])
def listar_procedimentos():

    if request.method == 'GET':

        # Variáveis
        procedimentos = []
        mensagem_erro = None

        # Recebe o atributo id_atendimento enviado pela requisição
        id_atendimento = request.args.get('id_atendimento')

        # Verifica se o atributo existe
        if not id_atendimento:
            return render_template("listar_procedimentos.html")

        # Realiza a validação do id (deve ser um número inteiro)
        if not id_atendimento.isdigit():
            mensagem_erro = "Erro: Nº de atendimento inválido"
            return render_template("listar_procedimentos.html", feedback=mensagem_erro)

        cursor = database.conexao.cursor()

        # Confirma se o atendimento existe antes de consultar os procedimentos
        cursor.execute("SELECT id_atendimento FROM ATENDIMENTO WHERE id_atendimento = %s", (id_atendimento,))
        resultado_atendimento = cursor.fetchone()

        if not resultado_atendimento:
            mensagem_erro = "Erro: Atendimento não encontrado."
            cursor.close()
            return render_template("listar_procedimentos.html", feedback=mensagem_erro)

        consulta = """
            select p.codigo, p.nome, pr.quantidade, pr.tempo_real_minutos, pr.observacao, pr.is_faturado
            from procedimento_realizado pr
            inner join procedimento p on p.id_procedimento = pr.id_procedimento
            where pr.id_atendimento = %s
            and pr.is_removido = FALSE
            order by p.nome
        """

        cursor.execute(consulta, (id_atendimento,))
        procedimentos = cursor.fetchall()

        cursor.close()

        return render_template("listar_procedimentos.html", lista_procedimentos=procedimentos, feedback=mensagem_erro)
        