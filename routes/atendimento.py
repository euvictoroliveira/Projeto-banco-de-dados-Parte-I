#
# Arquivo para tratamento do endpoint relacionado aos atendimentos
#

from flask import Blueprint, render_template, request
import database

atendimento_bp = Blueprint("atendimento", __name__)

@atendimento_bp.route('/atendimento', methods=['GET', 'POST'])
def atendimento():
    if request.method == 'GET':
        cursor = database.conexao.cursor()

        consulta = """SELECT * FROM atendimento"""
        
        cursor.execute(consulta)
        atendimentos = cursor.fetchall()

        cursor.close()

        return render_template("atendimento.html", lista_atendimentos=atendimentos)
        