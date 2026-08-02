#
# Arquivo para tratamento do endpoint unificado de pacientes
# Reúne, em /atualizar_paciente, as 2 abas: atualizar dados e sem risco alto.
#


from flask import Blueprint, render_template, request
from include.verify import validar_cpf
import database

paciente_bp = Blueprint("paciente", __name__)


#
# Aba "Sem Risco Alto": pacientes que nunca realizaram procedimento de risco ALTO

def get_pacientes_sem_risco_alto():

    cursor = database.conexao.cursor()

    consulta = """
        SELECT
            p.nome,
            p.cpf
        FROM pessoa p
        INNER JOIN paciente pa
            ON pa.id_pessoa = p.id_pessoa
        WHERE NOT EXISTS (

            SELECT 1
            FROM atendimento a
            INNER JOIN procedimento_realizado pr
                ON pr.id_atendimento = a.id_atendimento
            INNER JOIN procedimento proc
                ON proc.id_procedimento = pr.id_procedimento

            WHERE a.id_paciente = pa.id_pessoa
              AND proc.nivel_risco = 'ALTO'
              AND pr.is_removido = FALSE

        )
        ORDER BY p.nome;
    """

    cursor.execute(consulta)
    pacientes = cursor.fetchall()
    cursor.close()

    return pacientes


#
# Aba "Atualizar Dados": atualiza endereço e/ou convênio de um paciente
#
def atualizar_dados_paciente():

    mensagem_erro = None

    cpf = request.form.get("cpf")

    cep = request.form.get("cep")
    logradouro = request.form.get("logradouro")
    numero = request.form.get("numero")
    complemento = request.form.get("complemento")
    bairro = request.form.get("bairro")
    cidade = request.form.get("cidade")
    uf = request.form.get("uf")

    convenio = request.form.get("convenio")

    if not validar_cpf(cpf):
        return "Erro: CPF inválido."

    cursor = database.conexao.cursor()

    try:

        cursor.execute(
            """
            SELECT id_pessoa
            FROM pessoa
            WHERE cpf = %s
            """,
            (cpf,)
        )

        paciente = cursor.fetchone()

        if not paciente:
            mensagem_erro = "Paciente não encontrado."

        else:

            id_paciente = paciente[0]

            alterou = False

            campos = []
            valores  = []

            if cep:
                campos.append("cep = %s")
                valores.append(cep)

            if logradouro:
                campos.append("logradouro = %s")
                valores.append(logradouro)

            if numero:
                campos.append("numero = %s")
                valores.append(numero)

            if complemento:
                campos.append("complemento = %s")
                valores.append(complemento)

            if bairro:
                campos.append("bairro = %s")
                valores.append(bairro)

            if cidade:
                campos.append("cidade = %s")
                valores.append(cidade)

            if uf:
                campos.append("uf = %s")
                valores.append(uf)

            # Executa UPDATE somente se algum campo foi preenchido
            if campos:

                consulta = f"""
                    UPDATE pessoa
                    SET {', '.join(campos)}
                    WHERE id_pessoa = %s
                """

                valores.append(id_paciente)

                cursor.execute(consulta, tuple(valores))

                alterou = True

            if convenio:

                cursor.execute(
                    """
                    UPDATE paciente
                    SET numero_convenio = %s
                    WHERE id_pessoa = %s
                    """,
                    (
                        convenio,
                        id_paciente
                    )
                )

                alterou = True

            database.conexao.commit()

            if alterou:
                mensagem_erro = "Paciente atualizado com sucesso."
            else:
                mensagem_erro = "Nenhum houve nenhuma alteração."


    except Exception as e:

        database.conexao.rollback()
        mensagem_erro = f"Erro na operação: {e}"

    finally:

        cursor.close()

    return mensagem_erro


#
# Rota única da página Pacientes, com 2 abas controladas por ?tab=
#
@paciente_bp.route('/paciente', methods=['GET', 'POST'])
def atualizar_paciente():

    feedback = None
    aba = request.args.get('tab', 'atualizar')

    if request.method == 'POST':
        feedback = atualizar_dados_paciente()
        aba = 'atualizar'

    if aba == 'sem_alto':
        pacientes = get_pacientes_sem_risco_alto()
        return render_template(
            "paciente.html",
            feedback=feedback,
            pacientes=pacientes
        )

    return render_template(
        "paciente.html",
        feedback=feedback
    )