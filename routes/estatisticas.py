#
# Arquivo para tratamento do endpoint relacionado as estatísticas
#

from flask import Blueprint, render_template, request
import database

#ranking_residentes_bp = Blueprint("ranking_residentes", __name__)
estatisticas_bp = Blueprint("Estatisticas", __name__)

#@ranking_residentes_bp.route('/ranking_residentes', methods=['POST'])
def get_ranking_residentes():
    cursor = database.conexao.cursor()

    consulta = """
        SELECT p.nome, count(*)
        FROM residente r
        INNER JOIN pessoa p ON p.id_pessoa  = r.id_profissional
        inner join atendimento a on a.id_residente = r.id_profissional
        group by p.id_pessoa, p.nome 
        order by count(*) desc
    """

    cursor.execute(consulta)
    ranking = cursor.fetchall()

    return ranking

@estatisticas_bp.route('/estatisticas', methods=['GET'])
def estatisticas():

    ranking = get_ranking_residentes()

    return render_template('estatisticas.html', ranking_residentes=ranking)