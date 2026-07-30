#
# Arquivo para tratamento do endpoint relacionado aos atendimentos
#

from flask import Blueprint, render_template, request
from include.verify import validar_cpf, validar_crm
from sqlalchemy.orm import aliased
from models import Atendimento, Pessoa, Procedimento, ProcedimentoRealizado
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

        if paciente_cpf and preceptor_crm and residente_crm and duracao:
            cursor = database.conexao.cursor()
            
            try:
                
                cursor.execute("SELECT id_pessoa FROM PESSOA WHERE cpf = %s", (paciente_cpf,))
                resultado_paciente = cursor.fetchone()

                cursor.execute("SELECT id_pessoa FROM PROFISSIONAL WHERE crm = %s", (preceptor_crm,))
                resultado_preceptor = cursor.fetchone()

                cursor.execute("SELECT id_pessoa FROM PROFISSIONAL WHERE crm = %s", (residente_crm,))
                resultado_residente = cursor.fetchone()

                if not resultado_paciente:
                    mensagem_erro = "Erro: Paciente não encontrado."
                elif not resultado_preceptor:
                    mensagem_erro = "Erro: Preceptor não encontrado."
                elif not resultado_residente:
                    mensagem_erro = "Erro: Residente não encontrado."

                else:

                    id_pac = resultado_paciente[0]
                    id_prec = resultado_preceptor[0]
                    id_res = resultado_residente[0]

                    consulta_insert = """
                        INSERT INTO ATENDIMENTO 
                        (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor, id_unidade) 
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(consulta_insert, (data_hora, duracao, id_pac, id_res, id_prec, id_unidade))
                    database.conexao.commit()
                    
                    mensagem_erro = "Atendimento registrado com sucesso!"

            # Captura falhas e faz rollback do banco
            except Exception as e:
                database.conexao.rollback()
                mensagem_erro = f"Erro na operação: {e}"

            finally:
                cursor.close()

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

        # Confirma se o atendimento existe antes de consultar os procedimentos
        atendimento_existe = database.db.session.query(
            Atendimento.id_atendimento
        ).filter(
            Atendimento.id_atendimento == id_atendimento
        ).first()

        if not atendimento_existe:
            mensagem_erro = "Erro: Atendimento não encontrado."
            return render_template("listar_procedimentos.html", feedback=mensagem_erro)

        # Monta a pesquisa dos procedimentos realizados no atendimento
        query = database.db.session.query(
            Procedimento.codigo,
            Procedimento.nome,
            ProcedimentoRealizado.quantidade,
            ProcedimentoRealizado.tempo_real_minutos,
            ProcedimentoRealizado.observacao,
            ProcedimentoRealizado.is_faturado
        ).join(
            Procedimento, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento
        ).filter(
            ProcedimentoRealizado.id_atendimento == id_atendimento,
            ProcedimentoRealizado.is_removido == False
        ).order_by(
            Procedimento.nome
        )

        procedimentos = query.all()

        return render_template("listar_procedimentos.html", lista_procedimentos=procedimentos, feedback=mensagem_erro)