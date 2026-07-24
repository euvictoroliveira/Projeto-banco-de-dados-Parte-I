
-- procedures:

-- Procedure para tempo médio de espera 
CREATE OR REPLACE PROCEDURE sp_calcular_tempo_medio_espera()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Atualiza a coluna tempo_medio_espera_minutos da tabela unidade
    UPDATE unidade u
    SET tempo_medio_espera_minutos = calc.tempo_medio
    FROM (
        -- Subquery: Calcula a média de tempo por unidade
        SELECT 
            a.id_unidade,
            ROUND(AVG(EXTRACT(EPOCH FROM (pr.data_hora_inicio - a.data_hora)) / 60)::NUMERIC, 2) AS tempo_medio
        FROM atendimento a
        INNER JOIN (
            -- Pega apenas o horário do PRIMEIRO procedimento de cada atendimento
            SELECT id_atendimento, MIN(data_hora_inicio) as data_hora_inicio
            FROM procedimento_realizado
            GROUP BY id_atendimento
        ) pr ON a.id_atendimento = pr.id_atendimento
        GROUP BY a.id_unidade
    ) calc
    -- Condição de junção do UPDATE
    WHERE u.id_unidade = calc.id_unidade;
    
    -- Levanta um aviso no console de que a rotina terminou com sucesso
    RAISE NOTICE 'Tempos médios de espera recalculados e atualizados nas unidades com sucesso.';
END;
$$;

-- Procedure para reajustar escala
CREATE OR REPLACE PROCEDURE sp_reajustar_escala(
    p_id_residente INTEGER,
    p_dia_atual VARCHAR,
    p_turno_atual VARCHAR,
    p_dia_novo VARCHAR,
    p_turno_novo VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- para guardar a escala da vez enquanto o cursor percorre 
    r_escala RECORD;

    v_conflito BOOLEAN;
    v_atualizadas INTEGER := 0;
    v_puladas INTEGER := 0;
BEGIN
    -- percorre todas as escalas do residente que estão no dia e turno atuais
    FOR r_escala IN
        SELECT id_escala, id_unidade 
        FROM escala 
        WHERE id_residente = p_id_residente
        AND dia_semana = p_dia_atual
        AND turno = p_turno_atual
    LOOP
        -- checando conflito se existe outra escala do residente na mesma unidade, 
        -- no dia e turno de destino
        SELECT EXISTS (
            SELECT 1
            FROM escala
            WHERE id_unidade = r_escala.id_unidade
            AND dia_semana = p_dia_novo
            AND turno = p_turno_novo
            AND id_residente = p_id_residente
            AND id_escala <> r_escala.id_escala
        ) INTO v_conflito;

        IF v_conflito THEN
            v_puladas := v_puladas + 1;
        ELSE
            UPDATE escala
            SET dia_semana = p_dia_novo, 
                turno = p_turno_novo
            WHERE id_escala = r_escala.id_escala;

            v_atualizadas := v_atualizadas + 1;
        END IF; 
    END LOOP; 

    -- obs: estou deixando a saída com um RAISE NOTE para confirmar o que rodou, porém
    --      tem a opção de fazer com que a rota do flask mostre na tela uma saída
    --      (ex: 3 escalas foram atualizadas e 1 foi pulada por presença de conflito)!
    --      portantanto, fica à decisão quando for pensado sobre a construção da interface.

    RAISE NOTICE 'As escalas do residente % foram reajustadas: % atualizada(s) e % mantida(s)',
        p_id_residente, v_atualizadas, v_puladas;
        
END;
$$;

-- Functions:

-- Function para atualizar o tempo medio dos procedimentos
-- Foi preferido function ao invés de procedure pois é possível fazer os updates de forma direcionada
CREATE OR REPLACE FUNCTION fn_atualiza_media_procedimentos()
RETURNS TRIGGER AS $$
BEGIN
    -- Recalcula a média e atualiza na tabela procedimento
    UPDATE procedimento
    SET tempo_medio_minutos = (
        -- Verifica qual é a media em minutos daquele procedimento em específico
        SELECT COALESCE(ROUND(AVG(tempo_real_minutos)::NUMERIC, 2), 0)
        FROM procedimento_realizado
        WHERE id_procedimento = NEW.id_procedimento
    )
    WHERE id_procedimento = NEW.id_procedimento;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
