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


INSERT INTO ATENDIMENTO (id_atendimento, data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor, id_unidade) VALUES
(1, '2023-10-01 08:00:00', 45, 1, 6, 11, 1),
(2, '2023-10-01 09:30:00', 30, 2, 6, 11, 2),
(3, '2023-10-02 10:15:00', 60, 3, 6, 11, 3),
(4, '2023-10-02 14:00:00', 20, 4, 6, 11, 1),
(5, '2023-10-03 16:45:00', 90, 5, 7, 11, 2),
(6, '2023-10-04 07:30:00', 15, 1, 7, 11, 3),
(7, '2023-10-04 11:00:00', 120, 2, 7, 12, 1),
(8, '2023-10-05 13:20:00', 40, 3, 8, 12, 2),
(9, '2023-10-06 15:10:00', 25, 4, 8, 13, 3),
(10, '2023-10-07 18:00:00', 55, 5, 9, 13, 1),
(11, '2023-10-08 09:00:00', 30, 1, 10, 14, 2),
(12, '2023-10-09 10:00:00', 40, 2, 10, 14, 3),
(13, '2023-10-10 11:30:00', 20, 3, 10, 15, 1),
(14, '2023-10-11 14:20:00', 60, 4, 10, 15, 2),
(15, '2023-10-12 16:00:00', 45, 5, 10, 15, 3);


INSERT INTO PROCEDIMENTO_REALIZADO (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao, is_faturado, is_removido, data_hora_inicio) VALUES
(1, 5, 1, 35, 'Paciente colaborativo', FALSE, FALSE, '2023-10-01 08:15:00'),
(2, 1, 1, 25, 'Sutura leve', FALSE, FALSE, '2023-10-01 09:40:00'),
(3, 2, 1, 15, 'Coleta rápida', FALSE, FALSE, '2023-10-02 10:30:00'),
(4, 3, 1, 20, 'Aplicação de medicação IV (ALTO)', TRUE, FALSE, '2023-10-02 14:10:00'),
(5, 4, 1, 70, 'RCP (ALTO)', FALSE, FALSE, '2023-10-03 16:50:00'),
(6, 5, 1, 20, 'Avaliação ok', FALSE, FALSE, '2023-10-04 07:45:00'),
(7, 1, 2, 90, 'Sutura dupla', FALSE, FALSE, '2023-10-04 11:20:00'),
(8, 2, 1, 10, 'Acesso difícil', FALSE, FALSE, '2023-10-05 13:40:00'),
(9, 3, 1, 20, 'Medicação IV (ALTO)', FALSE, FALSE, '2023-10-06 15:25:00'),
(10, 4, 1, 60, 'RCP (ALTO)', FALSE, FALSE, '2023-10-07 18:15:00'),
(11, 5, 1, 30, 'Rotina', FALSE, FALSE, '2023-10-08 09:10:00'),
(12, 1, 1, 35, 'Sutura perna', FALSE, FALSE, '2023-10-09 10:20:00'),
(13, 2, 1, 12, 'Coleta dupla', FALSE, TRUE, '2023-10-10 11:35:00'),
(14, 3, 1, 18, 'Medicação (ALTO)', FALSE, FALSE, '2023-10-11 14:35:00'),
(15, 4, 1, 55, 'RCP (ALTO)', FALSE, FALSE, '2023-10-12 16:15:00');


INSERT INTO ESCALA (id_escala, id_unidade, dia_semana, turno, id_residente, id_preceptor, dia_plantao, mes_plantao, ano_plantao) VALUES
(1, 1, 'Segunda', 'Manhã', 6, 11, 01, 12, 2025),
(2, 2, 'Segunda', 'Tarde', 7, 12, 03, 09, 2025),
(3, 3, 'Terça', 'Noite', 8, 13, 11, 06, 2026),
-- Plantões adicionados no mês atual da execução (07/2026)
(4, 1, 'Segunda', 'Manhã', 6, 11, 06, 07, 2026),
(5, 2, 'Terça', 'Tarde', 7, 12, 07, 07, 2026),
(6, 1, 'Quarta', 'Noite', 6, 11, 08, 07, 2026),
(7, 3, 'Quinta', 'Manhã', 10, 15, 09, 07, 2026);

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
