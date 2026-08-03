from database import db
from sqlalchemy.sql import func

# ==============================================================================
# 1. PESSOA E HERANÇAS (Paciente, Profissional, Preceptor, Residente)
# ==============================================================================

class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id_pessoa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    is_flamengo = db.Column(db.Boolean, nullable=False)
    telefone = db.Column(db.String(13), nullable=False)
    cep = db.Column(db.String(8))
    logradouro = db.Column(db.String(150))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))


class Paciente(db.Model):
    __tablename__ = 'paciente'

    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), primary_key=True)
    numero_convenio = db.Column(db.String(20), unique=True, nullable=False)
    tipo_sanguineo = db.Column(db.String(3), nullable=False)


class Profissional(db.Model):
    __tablename__ = 'profissional'

    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), primary_key=True)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)


class Preceptor(db.Model):
    __tablename__ = 'preceptor'

    id_profissional = db.Column(db.Integer, db.ForeignKey('profissional.id_pessoa'), primary_key=True)
    titulacao = db.Column(db.String(50), nullable=False)


class Residente(db.Model):
    __tablename__ = 'residente'

    id_profissional = db.Column(db.Integer, db.ForeignKey('profissional.id_pessoa'), primary_key=True)
    ano_residencia = db.Column(db.String(2), nullable=False)


# ==============================================================================
# 2. TABELAS AUXILIARES E DE LIGAÇÃO (Alergias)
# ==============================================================================

class Alergia(db.Model):
    __tablename__ = 'alergia'

    id_alergia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    gravidade = db.Column(db.String(20), nullable=False)


class PacienteTemAlergia(db.Model):
    __tablename__ = 'paciente_tem_alergia'

    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id_pessoa'), primary_key=True)
    id_alergia = db.Column(db.Integer, db.ForeignKey('alergia.id_alergia'), primary_key=True)


# ==============================================================================
# 3. UNIDADES E PROCEDIMENTOS
# ==============================================================================

class Unidade(db.Model):
    __tablename__ = 'unidade'

    id_unidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    capacidade_leitos = db.Column(db.Integer, nullable=False)
    tempo_medio_espera_minutos = db.Column(db.Numeric(10, 2), default=0)


class Procedimento(db.Model):
    __tablename__ = 'procedimento'

    id_procedimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(6), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    tempo_medio_minutos = db.Column(db.Integer, nullable=False)
    nivel_risco = db.Column(db.String(20), default='BAIXO')


# ==============================================================================
# 4. OPERACIONAIS (Atendimento, Escala, Internação e Procedimentos Realizados)
# ==============================================================================

class Atendimento(db.Model):
    __tablename__ = 'atendimento'

    id_atendimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id_pessoa'), nullable=False)
    id_residente = db.Column(db.Integer, db.ForeignKey('residente.id_profissional'), nullable=False)
    id_preceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id_profissional'), nullable=False)
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidade.id_unidade'), nullable=False)


class Escala(db.Model):
    __tablename__ = 'escala'

    id_escala = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidade.id_unidade'), nullable=False)
    dia_semana = db.Column(db.String(15), nullable=False)
    turno = db.Column(db.String(10), nullable=False)
    id_residente = db.Column(db.Integer, db.ForeignKey('residente.id_profissional'), nullable=False)
    id_preceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id_profissional'), nullable=False)


class ProcedimentoRealizado(db.Model):
    __tablename__ = 'procedimento_realizado'

    id_atendimento = db.Column(db.Integer, db.ForeignKey('atendimento.id_atendimento'), primary_key=True)
    id_procedimento = db.Column(db.Integer, db.ForeignKey('procedimento.id_procedimento'), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    tempo_real_minutos = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.String(200), nullable=False)
    is_faturado = db.Column(db.Boolean, default=False)
    is_removido = db.Column(db.Boolean, default=False)
    data_hora_inicio = db.Column(db.DateTime, nullable=True)


class Internacao(db.Model):
    __tablename__ = 'internacao'

    id_internacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id_pessoa'), nullable=False)
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidade.id_unidade'), nullable=False)
    data_hora_entrada = db.Column(db.DateTime, nullable=False, server_default=func.now())
    data_hora_saida = db.Column(db.DateTime, nullable=True)