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
    e.turno,
    e.dia_plantao,
    e.mes_plantao,
    e.ano_plantao

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