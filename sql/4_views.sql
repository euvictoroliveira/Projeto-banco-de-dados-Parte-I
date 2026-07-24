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