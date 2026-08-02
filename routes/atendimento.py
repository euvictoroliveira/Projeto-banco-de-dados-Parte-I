#
# Arquivo para tratamento do endpoint relacionado aos atendimentos
#

from flask import Blueprint, render_template, request
from include.verify import validar_cpf, validar_crm
from sqlalchemy import select, and_
from sqlalchemy.orm import aliased
from models import *
import database
import time

atendimento_bp = Blueprint("atendimento", __name__)

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
# Ação (POST acao=remover_procedimento): remove logicamente um procedimento realizado
# 
def remover_procedimento_realizado():
    id_atendimento = request.form.get('id_atendimento')
    id_procedimento = request.form.get('id_procedimento')
    feedback = None

    try:

        proc_realizado = database.db.session.query(ProcedimentoRealizado).filter(
            ProcedimentoRealizado.id_atendimento == id_atendimento,
            ProcedimentoRealizado.id_procedimento == id_procedimento,
            ProcedimentoRealizado.is_removido.is_(False)
        ).first()

        if not proc_realizado:
            feedback = "Erro: Procedimento não encontrado neste atendimento."

        elif proc_realizado.is_faturado:
            feedback = "Erro: Este procedimento já foi faturado e não pode ser removido."

        else:


            proc_realizado.is_removido = True
            database.db.session.commit()
            feedback = "Procedimento removido com sucesso!"

    except Exception as e:
        database.db.session.rollback()
        feedback = f"Erro na operação: {e}"

    return feedback

#
# Método para registrar um atendimento completo
#
def registrar_atendimento_completo():

    paciente_cpf = request.form.get('cpf')
    preceptor_crm = request.form.get('preceptor')
    residente_crm = request.form.get('residente')
    duracao = request.form.get('duracao')
    data_hora = time.strftime('%Y-%m-%d %H:%M:%S')
    id_unidade = request.form.get('id_unidade')

    # Validações 
    if not validar_cpf(paciente_cpf): return "Erro: CPF inválido"
    if not validar_crm(preceptor_crm): return "Erro: CRM preceptor inválido"
    if not validar_crm(residente_crm): return "Erro: CRM residente inválido"
    if not (paciente_cpf and preceptor_crm and residente_crm and duracao and id_unidade):
        return "Preencha todos os campos."

    try:
        # Recupera os IDs necessários
        id_pac = database.db.session.scalar(select(Pessoa.id_pessoa).where(Pessoa.cpf == paciente_cpf))
        id_prec = database.db.session.scalar(select(Profissional.id_pessoa).where(Profissional.crm == preceptor_crm))
        id_res = database.db.session.scalar(select(Profissional.id_pessoa).where(Profissional.crm == residente_crm))

        if not id_pac: return "Erro: Paciente não encontrado."
        if not id_prec: return "Erro: Preceptor não encontrado."
        if not id_res: return "Erro: Residente não encontrado."

        # Cria o objeto do Atendimento e envia para o banco
        novo_atend = Atendimento(
            data_hora=data_hora,
            duracao_minutos=duracao,
            id_paciente=id_pac,
            id_residente=id_res,
            id_preceptor=id_prec,
            id_unidade=id_unidade
        )
        database.db.session.add(novo_atend)
        
        # O .flush() envia o insert para o banco para gerar a Primary Key (id_atendimento), mas ainda não efetiva a transação. 
        database.db.session.flush() 

        # Prepara e insere os procedimentos vinculados ao novo ID gerado
        procedimento_ids = request.form.getlist('procedimento_id[]')
        quantidades = request.form.getlist('quantidade[]')
        tempos_reais = request.form.getlist('tempo_real[]')
        observacoes = request.form.getlist('observacao[]')

        proc_adicionados = 0
        for i in range(len(procedimento_ids)):
            if procedimento_ids[i]: # Ignora linhas vazias do formulário

                novo_proc = ProcedimentoRealizado(
                    id_atendimento=novo_atend.id_atendimento, # Pega o ID gerado pelo flush
                    id_procedimento=int(procedimento_ids[i]),
                    quantidade=int(quantidades[i]),
                    tempo_real_minutos=int(tempos_reais[i]),
                    observacao=observacoes[i]
                )

                database.db.session.add(novo_proc)
                proc_adicionados += 1

        if proc_adicionados == 0:
            database.db.session.rollback()
            return "Erro: informe ao menos um procedimento realizado."

        database.db.session.commit()
        return f"Atendimento Nº {novo_atend.id_atendimento} registrado com sucesso!"

    except Exception as e:
        database.db.session.rollback()
        return f"Erro na operação: {e}"

#
# Método para buscar as unidades e popular o dropdown
#
def get_lista_unidade():

    unidades = database.db.session.query(Unidade.id_unidade, Unidade.nome).order_by(Unidade.nome).all()
    return unidades

#
# Método para buscar os procedimentos disponíveis para o dropdown
#
def get_procedimentos_disponiveis():

    procedimentos = database.db.session.query(
        Procedimento.id_procedimento, 
        Procedimento.nome
    ).order_by(Procedimento.nome).all()
    
    return [{"id": p.id_procedimento, "nome": p.nome} for p in procedimentos]

#
# Aba "Remover": dados do atendimento + procedimentos realizados nele
# 
def buscar_atendimento_e_procedimentos(id_atendimento):

    PessoaPaciente = aliased(Pessoa)
    PessoaPreceptor = aliased(Pessoa)
    PessoaResidente = aliased(Pessoa)

    # Dados do atendimento
    dados_atendimento = database.db.session.query(
        Atendimento.id_atendimento,
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
        Atendimento.id_atendimento == id_atendimento
    ).first()

    lista_procedimentos = []
    
    # Procedimentos realizados
    if dados_atendimento:
        lista_procedimentos = database.db.session.query(
            Procedimento.id_procedimento,
            Procedimento.nome,
            ProcedimentoRealizado.quantidade,
            ProcedimentoRealizado.tempo_real_minutos,
            ProcedimentoRealizado.observacao,
            ProcedimentoRealizado.is_faturado
        ).join(
            Procedimento, ProcedimentoRealizado.id_procedimento == Procedimento.id_procedimento
        ).filter(
            ProcedimentoRealizado.id_atendimento == id_atendimento,
            ProcedimentoRealizado.is_removido.is_(False)
        ).all()

    return dados_atendimento, lista_procedimentos

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
