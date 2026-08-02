#
# Arquivo para tratamento do endpoint unificado de atendimentos
# Reúne, em /novo_atendimento, as 3 abas: registrar, listar e remover procedimento.

from flask import Blueprint, render_template, request
from include.verify import validar_cpf, validar_crm
from sqlalchemy import select, and_, func
from sqlalchemy.orm import aliased
from models import *
import database
import time
import json

atendimento_bp = Blueprint("atendimento", __name__)


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
    cursor.close()

    return resultado


#
# Método para buscar os procedimentos disponíveis e popular o dropdown de procedimentos
#
def get_procedimentos_disponiveis():
    cursor = database.conexao.cursor()

    consulta = """
        select id_procedimento, nome
        from procedimento
        order by nome
    """

    cursor.execute(consulta)
    resultado = cursor.fetchall()
    cursor.close()

    # o template acessa proc.id / proc.nome; dicionário funciona com essa notação no Jinja
    return [{"id": linha[0], "nome": linha[1]} for linha in resultado]


#
# Aba "Listar": todos os atendimentos, com filtro opcional por CPF.
# Também agrega, numa única query, os nomes dos procedimentos realizados em cada
# atendimento (evita fazer uma query extra por linha da tabela).
#
def buscar_atendimentos(cpf=None):

    PessoaPaciente = aliased(Pessoa)
    PessoaPreceptor = aliased(Pessoa)
    PessoaResidente = aliased(Pessoa)

    query = database.db.session.query(
        Atendimento.id_atendimento,
        Atendimento.data_hora,
        Atendimento.duracao_minutos,
        PessoaPaciente.nome.label('nome_paciente'),
        PessoaPreceptor.nome.label('nome_preceptor'),
        PessoaResidente.nome.label('nome_residente'),
        func.string_agg(Procedimento.nome, ', ').label('procedimentos')
    ).join(
        PessoaPaciente, Atendimento.id_paciente == PessoaPaciente.id_pessoa
    ).join(
        PessoaPreceptor, Atendimento.id_preceptor == PessoaPreceptor.id_pessoa
    ).join(
        PessoaResidente, Atendimento.id_residente == PessoaResidente.id_pessoa
    ).outerjoin(
        ProcedimentoRealizado, and_(
            ProcedimentoRealizado.id_atendimento == Atendimento.id_atendimento,
            ProcedimentoRealizado.is_removido == False
        )
    ).outerjoin(
        Procedimento, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento
    ).group_by(
        Atendimento.id_atendimento,
        Atendimento.data_hora,
        Atendimento.duracao_minutos,
        PessoaPaciente.nome,
        PessoaPreceptor.nome,
        PessoaResidente.nome
    ).order_by(
        Atendimento.data_hora.desc()
    )

    if cpf:
        query = query.filter(PessoaPaciente.cpf == cpf)

    return query.all()


#
# Aba "Remover": dados do atendimento + procedimentos realizados nele
# 
def buscar_atendimento_e_procedimentos(id_atendimento):

    cursor = database.conexao.cursor()
    dados_atendimento = None
    lista_procedimentos = []

    try:
        cursor.execute("""
            SELECT a.id_atendimento, p_pac.nome, p_prec.nome, p_res.nome 
            FROM atendimento a
            INNER JOIN pessoa p_pac ON a.id_paciente = p_pac.id_pessoa
            INNER JOIN pessoa p_prec ON a.id_preceptor = p_prec.id_pessoa
            INNER JOIN pessoa p_res ON a.id_residente = p_res.id_pessoa
            WHERE a.id_atendimento = %s
        """, (id_atendimento,))
        dados_atendimento = cursor.fetchone()

        if dados_atendimento:
            cursor.execute("""
                SELECT pr.id_procedimento, pr.nome, pr_real.quantidade, 
                       pr_real.tempo_real_minutos, pr_real.observacao, pr_real.is_faturado
                FROM procedimento_realizado pr_real
                INNER JOIN procedimento pr ON pr_real.id_procedimento = pr.id_procedimento
                WHERE pr_real.id_atendimento = %s AND pr_real.is_removido = FALSE
            """, (id_atendimento,))
            lista_procedimentos = cursor.fetchall()

    finally:
        cursor.close()

    return dados_atendimento, lista_procedimentos


#
# Ação (POST acao=remover_procedimento): remove logicamente um procedimento realizado
# 
def remover_procedimento_realizado():

    id_atendimento = request.form.get('id_atendimento')
    id_procedimento = request.form.get('id_procedimento')
    feedback = None

    cursor = database.conexao.cursor()

    try:
        database.conexao.rollback()

        cursor.execute("""
            SELECT is_faturado FROM procedimento_realizado 
            WHERE id_atendimento = %s AND id_procedimento = %s AND is_removido = FALSE
        """, (id_atendimento, id_procedimento))
        resultado = cursor.fetchone()

        if not resultado:
            feedback = "Erro: Procedimento não encontrado neste atendimento."
        elif resultado[0] == True:
            feedback = "Erro: Este procedimento já foi faturado e não pode ser removido."
        else:
            cursor.execute("""
                UPDATE procedimento_realizado 
                SET is_removido = TRUE 
                WHERE id_atendimento = %s AND id_procedimento = %s
            """, (id_atendimento, id_procedimento))

            database.conexao.commit()
            feedback = "Procedimento removido com sucesso!"

    except Exception as e:
        database.conexao.rollback()
        feedback = f"Erro na operação: {e}"

    finally:
        cursor.close()

    return feedback


#
# Ação (POST acao=registrar): valida CPF/CRM (igual ao novo_atendimento() original) e,
# em vez de inserir só o atendimento, chama a procedure sp_registrar_atendimento_completo,
# que insere o atendimento + a lista de procedimentos em uma única transação.
#
def registrar_atendimento_completo():

    paciente_cpf = request.form.get('cpf')
    preceptor_crm = request.form.get('preceptor')
    residente_crm = request.form.get('residente')
    duracao = request.form.get('duracao')
    data_hora = time.strftime('%Y-%m-%d %H:%M:%S')
    id_unidade = request.form.get('id_unidade')

    # Validações (idênticas às de novo_atendimento() em atendimento.py)
    if not validar_cpf(paciente_cpf):
        return "Erro: CPF inválido"

    if not validar_crm(preceptor_crm):
        return "Erro: CRM preceptor inválido"

    if not validar_crm(residente_crm):
        return "Erro: CRM residente inválido"

    if not (paciente_cpf and preceptor_crm and residente_crm and duracao and id_unidade):
        return "Preencha todos os campos."

    try:
        # Verifica se existe e pega o id do paciente, preceptor e residente
        resultado_paciente = database.db.session.scalar(select(Pessoa.id_pessoa).where(paciente_cpf == Pessoa.cpf))
        if not resultado_paciente:
            return "Erro: Paciente não encontrado."

        resultado_preceptor = database.db.session.scalar(select(Profissional.id_pessoa).where(preceptor_crm == Profissional.crm))
        if not resultado_preceptor:
            return "Erro: Preceptor não encontrado."

        resultado_residente = database.db.session.scalar(select(Profissional.id_pessoa).where(residente_crm == Profissional.crm))
        if not resultado_residente:
            return "Erro: Residente não encontrado."

        # Monta a lista de procedimentos enviados no formulário (linhas em branco são ignoradas)
        procedimento_ids = request.form.getlist('procedimento_id[]')
        quantidades = request.form.getlist('quantidade[]')
        tempos_reais = request.form.getlist('tempo_real[]')
        observacoes = request.form.getlist('observacao[]')

        procedimentos = []
        for i in range(len(procedimento_ids)):
            if procedimento_ids[i]:
                procedimentos.append({
                    "id_procedimento": int(procedimento_ids[i]),
                    "quantidade": int(quantidades[i]),
                    "tempo_real_minutos": int(tempos_reais[i]),
                    "observacao": observacoes[i]
                })

        if not procedimentos:
            return "Erro: informe ao menos um procedimento realizado."

        cursor = database.conexao.cursor()

        try:
            # sp_registrar_atendimento_completo(
            #     p_data_hora, p_duracao_minutos, p_id_paciente, p_id_residente,
            #     p_id_preceptor, p_id_unidade, p_procedimentos JSONB,
            #     INOUT p_id_atendimento INTEGER DEFAULT NULL
            # )
            cursor.execute(
                "CALL sp_registrar_atendimento_completo(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data_hora,
                    duracao,
                    resultado_paciente,
                    resultado_residente,
                    resultado_preceptor,
                    id_unidade,
                    json.dumps(procedimentos),
                    None
                )
            )

            # a procedure devolve o id_atendimento gerado através do parâmetro INOUT
            linha_retorno = cursor.fetchone()
            id_atendimento_criado = linha_retorno[0] if linha_retorno else None

            database.conexao.commit()

        finally:
            cursor.close()

        return f"Atendimento Nº {id_atendimento_criado} registrado com sucesso!"

    except Exception as e:
        database.conexao.rollback()
        return f"Erro na operação: {e}"


#
# Rota única da página Atendimento, com 3 abas controladas por ?tab=
#
@atendimento_bp.route('/atendimento', methods=['GET', 'POST'])
def atendimento():

    lista_unidades = get_lista_unidade()
    procedimentos_disponiveis = get_procedimentos_disponiveis()
    feedback = None
    aba = request.args.get('tab', 'registrar')

    # dados extras que podem ser reaproveitados depois de um POST
    cpf_buscado = None
    dados_atendimento = None
    lista_procedimentos = []
    id_atendimento_buscado = None

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'registrar':
            feedback = registrar_atendimento_completo()
            aba = 'registrar'

        elif acao == 'remover_procedimento':
            feedback = remover_procedimento_realizado()
            aba = 'remover'

            # recarrega a mesma consulta de procedimentos, já refletindo a remoção
            id_atendimento_buscado = request.form.get('id_atendimento')
            dados_atendimento, lista_procedimentos = buscar_atendimento_e_procedimentos(id_atendimento_buscado)

    if aba == 'listar' and request.method == 'GET':
        cpf_buscado = request.args.get('cpf')

        if cpf_buscado and not validar_cpf(cpf_buscado):
            feedback = "Erro: CPF inválido"
            lista_atendimentos = []
        else:
            # sem CPF informado, cpf_buscado é None e a função lista todos os atendimentos
            lista_atendimentos = buscar_atendimentos(cpf_buscado)

        return render_template(
            "atendimento.html",
            unidades=lista_unidades,
            procedimentos_disponiveveis=procedimentos_disponiveis,
            feedback=feedback,
            lista_atendimentos=lista_atendimentos,
            cpf_buscado=cpf_buscado
        )

    if aba == 'remover' and request.method == 'GET':
        id_atendimento_buscado = request.args.get('id_atendimento')

        if id_atendimento_buscado:
            dados_atendimento, lista_procedimentos = buscar_atendimento_e_procedimentos(id_atendimento_buscado)
            if not dados_atendimento:
                feedback = "Erro: Atendimento não encontrado."

    # cobre: aba 'registrar' (GET/POST) e aba 'remover' (GET com busca, ou pós-POST de remoção)
    return render_template(
        "atendimento.html",
        unidades=lista_unidades,
        procedimentos_disponiveveis=procedimentos_disponiveis,
        feedback=feedback,
        dados_atendimento=dados_atendimento,
        lista_procedimentos=lista_procedimentos,
        id_atendimento_buscado=id_atendimento_buscado
    )