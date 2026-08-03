from flask import Blueprint, render_template
from sqlalchemy import text
from database import db

triggers_bp = Blueprint("triggers", __name__)


@triggers_bp.route("/triggers")
def menu_triggers():
    return render_template("triggers.html")


@triggers_bp.route("/triggers/auditoria")
def auditoria():

    auditorias = db.session.execute(
        text("""
            SELECT
                id_auditoria,
                id_atendimento,
                operacao,
                usuario_bd,
                data_hora,
                dados_antigos,
                dados_novos
            FROM auditoria_atendimento
            ORDER BY data_hora DESC
        """)
    ).mappings().all()

    return render_template(
        "auditoria.html",
        auditorias=auditorias
    )

@triggers_bp.route("/triggers/media_procedimentos")
def media_procedimentos():

    procedimentos = db.session.execute(
        text("""
            SELECT
                id_procedimento,
                codigo,
                nome,
                nivel_risco,
                tempo_medio_minutos
            FROM procedimento
            ORDER BY nome
        """)
    ).mappings().all()

    return render_template(
        "media_procedimentos.html",
        procedimentos=procedimentos
    )