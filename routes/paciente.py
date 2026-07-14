from flask import Blueprint, render_template, request
from include.verify import validar_cpf
import database

atualizar_paciente_bp = Blueprint("atualizar_paciente", __name__)

# Método para atualizar endereço ou convênio de um paciente
@atualizar_paciente_bp.route('/atualizar_paciente', methods=['GET', 'POST'])
def atualizar_paciente():

    if request.method == 'GET':
        return render_template("atualizar_paciente.html")

    else:

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
            mensagem_erro = "Erro: CPF inválido."
            return render_template("atualizar_paciente.html", feedback=mensagem_erro)

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

                # Atualiza endereço
                cursor.execute(
                    """
                    UPDATE pessoa
                    SET
                        cep=%s,
                        logradouro=%s,
                        numero=%s,
                        complemento=%s,
                        bairro=%s,
                        cidade=%s,
                        uf=%s
                    WHERE id_pessoa=%s
                    """,
                    (
                        cep,
                        logradouro,
                        numero,
                        complemento,
                        bairro,
                        cidade,
                        uf,
                        id_paciente
                    )
                )

                # Atualiza convênio
                cursor.execute(
                    """
                    UPDATE paciente
                    SET numero_convenio=%s
                    WHERE id_pessoa=%s
                    """,
                    (
                        convenio,
                        id_paciente
                    )
                )

                database.conexao.commit()

                mensagem_erro = "Paciente atualizado com sucesso."

        except Exception as e:

            database.conexao.rollback()
            mensagem_erro = f"Erro na operação: {e}"

        finally:

            cursor.close()

        return render_template(
            "atualizar_paciente.html",
            feedback=mensagem_erro
        )