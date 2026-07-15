-- Remove as tabelas existentes para evitar conflitos durante a criação
DROP TABLE IF EXISTS procedimento_realizado CASCADE;
DROP TABLE IF EXISTS escala CASCADE;
DROP TABLE IF EXISTS atendimento CASCADE;
DROP TABLE IF EXISTS procedimento CASCADE;
DROP TABLE IF EXISTS unidade CASCADE;
DROP TABLE IF EXISTS residente CASCADE;
DROP TABLE IF EXISTS preceptor CASCADE;
DROP TABLE IF EXISTS profissional CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS pessoa CASCADE;
drop table if exists alergia cascade;
drop table if exists paciente_tem_alergia cascade;

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
    gravidade VARCHAR(20) not null
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
    capacidade_leitos INTEGER NOT NULL
);

-- Cria a tabela de procedimento
-- atributos: id do procedimento(chave primária), codigo do procedimento, nome do procedimento e seu tempo médio em minutos
CREATE TABLE procedimento (
    id_procedimento SERIAL PRIMARY KEY,
    codigo VARCHAR(6) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    tempo_medio_minutos INTEGER NOT null,
    nivel_risco VARCHAR(20) DEFAULT 'BAIXO'
);

-- Cria a tabela de atendimento
CREATE TABLE atendimento (
    id_atendimento SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    duracao_minutos INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_residente INTEGER NOT NULL,
    id_preceptor INTEGER NOT NULL
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

-- Estabelece relacionamentos da tabela de escala
ALTER TABLE escala ADD CONSTRAINT fk_escala_unidade FOREIGN KEY (id_unidade) REFERENCES unidade(id_unidade);
ALTER TABLE escala ADD CONSTRAINT fk_escala_residente FOREIGN KEY (id_residente) REFERENCES residente(id_profissional);
ALTER TABLE escala ADD CONSTRAINT fk_escala_preceptor FOREIGN KEY (id_preceptor) REFERENCES preceptor(id_profissional);

-- Estabelece relacionamentos da tabela de procedimento
ALTER TABLE procedimento_realizado ADD CONSTRAINT fk_procedimento_realizado_atendimento FOREIGN KEY (id_atendimento) REFERENCES atendimento(id_atendimento);
ALTER TABLE procedimento_realizado ADD CONSTRAINT fk_procedimento_realizado_procedimento FOREIGN KEY (id_procedimento) REFERENCES procedimento(id_procedimento);

alter table paciente_tem_alergia add CONSTRAINT fk_pta_paciente FOREIGN KEY (id_paciente) REFERENCES paciente(id_pessoa);
alter table paciente_tem_alergia add CONSTRAINT fk_pta_alergia FOREIGN KEY (id_alergia) REFERENCES alergia(id_alergia);

-- POPULA AS TABELAS
INSERT INTO pessoa (id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone, cep, logradouro, numero, complemento, bairro, cidade, uf) VALUES
(1, 'Ana Clara', '00000000191', '1995-03-10', TRUE, '83999991111', '58000001', 'Rua das Flores', '123', 'Apt 101', 'Centro', 'João Pessoa', 'PB'),
(2, 'Bruno Mendes', '00000000272', '1988-07-21', FALSE, '83988882222', '58000002', 'Av. Epitácio Pessoa', '456', '', 'Tambaú', 'João Pessoa', 'PB'),
(3, 'Carlos Eduardo', '00000000353', '2001-11-05', TRUE, '83977773333', '58000003', 'Rua Bancário', '789', 'Casa B', 'Bancários', 'João Pessoa', 'PB'),
(4, 'Diana Silva', '00000000434', '1975-01-30', FALSE, '83966664444', '58000004', 'Av. Ruy Carneiro', '101', '', 'Manaíra', 'João Pessoa', 'PB'),
(5, 'Evelyn Costa', '00000000515', '1999-09-15', TRUE, '83955555555', '58000005', 'Rua da Praia', '202', 'Bloco C', 'Cabo Branco', 'João Pessoa', 'PB');

INSERT INTO pessoa (id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone, cep, logradouro, numero, complemento, bairro, cidade, uf) VALUES
(6, 'Dr. Felipe Souza', '00000000604', '1994-02-20', FALSE, '83944446666', '58000006', 'Rua das Acácias', '303', '', 'Bessa', 'João Pessoa', 'PB'),
(7, 'Dra. Gabriela Nunes', '00000000787', '1993-06-12', TRUE, '83933337777', '58000007', 'Rua dos Ipês', '404', 'Apt 202', 'Castelo Branco', 'João Pessoa', 'PB'),
(8, 'Dr. Henrique Lima', '00000000868', '1995-10-08', FALSE, '83922228888', '58000008', 'Av. João Maurício', '505', '', 'Manaíra', 'João Pessoa', 'PB'),
(9, 'Dra. Isabela Rocha', '00000000949', '1992-12-25', TRUE, '83911119999', '58000009', 'Rua Flamboyant', '606', 'Casa', 'Altiplano', 'João Pessoa', 'PB'),
(10, 'Dr. João Pedro', '00000001082', '1996-04-18', FALSE, '83900001010', '58000010', 'Rua das Palmeiras', '707', '', 'Miramar', 'João Pessoa', 'PB');

INSERT INTO pessoa (id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone, cep, logradouro, numero, complemento, bairro, cidade, uf) VALUES
(11, 'Dra. Karen Dias', '00000001163', '1980-05-11', TRUE, '83999991212', '58000011', 'Av. Beira Mar', '808', 'Cobertura', 'Cabo Branco', 'João Pessoa', 'PB'),
(12, 'Dr. Leonardo Melo', '00000001244', '1978-08-30', FALSE, '83988881313', '58000012', 'Rua do Sol', '909', '', 'Tambaú', 'João Pessoa', 'PB'),
(13, 'Dra. Mariana Farias', '00000001325', '1982-11-22', TRUE, '83977771414', '58000013', 'Rua da Lua', '100', 'Apt 505', 'Bessa', 'João Pessoa', 'PB'),
(14, 'Dr. Nilton Cezar', '00000001406', '1975-02-14', FALSE, '83966661515', '58000014', 'Av. das Estrelas', '200', '', 'Intermares', 'Cabedelo', 'PB'),
(15, 'Dra. Olivia Martins', '00000001597', '1985-09-07', TRUE, '83955551616', '58000015', 'Rua Oceano', '300', 'Casa de Esquina', 'Poço', 'Cabedelo', 'PB');

INSERT INTO PACIENTE (id_pessoa, numero_convenio, tipo_sanguineo) VALUES
(1, 'CONV1001', 'O+'),
(2, 'CONV1002', 'A+'),
(3, 'CONV1003', 'B-'),
(4, 'CONV1004', 'AB+'),
(5, 'CONV1005', 'O-');

INSERT INTO alergia (id_alergia, nome, gravidade) VALUES
(1, 'Dipirona', 'Moderada'),
(2, 'Amendoim', 'Grave'),
(3, 'Frutos do mar', 'Grave'),
(4, 'Lactose', 'Leve'),
(5, 'Ibuprofeno', 'Moderada');

INSERT INTO paciente_tem_alergia (id_paciente, id_alergia) VALUES
(2, 1),
(3, 2),
(5, 3),
(5, 4);

INSERT INTO PROFISSIONAL (id_pessoa, CRM, data_admissao, especialidade) VALUES
(6, '03212/PB', '2023-03-01', 'Clínica Médica'),
(7, '02345/PB', '2023-03-01', 'Pediatria'),
(8, '002345/PB', '2022-03-01', 'Cirurgia Geral'),
(9, '02344/PB', '2024-03-01', 'Ginecologia'),
(10, '01205/PB', '2023-03-01', 'Ortopedia'),
(11, '01106/PB', '2015-01-10', 'Clínica Médica'),
(12, '0807/PB', '2012-05-20', 'Pediatria'),
(13, '0108/PB', '2018-07-15', 'Cirurgia Geral'),
(14, '0309/PB', '2010-09-01', 'Ginecologia'),
(15, '1010/PB', '2016-11-11', 'Ortopedia');

INSERT INTO RESIDENTE (id_profissional, ano_residencia) VALUES
(6, 'R2'),
(7, 'R2'),
(8, 'R3'),
(9, 'R1'),
(10, 'R2');

INSERT INTO PRECEPTOR (id_profissional, titulacao) VALUES
(11, 'Doutor'),
(12, 'Mestre'),
(13, 'Doutor'),
(14, 'Especialista'),
(15, 'Mestre');

INSERT INTO UNIDADE (id_unidade, nome, tipo, capacidade_leitos) VALUES
(1, 'Enfermaria Ala Sul', 'Enfermaria', 50),
(2, 'UTI Adulto', 'UTI', 20),
(3, 'Pronto-Socorro Principal', 'Pronto-Socorro', 30);

INSERT INTO PROCEDIMENTO (id_procedimento, codigo, nome, tempo_medio_minutos, nivel_risco) VALUES
(1, 'PROC01', 'Sutura simples', 20, 'BAIXO'),
(2, 'PROC02', 'Coleta de sangue', 10, 'BAIXO'),
(3, 'PROC03', 'Aplicação de medicação IV', 15, 'ALTO'),
(4, 'PROC04', 'Ressuscitação Cardiopulmonar', 60, 'ALTO'),
(5, 'PROC05', 'Avaliação Clínica Básica', 30, 'BAIXO');

INSERT INTO ATENDIMENTO (id_atendimento, data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor) VALUES
(1, '2023-10-01 08:00:00', 45, 1, 6, 11),
(2, '2023-10-01 09:30:00', 30, 2, 7, 12),
(3, '2023-10-02 10:15:00', 60, 3, 8, 13),
(4, '2023-10-02 14:00:00', 20, 4, 9, 14),
(5, '2023-10-03 16:45:00', 90, 5, 10, 15),
(6, '2023-10-04 07:30:00', 15, 1, 7, 12),
(7, '2023-10-04 11:00:00', 120, 2, 8, 13),
(8, '2023-10-05 13:20:00', 40, 3, 6, 11),
(9, '2023-10-06 15:10:00', 25, 4, 10, 15),
(10, '2023-10-07 18:00:00', 55, 5, 9, 14);

INSERT INTO PROCEDIMENTO_REALIZADO (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao, is_faturado, is_removido) values

-- Procedimentos normais (Ainda não faturados, não removidos)
(1, 5, 1, 35, 'Paciente colaborativo', FALSE, FALSE),
(2, 5, 1, 30, 'Sem intercorrências', FALSE, FALSE),
(3, 1, 2, 60, 'Sutura extensa no braço', FALSE, FALSE),
(6, 2, 2, 15, 'Duas amostras coletadas', FALSE, FALSE),
(7, 1, 1, 120, 'Cirurgia ambulatorial complexa', FALSE, FALSE),
(8, 5, 1, 40, 'Revisão de exames', FALSE, FALSE),
(9, 3, 1, 25, 'Medicação analgésica', FALSE, FALSE),
(10, 5, 1, 55, 'Paciente apresentou leve febre', FALSE, FALSE),

-- Procedimento já faturado
(1, 2, 1, 10, 'Acesso venoso difícil', TRUE, FALSE),
(5, 4, 1, 90, 'Manobra com sucesso após 1h', TRUE, FALSE),

-- Exclusão Lógica
(4, 3, 1, 20, 'Aplicação de antibiótico inserida por engano', FALSE, TRUE);

INSERT INTO ESCALA (id_escala, id_unidade, dia_semana, turno, id_residente, id_preceptor) VALUES
(1, 1, 'Segunda', 'Manhã', 6, 11),
(2, 2, 'Segunda', 'Tarde', 7, 12),
(3, 3, 'Terça', 'Noite', 8, 13);

-- Sincroniza o contador automático das tabelas com o maior ID que já existe na tabela
SELECT setval(pg_get_serial_sequence('pessoa', 'id_pessoa'), max(id_pessoa))
FROM pessoa;

SELECT setval(pg_get_serial_sequence('atendimento', 'id_atendimento'), max(id_atendimento))
FROM atendimento;

SELECT setval(pg_get_serial_sequence('procedimento', 'id_procedimento'), max(id_procedimento))
FROM procedimento;

SELECT setval(pg_get_serial_sequence('escala', 'id_escala'), max(id_escala))
FROM escala;

SELECT setval(pg_get_serial_sequence('unidade', 'id_unidade'), max(id_unidade))
FROM unidade;

SELECT setval(pg_get_serial_sequence('alergia', 'id_alergia'), max(id_alergia)) 
FROM alergia;
