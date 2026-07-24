-- Remove as tabelas existentes para evitar conflitos durante a criação
DROP TABLE IF EXISTS procedimento_realizado CASCADE;
DROP TABLE IF EXISTS escala CASCADE;
DROP TABLE IF EXISTS atendimento CASCADE;
DROP TABLE IF EXISTS procedimento CASCADE;
DROP TABLE IF EXISTS unidade CASCADE;
DROP TABLE IF EXISTS residente cascade;
DROP TABLE IF EXISTS preceptor CASCADE;
DROP TABLE IF EXISTS profissional CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS pessoa CASCADE;
drop table if exists alergia CASCADE;
drop table if exists paciente_tem_alergia CASCADE;

-- Cria a tabela pessoa
-- Atributos: ID(chave primária), nome, cpf, data de nascimento, is_flamengo, telefone e endereço
CREATE TABLE pessoa (
    id_pessoa SERIAL PRIMARY KEY NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    is_flamengo BOOLEAN NOT NULL,
    telefone VARCHAR(13) NOT NULL,
    cep VARCHAR(8),
    logradouro VARCHAR(150),
    numero VARCHAR(10),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2)
);

-- Cria a tabela paciente
-- atributos: ID(chave primária), número de convênio(chava candidata), alergias existentes e tipo sanguíneo
CREATE TABLE paciente (
    id_pessoa INTEGER PRIMARY KEY,
    numero_convenio VARCHAR(20) NOT NULL UNIQUE,
    tipo_sanguineo VARCHAR(3) NOT NULL
);

CREATE TABLE alergia (
    id_alergia SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    gravidade VARCHAR(20) not NULL
);

CREATE TABLE paciente_tem_alergia (
    id_paciente INTEGER NOT NULL,
    id_alergia INTEGER NOT NULL,
    
    PRIMARY KEY (id_paciente, id_alergia)
);

-- Cra a tabela profissiona
-- atributos: ID(chave primária), CRM(Chave candidadta), data de admissão e especialidade
CREATE TABLE profissional (
    id_pessoa INTEGER PRIMARY KEY,
    crm VARCHAR(20) NOT NULL UNIQUE,
    data_admissao DATE NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);

-- Cria a tabela preceptor
-- atrbiutos: ID_profissional(chave primária), titulação
CREATE TABLE preceptor (
    id_profissional INTEGER PRIMARY KEY,
    titulacao VARCHAR(50) NOT NULL
);

-- Cria a tabela residente
-- atributos: ID_profissional(chave primária) e ano de residência
CREATE TABLE residente (
    id_profissional INTEGER PRIMARY KEY,
    ano_residencia VARCHAR(2) NOT NULL
);

-- Cria a tabela unidade
-- atributos: id_unidade(chave primária), nome da unidade, tipo da unidade e capacidade de leitos
CREATE TABLE unidade (
    id_unidade SERIAL PRIMARY KEY NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    capacidade_leitos INTEGER NOT NULL,
    tempo_medio_espera_minutos NUMERIC(10,2) default 0
);

-- Cria a tabela de procedimento
-- atributos: id do procedimento(chave primária), codigo do procedimento, nome do procedimento e seu tempo médio em minutos
CREATE TABLE procedimento (
    id_procedimento SERIAL PRIMARY KEY,
    codigo VARCHAR(6) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    tempo_medio_minutos INTEGER NOT NULL,
    nivel_risco VARCHAR(20) DEFAULT 'BAIXO'
);

-- Cria a tabela de atendimento
CREATE TABLE atendimento (
    id_atendimento SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    duracao_minutos INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_residente INTEGER NOT NULL,
    id_preceptor INTEGER NOT NULL,
    id_unidade INTEGER not NULL
);

-- Cria a tabela de escala
CREATE TABLE escala (
    id_escala SERIAL PRIMARY KEY,
    id_unidade INTEGER NOT NULL,
    dia_semana VARCHAR(15) NOT NULL,
    turno VARCHAR(10) NOT NULL,
    id_residente INTEGER NOT NULL,
    id_preceptor INTEGER NOT NULL,
    dia_plantao INTEGER NOT NULL CHECK (dia_plantao BETWEEN 1 AND 31),
    mes_plantao INTEGER NOT NULL CHECK (mes_plantao BETWEEN 1 AND 12),
    ano_plantao INTEGER NOT NULL
);

-- Cria a tabela de procedimento realizado
CREATE TABLE procedimento_realizado (
    id_atendimento INTEGER NOT NULL,
    id_procedimento INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    tempo_real_minutos INTEGER NOT NULL,
    observacao VARCHAR(200) NOT NULL,
    is_faturado BOOLEAN DEFAULT FALSE,
    is_removido BOOLEAN DEFAULT FALSE,
    data_hora_inicio TIMESTAMP,
    PRIMARY KEY (id_atendimento, id_procedimento)
);

-- CRIA RELACIONAMENTOS
ALTER TABLE paciente ADD CONSTRAINT fk_paciente_pessoa FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa); -- Paciente é uma pessoa
ALTER TABLE profissional ADD CONSTRAINT fk_profissional_pessoa FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa); -- Profissional é uma pessoa
ALTER TABLE preceptor ADD CONSTRAINT fk_preceptor_profissional FOREIGN KEY (id_profissional) REFERENCES profissional(id_pessoa); -- Preceptor é um profissional
ALTER TABLE residente ADD CONSTRAINT fk_residente_profissional FOREIGN KEY (id_profissional) REFERENCES profissional(id_pessoa); -- Residente é um profissional

-- Estabelece relacionamentos da tabela de atendidmento
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_paciente FOREIGN KEY (id_paciente) REFERENCES paciente(id_pessoa);
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_residente FOREIGN KEY (id_residente) REFERENCES residente(id_profissional); 
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_preceptor FOREIGN KEY (id_preceptor) REFERENCES preceptor(id_profissional);
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_unidade FOREIGN KEY (id_unidade) REFERENCES unidade(id_unidade);

-- Estabelece relacionamentos da tabela de escala
ALTER TABLE escala ADD CONSTRAINT fk_escala_unidade FOREIGN KEY (id_unidade) REFERENCES unidade(id_unidade);
ALTER TABLE escala ADD CONSTRAINT fk_escala_residente FOREIGN KEY (id_residente) REFERENCES residente(id_profissional);
ALTER TABLE escala ADD CONSTRAINT fk_escala_preceptor FOREIGN KEY (id_preceptor) REFERENCES preceptor(id_profissional);

-- Estabelece relacionamentos da tabela de procedimento
ALTER TABLE procedimento_realizado ADD CONSTRAINT fk_procedimento_realizado_atendimento FOREIGN KEY (id_atendimento) REFERENCES atendimento(id_atendimento);
ALTER TABLE procedimento_realizado ADD CONSTRAINT fk_procedimento_realizado_procedimento FOREIGN KEY (id_procedimento) REFERENCES procedimento(id_procedimento);

alter table paciente_tem_alergia add CONSTRAINT fk_pta_paciente FOREIGN KEY (id_paciente) REFERENCES paciente(id_pessoa);
alter table paciente_tem_alergia add CONSTRAINT fk_pta_alergia FOREIGN KEY (id_alergia) REFERENCES alergia(id_alergia);