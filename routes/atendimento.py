#
# Arquivo para tratamento do endpoint relacionado aos atendimentos
#

from flask import Blueprint, render_template, request
from include.verify import validar_cpf, validar_crm
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
        

        cursor = database.conexao.cursor()

        consulta = """
            select a.id_atendimento, a.data_hora, a.duracao_minutos, p_p.nome, p_pre.nome, p_re.nome
            from atendimento a
            inner join pessoa p_p on p_p.id_pessoa = a.id_paciente 
            inner join pessoa p_pre on p_pre.id_pessoa = a.id_preceptor 
            inner join pessoa p_re on p_re.id_pessoa = a.id_residente 
            where p_p.cpf = %s
            order by a.data_hora desc
        """
        
        cursor.execute(consulta, (paciente_cpf,))
        atendimentos = cursor.fetchall()

        cursor.close()

        return render_template("listar_atendimento.html", lista_atendimentos=atendimentos, feedback=mensagem_erro)


#
# Método para criar um novo atendimento
#
@novo_atendimento_bp.route('/novo_atendimento', methods=['GET','POST'])
def novo_atendimento():
    
    if request.method == 'GET':
        return render_template("novo_atendimento.html")

    else:
        paciente_cpf = request.form.get('cpf')
        preceptor_crm = request.form.get('preceptor')
        residente_crm = request.form.get('residente')
        duracao = request.form.get('duracao')
        data_hora = time.strftime('%Y-%m-%d %H:%M:%S')

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
                        (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    cursor.execute(consulta_insert, (data_hora, duracao, id_pac, id_res, id_prec))
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
            
        return render_template("novo_atendimento.html", feedback=mensagem_erro)


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
        