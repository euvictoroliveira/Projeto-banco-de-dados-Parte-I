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

INSERT INTO pessoa (id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone, cep, logradouro, numero, complemento, bairro, cidade, uf) VALUES
(16, 'Fernanda Alves', '00000001678', '1990-01-12', FALSE, '83999992001', '58010001', 'Rua Maceió', '11', '', 'Jaguaribe', 'João Pessoa', 'PB'),
(17, 'Gustavo Ramos', '00000001759', '1985-05-23', TRUE, '83999992002', '58010002', 'Rua Natal', '22', 'Apt 12', 'Torre', 'João Pessoa', 'PB'),
(18, 'Helena Torres', '00000001830', '2003-08-02', FALSE, '83999992003', '58010003', 'Rua Recife', '33', '', 'Cristo Redentor', 'João Pessoa', 'PB'),
(19, 'Igor Barbosa', '00000001910', '1998-12-19', TRUE, '83999992004', '58010004', 'Rua Aracaju', '44', 'Casa', 'Valentina', 'João Pessoa', 'PB'),
(20, 'Juliana Prado', '00000002054', '1979-03-27', FALSE, '83999992005', '58010005', 'Rua Salvador', '55', '', 'Mangabeira', 'João Pessoa', 'PB'),
(21, 'Kleber Nogueira', '00000002135', '1966-11-09', TRUE, '83999992006', '58010006', 'Rua Fortaleza', '66', 'Fundos', 'Cristo', 'João Pessoa', 'PB'),
(22, 'Larissa Vidal', '00000002216', '2010-06-14', FALSE, '83999992007', '58010007', 'Rua Teresina', '77', '', 'Ernesto Geisel', 'João Pessoa', 'PB'),
(23, 'Marcelo Tavares', '00000002305', '1972-09-30', TRUE, '83999992008', '58010008', 'Rua São Luís', '88', 'Bloco A', 'Água Fria', 'João Pessoa', 'PB'),
(24, 'Natália Duarte', '00000002488', '1994-04-04', FALSE, '83999992009', '58010009', 'Rua Belém', '99', '', 'Funcionários', 'João Pessoa', 'PB'),
(25, 'Otávio Guedes', '00000002569', '1958-07-17', TRUE, '83999992010', '58010010', 'Rua Vitória', '110', 'Casa 2', 'Geisel', 'João Pessoa', 'PB');

INSERT INTO pessoa (id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone, cep, logradouro, numero, complemento, bairro, cidade, uf) VALUES
(26, 'Dr. Paulo Cesar', '00000002640', '1997-01-15', FALSE, '83999993001', '58020001', 'Rua Aurora', '12', '', 'Bancários', 'João Pessoa', 'PB'),
(27, 'Dra. Renata Silveira', '00000002720', '1996-03-21', TRUE, '83999993002', '58020002', 'Rua Cometa', '23', 'Apt 3', 'Bessa', 'João Pessoa', 'PB'),
(28, 'Dr. Samuel Cordeiro', '00000002801', '1995-07-08', FALSE, '83999993003', '58020003', 'Rua Nébula', '34', '', 'Miramar', 'João Pessoa', 'PB'),
(29, 'Dra. Tatiana Freire', '00000002992', '1998-10-02', TRUE, '83999993004', '58020004', 'Rua Órion', '45', 'Casa', 'Manaíra', 'João Pessoa', 'PB'),
(30, 'Dr. Ulisses Andrade', '00000003026', '1994-12-30', FALSE, '83999993005', '58020005', 'Rua Vega', '56', '', 'Tambauzinho', 'João Pessoa', 'PB'),
(31, 'Dra. Vanessa Cunha', '00000003107', '1997-05-19', TRUE, '83999993006', '58020006', 'Rua Sirius', '67', 'Apt 8', 'Expedicionários', 'João Pessoa', 'PB'),
(32, 'Dr. Wagner Lopes', '00000003298', '1996-08-24', FALSE, '83999993007', '58020007', 'Rua Netuno', '78', '', 'Jardim Oceania', 'João Pessoa', 'PB'),
(33, 'Dra. Ximena Rocha', '00000003379', '1995-02-11', TRUE, '83999993008', '58020008', 'Rua Marte', '89', 'Casa 3', 'Cabo Branco', 'João Pessoa', 'PB');

INSERT INTO pessoa (id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone, cep, logradouro, numero, complemento, bairro, cidade, uf) VALUES
(34, 'Dr. Yuri Castelo', '00000003450', '1974-06-13', FALSE, '83999994001', '58030001', 'Av. Litorânea', '210', '', 'Cabo Branco', 'João Pessoa', 'PB'),
(35, 'Dra. Zilda Monteiro', '00000003530', '1970-09-28', TRUE, '83999994002', '58030002', 'Av. Cabo Branco', '220', 'Cobertura', 'Cabo Branco', 'João Pessoa', 'PB'),
(36, 'Dr. André Peixoto', '00000003611', '1983-01-05', FALSE, '83999994003', '58030003', 'Rua dos Coqueiros', '230', '', 'Tambaú', 'João Pessoa', 'PB'),
(37, 'Dra. Bianca Sales', '00000003700', '1979-04-17', TRUE, '83999994004', '58030004', 'Rua das Gaivotas', '240', 'Apt 14', 'Manaíra', 'João Pessoa', 'PB'),
(38, 'Dr. Cauã Meireles', '00000003883', '1976-11-24', FALSE, '83999994005', '58030005', 'Rua do Horizonte', '250', '', 'Bessa', 'João Pessoa', 'PB'),
(39, 'Dra. Debora Aquino', '00000003964', '1981-02-08', TRUE, '83999994006', '58030006', 'Rua Aurora Boreal', '260', 'Casa', 'Altiplano', 'João Pessoa', 'PB'),
(40, 'Dr. Emerson Vale', '00000004006', '1977-07-22', FALSE, '83999994007', '58030007', 'Rua das Marés', '270', '', 'Miramar', 'João Pessoa', 'PB');

INSERT INTO PACIENTE (id_pessoa, numero_convenio, tipo_sanguineo) VALUES
(1, 'CONV1001', 'O+'),
(2, 'CONV1002', 'A+'),
(3, 'CONV1003', 'B-'),
(4, 'CONV1004', 'AB+'),
(5, 'CONV1005', 'O-');

INSERT INTO PACIENTE (id_pessoa, numero_convenio, tipo_sanguineo) VALUES
(16, 'CONV1006', 'A-'),
(17, 'CONV1007', 'B+'),
(18, 'CONV1008', 'O+'),
(19, 'CONV1009', 'AB-'),
(20, 'CONV1010', 'O+'),
(21, 'CONV1011', 'A+'),
(22, 'CONV1012', 'B-'),
(23, 'CONV1013', 'O-'),
(24, 'CONV1014', 'AB+'),
(25, 'CONV1015', 'A+');

INSERT INTO alergia (id_alergia, nome, gravidade) VALUES
(1, 'Dipirona', 'Moderada'),
(2, 'Amendoim', 'Grave'),
(3, 'Frutos do mar', 'Grave'),
(4, 'Lactose', 'Leve'),
(5, 'Ibuprofeno', 'Moderada'),
(6, 'Penicilina', 'Grave'),
(7, 'Látex', 'Moderada'),
(8, 'Poeira', 'Leve'),
(9, 'Pólen', 'Leve'),
(10, 'Sulfa', 'Grave'),
(11, 'Corante alimentar', 'Leve'),
(12, 'Picada de inseto', 'Moderada');

INSERT INTO paciente_tem_alergia (id_paciente, id_alergia) VALUES
(2, 1),
(3, 2),
(5, 3),
(5, 4),
(16, 6),
(17, 7),
(18, 8),
(19, 9),
(20, 10),
(21, 1),
(22, 11),
(23, 12),
(24, 2),
(25, 4);

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

INSERT INTO PROFISSIONAL (id_pessoa, CRM, data_admissao, especialidade) VALUES
(26, '04512/PB', '2024-03-01', 'Clínica Médica'),
(27, '04513/PB', '2024-03-01', 'Pediatria'),
(28, '04514/PB', '2023-03-01', 'Cirurgia Geral'),
(29, '04515/PB', '2025-03-01', 'Ginecologia'),
(30, '04516/PB', '2024-03-01', 'Ortopedia'),
(31, '04517/PB', '2025-03-01', 'Neurologia'),
(32, '04518/PB', '2023-03-01', 'Cardiologia'),
(33, '04519/PB', '2025-03-01', 'Clínica Médica');

INSERT INTO PROFISSIONAL (id_pessoa, CRM, data_admissao, especialidade) VALUES
(34, '02011/PB', '2008-02-15', 'Neurologia'),
(35, '01512/PB', '2005-06-10', 'Cardiologia'),
(36, '03013/PB', '2014-08-20', 'Clínica Médica'),
(37, '02514/PB', '2011-04-05', 'Pediatria'),
(38, '03515/PB', '2017-09-12', 'Cirurgia Geral'),
(39, '02016/PB', '2009-01-25', 'Ginecologia'),
(40, '03517/PB', '2019-10-30', 'Ortopedia');

INSERT INTO RESIDENTE (id_profissional, ano_residencia) VALUES
(6, 'R2'),
(7, 'R2'),
(8, 'R3'),
(9, 'R1'),
(10, 'R2');

INSERT INTO RESIDENTE (id_profissional, ano_residencia) VALUES
(26, 'R1'),
(27, 'R1'),
(28, 'R2'),
(29, 'R3'),
(30, 'R1'),
(31, 'R2'),
(32, 'R3'),
(33, 'R1');

INSERT INTO PRECEPTOR (id_profissional, titulacao) VALUES
(11, 'Doutor'),
(12, 'Mestre'),
(13, 'Doutor'),
(14, 'Especialista'),
(15, 'Mestre');

INSERT INTO PRECEPTOR (id_profissional, titulacao) VALUES
(34, 'Doutor'),
(35, 'Doutor'),
(36, 'Mestre'),
(37, 'Especialista'),
(38, 'Mestre'),
(39, 'Doutor'),
(40, 'Especialista');

INSERT INTO UNIDADE (id_unidade, nome, tipo, capacidade_leitos) VALUES
(1, 'Enfermaria Ala Sul', 'Enfermaria', 50),
(2, 'UTI Adulto', 'UTI', 20),
(3, 'Pronto-Socorro Principal', 'Pronto-Socorro', 30);

INSERT INTO UNIDADE (id_unidade, nome, tipo, capacidade_leitos) VALUES
(4, 'UTI Pediátrica', 'UTI', 12),
(5, 'Enfermaria Ala Norte', 'Enfermaria', 40),
(6, 'Centro Cirúrgico', 'Centro Cirúrgico', 8),
(7, 'Ambulatório Geral', 'Ambulatório', 25);

INSERT INTO PROCEDIMENTO (id_procedimento, codigo, nome, tempo_medio_minutos, nivel_risco) VALUES
(1, 'PROC01', 'Sutura simples', 20, 'BAIXO'),
(2, 'PROC02', 'Coleta de sangue', 10, 'BAIXO'),
(3, 'PROC03', 'Aplicação de medicação IV', 15, 'ALTO'),
(4, 'PROC04', 'Ressuscitação Cardiopulmonar', 60, 'ALTO'),
(5, 'PROC05', 'Avaliação Clínica Básica', 30, 'BAIXO');

INSERT INTO PROCEDIMENTO (id_procedimento, codigo, nome, tempo_medio_minutos, nivel_risco) VALUES
(6, 'PROC06', 'Intubação orotraqueal', 25, 'ALTO'),
(7, 'PROC07', 'Curativo simples', 15, 'BAIXO'),
(8, 'PROC08', 'Raio-X', 20, 'BAIXO'),
(9, 'PROC09', 'Eletrocardiograma', 15, 'BAIXO'),
(10, 'PROC10', 'Drenagem torácica', 40, 'ALTO'),
(11, 'PROC11', 'Biópsia', 35, 'ALTO'),
(12, 'PROC12', 'Nebulização', 20, 'BAIXO');

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

INSERT INTO ATENDIMENTO (id_atendimento, data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor, id_unidade) VALUES
(16, '2024-02-14 08:30:00', 35, 16, 26, 34, 4),
(17, '2024-05-20 10:00:00', 50, 17, 27, 35, 5),
(18, '2024-08-09 13:45:00', 25, 18, 28, 36, 6),
(19, '2024-11-03 09:15:00', 40, 19, 29, 37, 7),
(20, '2025-01-18 15:00:00', 60, 20, 30, 38, 1),
(21, '2025-03-22 11:20:00', 20, 21, 31, 39, 2),
(22, '2025-06-30 16:40:00', 45, 22, 32, 40, 3),
(23, '2025-09-12 08:00:00', 30, 23, 33, 34, 4),
(24, '2025-12-05 14:10:00', 55, 24, 26, 35, 5),
(25, '2026-02-08 10:30:00', 25, 25, 27, 36, 6),
(26, '2026-05-17 09:45:00', 35, 1, 28, 37, 7),
(27, '2026-07-15 13:00:00', 40, 2, 29, 38, 1),
(28, '2026-07-28 16:20:00', 50, 16, 30, 39, 2),
(29, '2026-08-01 08:10:00', 20, 17, 31, 40, 3),
(30, '2026-08-03 07:50:00', 30, 18, 32, 34, 4),
(31, '2026-08-03 09:00:00', 35, 19, 33, 39, 5),
(32, '2026-08-03 11:00:00', 30, 21, 26, 34, 1);

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
(15, 4, 1, 55, 'RCP (ALTO)', FALSE, FALSE, '2023-10-12 16:15:00'),
(16, 6, 1, 22, 'Intubação bem sucedida (ALTO)', FALSE, FALSE, '2024-02-14 08:40:00'),
(17, 7, 1, 12, 'Curativo trocado', FALSE, FALSE, '2024-05-20 10:10:00'),
(18, 8, 1, 18, 'Raio-X de tórax', FALSE, FALSE, '2024-08-09 13:55:00'),
(19, 9, 1, 14, 'ECG de rotina', FALSE, FALSE, '2024-11-03 09:25:00'),
(20, 10, 1, 45, 'Drenagem torácica (ALTO)', TRUE, FALSE, '2025-01-18 15:15:00'),
(21, 11, 1, 38, 'Biópsia de pele (ALTO)', FALSE, FALSE, '2025-03-22 11:30:00'),
(22, 12, 2, 25, 'Nebulização dupla', FALSE, FALSE, '2025-06-30 16:50:00'),
(23, 5, 1, 28, 'Avaliação clínica geral', FALSE, FALSE, '2025-09-12 08:10:00'),
(24, 6, 1, 24, 'Intubação de emergência (ALTO)', FALSE, FALSE, '2025-12-05 14:20:00'),
(25, 2, 1, 9, 'Coleta simples', FALSE, FALSE, '2026-02-08 10:40:00'),
(26, 1, 1, 22, 'Sutura no braço', FALSE, FALSE, '2026-05-17 09:55:00'),
(27, 9, 1, 16, 'ECG pré-operatório', FALSE, FALSE, '2026-07-15 13:10:00'),
(28, 3, 1, 17, 'Medicação IV (ALTO)', FALSE, FALSE, '2026-07-28 16:30:00'),
(29, 7, 1, 11, 'Curativo pós-procedimento', FALSE, FALSE, '2026-08-01 08:20:00'),
(30, 4, 1, 58, 'RCP (ALTO)', FALSE, FALSE, '2026-08-03 08:00:00'),
(31, 5, 1, 33, 'Avaliação clínica de rotina', FALSE, FALSE, '2026-08-03 09:10:00'),
(32, 2, 1, 12, 'Coleta de rotina', FALSE, FALSE, '2026-08-03 11:10:00');

INSERT INTO ESCALA (id_escala, id_unidade, dia_semana, turno, id_residente, id_preceptor) VALUES
(1, 1, 'Segunda', 'Manhã', 6, 11),
(2, 2, 'Segunda', 'Tarde', 7, 12),
(3, 3, 'Terça', 'Noite', 8, 13),
(4, 1, 'Segunda', 'Tarde', 6, 11),
(5, 2, 'Terça', 'Tarde', 7, 12),
(6, 1, 'Quarta', 'Noite', 6, 11),
(7, 3, 'Quinta', 'Manhã', 10, 15);

INSERT INTO ESCALA (id_escala, id_unidade, dia_semana, turno, id_residente, id_preceptor) VALUES
(8, 4, 'Segunda', 'Manhã', 26, 34),
(9, 5, 'Segunda', 'Tarde', 27, 35),
(10, 6, 'Terça', 'Manhã', 28, 36),
(11, 7, 'Terça', 'Tarde', 29, 37),
(12, 1, 'Quarta', 'Manhã', 30, 38),
(13, 2, 'Quarta', 'Tarde', 31, 39),
(14, 3, 'Quinta', 'Tarde', 32, 40),
(15, 4, 'Quinta', 'Noite', 33, 34),
(16, 5, 'Sexta', 'Manhã', 26, 35),
(17, 6, 'Sexta', 'Tarde', 27, 36),
(18, 7, 'Sexta', 'Noite', 28, 37),
(19, 2, 'Segunda', 'Noite', 29, 38),
(20, 3, 'Quarta', 'Manhã', 9, 14);

INSERT INTO internacao (id_paciente, id_unidade, data_hora_entrada, data_hora_saida) 
VALUES (1, 2, '2023-10-01 08:00:00', '2023-10-15 14:30:00');

-- Internação ATIVA (Paciente ainda está no hospital)
INSERT INTO internacao (id_paciente, id_unidade, data_hora_entrada, data_hora_saida) 
VALUES (2, 3, '2023-11-20 09:15:00', NULL);

INSERT INTO internacao (id_paciente, id_unidade, data_hora_entrada, data_hora_saida) VALUES
(16, 4, '2024-02-14 09:00:00', '2024-02-20 11:00:00'),
(17, 5, '2024-05-20 10:30:00', '2024-05-25 09:00:00'),
(18, 6, '2024-08-09 14:00:00', '2024-08-11 08:30:00'),
(19, 7, '2024-11-03 09:30:00', '2024-11-06 12:00:00'),
(20, 1, '2025-01-18 15:30:00', NULL),
(21, 2, '2025-03-22 11:40:00', '2025-03-30 10:00:00'),
(3, 3, '2025-06-30 17:00:00', NULL),
(22, 4, '2025-09-12 08:20:00', '2025-09-18 16:00:00'),
(23, 5, '2026-07-20 10:00:00', NULL),
(24, 6, '2026-08-02 09:00:00', NULL);

INSERT INTO auditoria_atendimento (id_atendimento, operacao, usuario_bd, data_hora, dados_antigos, dados_novos) VALUES
(30, 'INSERT', 'postgres', '2026-08-03 07:50:00',
    NULL,
    '{"id_atendimento":30,"data_hora":"2026-08-03T07:50:00","duracao_minutos":30,"id_paciente":18,"id_residente":32,"id_preceptor":34,"id_unidade":4}'::jsonb),
(31, 'INSERT', 'postgres', '2026-08-03 09:00:00',
    NULL,
    '{"id_atendimento":31,"data_hora":"2026-08-03T09:00:00","duracao_minutos":20,"id_paciente":19,"id_residente":33,"id_preceptor":39,"id_unidade":5}'::jsonb),
(31, 'UPDATE', 'postgres', '2026-08-03 09:05:00',
    '{"id_atendimento":31,"data_hora":"2026-08-03T09:00:00","duracao_minutos":20,"id_paciente":19,"id_residente":33,"id_preceptor":39,"id_unidade":5}'::jsonb,
    '{"id_atendimento":31,"data_hora":"2026-08-03T09:00:00","duracao_minutos":35,"id_paciente":19,"id_residente":33,"id_preceptor":39,"id_unidade":5}'::jsonb),
(9999, 'INSERT', 'postgres', '2026-08-03 10:00:00',
    NULL,
    '{"id_atendimento":9999,"data_hora":"2026-08-03T10:00:00","duracao_minutos":15,"id_paciente":20,"id_residente":26,"id_preceptor":34,"id_unidade":1}'::jsonb),
(9999, 'DELETE', 'postgres', '2026-08-03 10:05:00',
    '{"id_atendimento":9999,"data_hora":"2026-08-03T10:00:00","duracao_minutos":15,"id_paciente":20,"id_residente":26,"id_preceptor":34,"id_unidade":1}'::jsonb,
    NULL);

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

select setval(pg_get_serial_sequence('internacao', 'id_internacao'), max(id_internacao))
from internacao;