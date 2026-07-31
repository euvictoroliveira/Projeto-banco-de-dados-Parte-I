-- Triggers

-- trigger para atualização da média de procedimentos.
CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT ON procedimento_realizado
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_media_procedimentos();

-- Trigger para sobreposição de escala.
CREATE TRIGGER trg_check_sobreposicao_escala
BEFORE INSERT OR UPDATE ON escala
FOR EACH ROW
EXECUTE FUNCTION fn_check_sobreposicao_escala();

-- Trigger para auditoria dos atendimentos.
CREATE TRIGGER trg_audita_atendimento
AFTER INSERT OR UPDATE OR DELETE
ON atendimento
FOR EACH ROW
EXECUTE FUNCTION fn_audita_atendimento();