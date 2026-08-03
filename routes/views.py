from flask import Blueprint, render_template
from sqlalchemy import text
from database import db

views_bp = Blueprint("views", __name__)


# ==========================================================
# Menu das Views
# ==========================================================

@views_bp.route("/views")
def menu_views():
    return render_template("views.html")


# View: Pacientes Internados
@views_bp.route("/vw_pacientes_internados")
def pacientes_internados():

    pacientes = db.session.execute(
        text("""
            SELECT *
            FROM vw_pacientes_internados
            ORDER BY nome_paciente
        """)
    ).mappings().all()

    return render_template(
        "vw_pacientes_internados.html",
        pacientes=pacientes
    )

# View: Residentes sem Supervisor
@views_bp.route("/vw_residentes_sem_supervisor")
def residentes_sem_supervisor():

    residentes = db.session.execute(
        text("""
            SELECT *
            FROM vw_residentes_sem_supervisor
            ORDER BY nome_residente
        """)
    ).mappings().all()

    return render_template(
        "vw_residentes_sem_supervisor.html",
        residentes=residentes
    )


# View: Estatísticas Mensais
@views_bp.route("/vw_estatisticas_mensais")
def estatisticas_mensais():

    estatisticas = db.session.execute(
        text("""
            SELECT *
            FROM vw_estatisticas_atendimentos_mensal
            ORDER BY mes DESC, unidade
        """)
    ).mappings().all()

    return render_template(
        "vw_estatisticas_mensais.html",
        estatisticas=estatisticas
    )