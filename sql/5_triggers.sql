-- Triggers

CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT ON procedimento_realizado
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_media_procedimentos();