from flask import Blueprint, render_template, request
import database

remover_procedimento_bp = Blueprint("remover_procedimento", __name__)

@remover_procedimento_bp.route('/remover_procedimento', methods=['GET', 'POST'])
def remover_procedimento():
    feedback = None
    dados_atendimento = None
    lista_procedimentos = []
    
    # Capturando usando a nomenclatura do HTML
    id_atendimento = request.args.get('id_atendimento') or request.form.get('id_atendimento')
    id_procedimento = request.form.get('id_procedimento')

    cursor = database.conexao.cursor()

    try:
        database.conexao.rollback()

        if request.method == 'POST' and id_procedimento and id_atendimento:
            # 1. Verifica se o procedimento já foi faturado na tabela "procedimento_realizado"
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
                # 2. Executa a exclusão lógica (definindo is_removido como TRUE) ou física.
               
                cursor.execute("""
                    UPDATE procedimento_realizado 
                    SET is_removido = TRUE 
                    WHERE id_atendimento = %s AND id_procedimento = %s
                """, (id_atendimento, id_procedimento))
                
                database.conexao.commit()
                feedback = "Procedimento removido com sucesso!"

        # SE TEMOS UM ATENDIMENTO SENDO CONSULTADO/REMOVIDO
        if id_atendimento:
            
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
                # Busca os procedimentos vinculados na tabela "procedimento_realizado"
                
                cursor.execute("""
                    SELECT pr.id_procedimento, pr.nome, pr_real.quantidade, 
                           pr_real.tempo_real_minutos, pr_real.observacao, pr_real.is_faturado
                    FROM procedimento_realizado pr_real
                    INNER JOIN procedimento pr ON pr_real.id_procedimento = pr.id_procedimento
                    WHERE pr_real.id_atendimento = %s AND pr_real.is_removido = FALSE
                """, (id_atendimento,))
                lista_procedimentos = cursor.fetchall()
            else:
                feedback = "Erro: Atendimento não encontrado."

    except Exception as e:
        database.conexao.rollback()
        feedback = f"Erro na operação: {e}"
    finally:
        cursor.close()

    # Retorna o HTML passando as variáveis padronizadas
    return render_template(
        "remover_procedimento.html", 
        dados_atendimento=dados_atendimento, 
        lista_procedimentos=lista_procedimentos, 
        feedback=feedback,
        id_atendimento_buscado=id_atendimento
    )