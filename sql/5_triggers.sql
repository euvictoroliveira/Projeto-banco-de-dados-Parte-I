-- Triggers

CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT ON procedimento_realizado
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_media_procedimentos();

CREATE TRIGGER trg_check_sobreposicao_escala
BEFORE INSERT OR UPDATE ON escala
FOR EACH ROW
EXECUTE FUNCTION fn_check_sobreposicao_escala();