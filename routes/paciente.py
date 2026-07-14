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
                    mensagem = "Paciente atualizado com sucesso."
                else: 
                    mensagem = "Nenhum houve nenhuma alteração."


        except Exception as e:

            database.conexao.rollback()
            mensagem_erro = f"Erro na operação: {e}"

        finally:

            cursor.close()

        return render_template(
            "atualizar_paciente.html",
            feedback=mensagem
        )