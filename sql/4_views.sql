create or replace view vw_pacientes_internados as
select
	i.id_paciente,
	p.nome as nome_paciente,
	i.id_unidade,
	i.data_hora_entrada
from (
	select distinct on (id_paciente) *
	from internacao
	order by id_paciente, data_hora_entrada DESC
) i

inner join pessoa p on i.id_paciente = p.id_pessoa
where i.data_hora_saida is null;

-- View de residentes sem supervisor
CREATE OR REPLACE VIEW vw_residentes_sem_supervisor AS
SELECT DISTINCT
    r.id_profissional AS id_residente,
    p_res.nome AS nome_residente,

    pr.id_profissional AS id_preceptor,
    p_pre.nome AS nome_preceptor,
    pr.titulacao,

    u.nome AS unidade,

    e.dia_semana,
    e.turno

FROM escala e

INNER JOIN residente r
    ON e.id_residente = r.id_profissional

INNER JOIN profissional prof_res
    ON r.id_profissional = prof_res.id_pessoa

INNER JOIN pessoa p_res
    ON prof_res.id_pessoa = p_res.id_pessoa

INNER JOIN preceptor pr
    ON e.id_preceptor = pr.id_profissional

INNER JOIN profissional prof_pre
    ON pr.id_profissional = prof_pre.id_pessoa

INNER JOIN pessoa p_pre
    ON prof_pre.id_pessoa = p_pre.id_pessoa

INNER JOIN unidade u
    ON e.id_unidade = u.id_unidade

WHERE pr.titulacao <> 'Doutor';

-- View de estatísticas de procedimentos mais comuns
CREATE OR REPLACE VIEW vw_estatisticas_atendimentos_mensal AS
WITH procedimentos_contagem AS (
    SELECT
        DATE_TRUNC('month', a.data_hora) AS mes,
        a.id_unidade,
        pr.nome AS procedimento,
        COUNT(*) AS quantidade,

        RANK() OVER (
            PARTITION BY DATE_TRUNC('month', a.data_hora), a.id_unidade
            ORDER BY COUNT(*) DESC
        ) AS posicao

    FROM atendimento a
    INNER JOIN procedimento_realizado p
        ON a.id_atendimento = p.id_atendimento
    INNER JOIN procedimento pr
        ON p.id_procedimento = pr.id_procedimento
    GROUP BY
        DATE_TRUNC('month', a.data_hora),
        a.id_unidade,
        pr.nome
),

procedimentos_mais_comuns AS (
    SELECT
        mes,
        id_unidade,
        STRING_AGG(procedimento, ', ' ORDER BY procedimento) AS procedimentos_mais_comuns
    FROM procedimentos_contagem
    WHERE posicao = 1
    GROUP BY
        mes,
        id_unidade
)

SELECT
    DATE_TRUNC('month', a.data_hora) AS mes,
    u.id_unidade,
    u.nome AS unidade,
    COUNT(*) AS total_atendimentos,
    ROUND(AVG(a.duracao_minutos), 2) AS media_duracao,
    pmc.procedimentos_mais_comuns

FROM atendimento a

INNER JOIN unidade u
    ON a.id_unidade = u.id_unidade
    
LEFT JOIN procedimentos_mais_comuns pmc
    ON pmc.mes = DATE_TRUNC('month', a.data_hora)
    AND pmc.id_unidade = a.id_unidade

GROUP BY
    DATE_TRUNC('month', a.data_hora),
    u.id_unidade,
    u.nome,
    pmc.procedimentos_mais_comuns;