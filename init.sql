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

CREATE TABLE pessoa (
    id_pessoa INTEGER PRIMARY KEY NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    is_flamengo BOOLEAN NOT NULL,
    telefone VARCHAR(13)NOT NULL
);

CREATE TABLE paciente (
    id_pessoa INTEGER PRIMARY KEY NOT NULL,
    numero_convenio VARCHAR(20) NOT NULL UNIQUE,
    alergias VARCHAR(100) NOT NULL,
    tipo_sanguineo VARCHAR(3) NOT NULL
);

CREATE TABLE profissional (
    id_pessoa INTEGER PRIMARY KEY NOT NULL,
    crm VARCHAR(20) NOT NULL UNIQUE,
    data_admissao DATE NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);

CREATE TABLE preceptor (
    id_profissional INTEGER PRIMARY KEY NOT NULL,
    titulacao VARCHAR(50) NOT NULL
);

CREATE TABLE residente (
    id_profissional INTEGER PRIMARY KEY NOT NULL,
    ano_residencia VARCHAR(2) NOT NULL
);

CREATE TABLE unidade (
    id_unidade INTEGER PRIMARY KEY NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    capacidade_leitos INTEGER NOT NULL
);

CREATE TABLE procedimento (
    id_procedimento INTEGER PRIMARY KEY NOT NULL,
    codigo VARCHAR(6) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    tempo_medio_minutos INTEGER NOT NULL
);

CREATE TABLE atendimento (
    id_atendimento INTEGER PRIMARY KEY NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    duracao_minutos INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_residente INTEGER NOT NULL,
    id_preceptor INTEGER NOT NULL
);

CREATE TABLE escala (
    id_escala INTEGER PRIMARY KEY NOT NULL,
    id_unidade INTEGER NOT NULL,
    dia_semana VARCHAR(15) NOT NULL,
    turno VARCHAR(10) NOT NULL,
    id_residente INTEGER NOT NULL,
    id_preceptor INTEGER NOT NULL
);

CREATE TABLE procedimento_realizado (
    id_atendimento INTEGER NOT NULL,
    id_procedimento INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    tempo_real_minutos INTEGER NOT NULL,
    observacao VARCHAR(200) NOT NULL,
    PRIMARY KEY (id_atendimento, id_procedimento)
);

ALTER TABLE paciente ADD CONSTRAINT fk_paciente_pessoa FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa);
ALTER TABLE profissional ADD CONSTRAINT fk_profissional_pessoa FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa);
ALTER TABLE preceptor ADD CONSTRAINT fk_preceptor_profissional FOREIGN KEY (id_profissional) REFERENCES profissional(id_pessoa);
ALTER TABLE residente ADD CONSTRAINT fk_residente_profissional FOREIGN KEY (id_profissional) REFERENCES profissional(id_pessoa);
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_paciente FOREIGN KEY (id_paciente) REFERENCES paciente(id_pessoa);
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_residente FOREIGN KEY (id_residente) REFERENCES residente(id_profissional);
ALTER TABLE atendimento ADD CONSTRAINT fk_atendimento_preceptor FOREIGN KEY (id_preceptor) REFERENCES preceptor(id_profissional);
ALTER TABLE escala ADD CONSTRAINT fk_escala_unidade FOREIGN KEY (id_unidade) REFERENCES unidade(id_unidade);
ALTER TABLE escala ADD CONSTRAINT fk_escala_residente FOREIGN KEY (id_residente) REFERENCES residente(id_profissional);
ALTER TABLE escala ADD CONSTRAINT fk_escala_preceptor FOREIGN KEY (id_preceptor) REFERENCES preceptor(id_profissional);
ALTER TABLE procedimento_realizado ADD CONSTRAINT fk_procedimento_realizado_atendimento FOREIGN KEY (id_atendimento) REFERENCES atendimento(id_atendimento);
ALTER TABLE procedimento_realizado ADD CONSTRAINT fk_procedimento_realizado_procedimento FOREIGN KEY (id_procedimento) REFERENCES procedimento(id_procedimento);


INSERT INTO PESSOA (id_pessoa, nome, CPF, data_nascimento, is_flamengo, telefone) VALUES
(1, 'Ana Clara', '11111111111', '1995-03-10', TRUE, '83999991111'),
(2, 'Bruno Mendes', '22222222222', '1988-07-21', FALSE, '83988882222'),
(3, 'Carlos Eduardo', '33333333333', '2001-11-05', TRUE, '83977773333'),
(4, 'Diana Silva', '44444444444', '1975-01-30', FALSE, '83966664444'),
(5, 'Evelyn Costa', '55555555555', '1999-09-15', TRUE, '83955555555');


INSERT INTO PESSOA (id_pessoa, nome, CPF, data_nascimento, is_flamengo, telefone) VALUES
(6, 'Dr. Felipe Souza', '66666666666', '1994-02-20', FALSE, '83944446666'),
(7, 'Dra. Gabriela Nunes', '77777777777', '1993-06-12', TRUE, '83933337777'),
(8, 'Dr. Henrique Lima', '88888888888', '1995-10-08', FALSE, '83922228888'),
(9, 'Dra. Isabela Rocha', '99999999999', '1992-12-25', TRUE, '83911119999'),
(10, 'Dr. João Pedro', '10101010101', '1996-04-18', FALSE, '83900001010');


INSERT INTO PESSOA (id_pessoa, nome, CPF, data_nascimento, is_flamengo, telefone) VALUES
(11, 'Dra. Karen Dias', '12121212121', '1980-05-11', TRUE, '83999991212'),
(12, 'Dr. Leonardo Melo', '13131313131', '1978-08-30', FALSE, '83988881313'),
(13, 'Dra. Mariana Farias', '14141414141', '1982-11-22', TRUE, '83977771414'),
(14, 'Dr. Nilton Cezar', '15151515151', '1975-02-14', FALSE, '83966661515'),
(15, 'Dra. Olivia Martins', '16161616161', '1985-09-07', TRUE, '83955551616');

INSERT INTO PACIENTE (id_pessoa, numero_convenio, alergias, tipo_sanguineo) VALUES
(1, 'CONV1001', 'Nenhuma', 'O+'),
(2, 'CONV1002', 'Dipirona', 'A+'),
(3, 'CONV1003', 'Amendoim', 'B-'),
(4, 'CONV1004', 'Nenhuma', 'AB+'),
(5, 'CONV1005', 'Frutos do mar', 'O-');

INSERT INTO PROFISSIONAL (id_pessoa, CRM, data_admissao, especialidade) VALUES
(6, 'CRM1001', '2023-03-01', 'Clínica Médica'),
(7, 'CRM1002', '2023-03-01', 'Pediatria'),
(8, 'CRM1003', '2022-03-01', 'Cirurgia Geral'),
(9, 'CRM1004', '2024-03-01', 'Ginecologia'),
(10, 'CRM1005', '2023-03-01', 'Ortopedia'),
(11, 'CRM2001', '2015-01-10', 'Clínica Médica'),
(12, 'CRM2002', '2012-05-20', 'Pediatria'),
(13, 'CRM2003', '2018-07-15', 'Cirurgia Geral'),
(14, 'CRM2004', '2010-09-01', 'Ginecologia'),
(15, 'CRM2005', '2016-11-11', 'Ortopedia');

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

INSERT INTO PROCEDIMENTO (id_procedimento, codigo, nome, tempo_medio_minutos) VALUES
(1, 'PROC01', 'Sutura simples', 20),
(2, 'PROC02', 'Coleta de sangue', 10),
(3, 'PROC03', 'Aplicação de medicação IV', 15),
(4, 'PROC04', 'Ressuscitação Cardiopulmonar', 60),
(5, 'PROC05', 'Avaliação Clínica Básica', 30);

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

INSERT INTO PROCEDIMENTO_REALIZADO (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao) VALUES
(1, 5, 1, 35, 'Paciente colaborativo'),
(1, 2, 1, 10, 'Acesso venoso difícil'),
(2, 5, 1, 30, 'Sem intercorrências'),
(3, 1, 2, 60, 'Sutura extensa no braço'),
(4, 3, 1, 20, 'Aplicação de antibiótico'),
(5, 4, 1, 90, 'Manobra com sucesso após 1h'),
(6, 2, 2, 15, 'Duas amostras coletadas'),
(7, 1, 1, 120, 'Cirurgia ambulatorial complexa'),
(8, 5, 1, 40, 'Revisão de exames'),
(9, 3, 1, 25, 'Medicação analgésica'),
(10, 5, 1, 55, 'Paciente apresentou leve febre');

INSERT INTO ESCALA (id_escala, id_unidade, dia_semana, turno, id_residente, id_preceptor) VALUES
(1, 1, 'Segunda', 'Manhã', 6, 11),
(2, 2, 'Segunda', 'Tarde', 7, 12),
(3, 3, 'Terça', 'Noite', 8, 13);
