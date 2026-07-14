#
# Arquivo para tratamento do endpoint relacionado aos atendimentos
#

from flask import Blueprint, render_template, request
import database

listar_atendimentos_bp = Blueprint("listar_atendimentos", __name__)

@listar_atendimentos_bp.route('/listar_atendimentos', methods=['GET', 'POST'])
def listar_atendimento():
    if request.method == 'GET':
        paciente_cpf = request.args.get('cpf')

        atendimentos = []
        mensagem_erro = None
        
        if paciente_cpf:
            cursor = database.conexao.cursor()

            consulta = """select a.id_atendimento, a.data_hora, a.duracao_minutos, p_p.nome, p_pre.nome, p_re.nome
                            from atendimento a
                            inner join pessoa p_p on p_p.id_pessoa = a.id_paciente 
                            inner join pessoa p_pre on p_pre.id_pessoa = a.id_preceptor 
                            inner join pessoa p_re on p_re.id_pessoa = a.id_residente 
                            where p_p.cpf = %s
                            order by a.data_hora desc"""
            
            cursor.execute(consulta, (paciente_cpf,))
            atendimentos = cursor.fetchall()

            cursor.close()

        return render_template("listar_atendimento.html", lista_atendimentos=atendimentos)
