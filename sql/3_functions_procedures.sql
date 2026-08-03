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


-- --------------------------------------------------------------------------------------------------
-- Procedure para reajustar escala
CREATE OR REPLACE PROCEDURE sp_reajustar_escala(
    p_id_residente INTEGER,
    p_dia_atual VARCHAR,
    p_turno_atual VARCHAR,
    p_dia_novo VARCHAR,
    p_turno_novo VARCHAR,
    INOUT p_mensagem VARCHAR DEFAULT NULL -- para retornar mensagem de saída
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- para guardar a escala da vez enquanto o cursor percorre 
    r_escala RECORD;

    v_conflito BOOLEAN;
	v_data_plantao TIMESTAMP;
    v_atualizadas INTEGER := 0;
    v_puladas INTEGER := 0;
    v_total INTEGER := 0;

BEGIN
    -- percorre todas as escalas do residente que estão no dia e turno atuais
    FOR r_escala IN
        SELECT id_escala, id_unidade 
        FROM escala 
        WHERE id_residente = p_id_residente
        AND dia_semana = p_dia_atual
        AND turno = p_turno_atual
    LOOP
        v_total := v_total + 1;

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

    -- mensagem de retorno de acordo com o resultado do ajuste
    IF v_total = 0 THEN
        p_mensagem := FORMAT(
            'Nenhuma escala encontrada para o residente %s no dia %s turno %s.',
            p_id_residente, p_dia_atual, p_turno_atual
        );
    ELSIF v_atualizadas > 0 AND v_puladas = 0 THEN
        p_mensagem := FORMAT(
            'Escala alterada com sucesso: %s escala(s) movida(s) para %s no turno da %s.',
            v_atualizadas, p_dia_novo, p_turno_novo
        );
    ELSIF v_atualizadas > 0 AND v_puladas > 0 THEN
        p_mensagem := FORMAT(
            'Escala parcialmente alterada: %s movida(s) para %s turno %s e %s mantida(s) por conflito de horário.',
            v_atualizadas, p_dia_novo, p_turno_novo, v_puladas
        );
    ELSE
        p_mensagem := FORMAT(
            'Escala mantida: por existir conflito em %s turno na %s.',
            v_puladas, p_dia_novo, p_turno_novo
        );
    END IF;

    -- obs: mantendo o RAISE NOTICE também, para acompanhamento no console/log do banco
    RAISE NOTICE 'As escalas do residente % foram reajustadas: % atualizada(s) e % mantida(s)',
        p_id_residente, v_atualizadas, v_puladas;
        
END;
$$;


-- -------------------------------------------------------------------------------------------------
-- procedure para registrar um atendimento completo
CREATE OR REPLACE PROCEDURE sp_registrar_atendimento_completo(
    p_data_hora TIMESTAMP,
    p_duracao_minutos INTEGER,
    p_id_paciente INTEGER,
    p_id_residente INTEGER,
    p_id_preceptor INTEGER,
    p_id_unidade INTEGER,

    p_procedimentos JSONB,

    INOUT p_id_atendimento INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- v_id_atendimento INTEGER; ??
    v_id_procedimento INTEGER;
    v_quantidade INTEGER;
    v_tempo_real_minutos INTEGER;
    v_observacao VARCHAR(200);
    v_data_hora_inicio TIMESTAMP;
    -- para percorrer cada elemento do array JSON recebido
    v_procedimento JSONB;

BEGIN
    -- Validando existência primeiro
    IF NOT EXISTS (SELECT 1 FROM paciente WHERE id_pessoa = p_id_paciente) THEN
        RAISE EXCEPTION 'Paciente % não encontrado.', p_id_paciente;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM residente WHERE id_profissional = p_id_residente) THEN
        RAISE EXCEPTION 'Residente % não encontrado.', p_id_residente;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM preceptor WHERE id_profissional = p_id_preceptor) THEN
        RAISE EXCEPTION 'Preceptor % não encontrado.', p_id_preceptor;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM unidade WHERE id_unidade = p_id_unidade) THEN
        RAISE EXCEPTION 'Unidade % não encontrada.', p_id_unidade;
    END IF;

    -- validação dos dados do atendimento
    IF p_duracao_minutos IS NULL OR p_duracao_minutos <= 0 THEN
        RAISE EXCEPTION 'Duração do atendimento deve ser maior que zero.';
    END IF;

    IF p_procedimentos IS NULL
       OR jsonb_typeof(p_procedimentos) <> 'array'
       OR jsonb_array_length(p_procedimentos) = 0 THEN
        RAISE EXCEPTION 'É necessário informar ao menos um procedimento realizado.';
    END IF;

    -- 1. Insere o atendimento e retorna seu id 
    INSERT INTO atendimento (
        data_hora, 
        duracao_minutos, 
        id_paciente, 
        id_residente, 
        id_preceptor, 
        id_unidade
    )
    VALUES (
        p_data_hora, 
        p_duracao_minutos, 
        p_id_paciente, 
        p_id_residente, 
        p_id_preceptor, 
        p_id_unidade
    )
    RETURNING id_atendimento INTO p_id_atendimento;

    -- 2. Percorre o JSON iserindo cada procedimento em procedimento_realizado
    FOR v_procedimento IN SELECT * FROM jsonb_array_elements(p_procedimentos)
    LOOP
        -- extraindo os dados do JSON
        v_id_procedimento    := (v_procedimento->>'id_procedimento')::INTEGER;
        v_quantidade         := (v_procedimento->>'quantidade')::INTEGER;
        v_tempo_real_minutos := (v_procedimento->>'tempo_real_minutos')::INTEGER;
        v_observacao         := v_procedimento->>'observacao';

        -- Defindo o horário de início (se não vier no JSON, fica o horário do atendimento)
        v_data_hora_inicio   := COALESCE(
            (v_procedimento->>'data_hora_inicio')::TIMESTAMP,
            p_data_hora
        );
 
        -- validando o procedimento
        IF NOT EXISTS (
            SELECT 1 FROM procedimento
            WHERE id_procedimento = v_id_procedimento
        ) THEN
            RAISE EXCEPTION 'Procedimento % não encontrado.', v_id_procedimento;
        END IF;

        -- validações de integridade dos campos
        IF v_quantidade IS NULL OR v_quantidade <= 0 THEN
            RAISE EXCEPTION 'Quantidade inválida para o procedimento %.', v_id_procedimento;
        END IF;

        IF v_tempo_real_minutos IS NULL OR v_tempo_real_minutos <= 0 THEN
            RAISE EXCEPTION 'Tempo real inválido para o procedimento %.', v_id_procedimento;
        END IF;

        IF v_observacao IS NULL OR btrim(v_observacao) = '' THEN
            RAISE EXCEPTION 'Observação obrigatória para o procedimento %.', v_id_procedimento;
        END IF;

        -- só pra caso exista procedimento duplicado na lista
        IF EXISTS (
            SELECT 1 FROM procedimento_realizado
            WHERE id_atendimento = p_id_atendimento
              AND id_procedimento = v_id_procedimento
        ) THEN
            RAISE EXCEPTION 'Procedimento % duplicado na lista enviada.', v_id_procedimento;
        END IF;

        -- por fim, insere o procedimento utilizado as variáveis locais já tratadas
        INSERT INTO procedimento_realizado (
            id_atendimento,
            id_procedimento,
            quantidade,
            tempo_real_minutos,
            observacao,
            data_hora_inicio
        )
        VALUES (
            p_id_atendimento,
            v_id_procedimento,
            v_quantidade,
            v_tempo_real_minutos,
            v_observacao,
            v_data_hora_inicio
        );
    END LOOP;

    RAISE NOTICE 'Atendimento % registrado com sucesso, com % procedimento(s).',
        p_id_atendimento, jsonb_array_length(p_procedimentos);
END;
$$;


-- -------------------------------------------------------------------------------------------------
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


-- -------------------------------------------------------------------------------------------------
-- Function para auditoria dos atendimentos
-- Registra automaticamente INSERT, UPDATE e DELETE na tabela atendimento
CREATE OR REPLACE FUNCTION fn_audita_atendimento()
RETURNS TRIGGER AS $$
BEGIN

    -- Registro após inserção
    IF TG_OP = 'INSERT' THEN

        INSERT INTO auditoria_atendimento (
            id_atendimento,
            operacao,
            usuario_bd,
            data_hora,
            dados_antigos,
            dados_novos
        )
        VALUES (
            NEW.id_atendimento,
            TG_OP,
            CURRENT_USER,
            CURRENT_TIMESTAMP,
            NULL,
            to_jsonb(NEW)
        );

        RETURN NEW;

    END IF;

    -- Registro após atualização
    IF TG_OP = 'UPDATE' THEN

        INSERT INTO auditoria_atendimento (
            id_atendimento,
            operacao,
            usuario_bd,
            data_hora,
            dados_antigos,
            dados_novos
        )
        VALUES (
            NEW.id_atendimento,
            TG_OP,
            CURRENT_USER,
            CURRENT_TIMESTAMP,
            to_jsonb(OLD),
            to_jsonb(NEW)
        );

        RETURN NEW;

    END IF;

    -- Registro após remoção
    IF TG_OP = 'DELETE' THEN

        INSERT INTO auditoria_atendimento (
            id_atendimento,
            operacao,
            usuario_bd,
            data_hora,
            dados_antigos,
            dados_novos
        )
        VALUES (
            OLD.id_atendimento,
            TG_OP,
            CURRENT_USER,
            CURRENT_TIMESTAMP,
            to_jsonb(OLD),
            NULL
        );

        RETURN OLD;

    END IF;

    RETURN NULL;

END;
$$ LANGUAGE plpgsql;


-- -----------------------------------------------------------------------------------------------
-- Function para checar sobreposição de escala
CREATE OR REPLACE FUNCTION fn_check_sobreposicao_escala()
RETURNS TRIGGER AS $$
BEGIN
    -- verifica se já existe outra linha de escala para o mesmo residente,
    -- no mesmo dia/turno, mas em unidade diferente
    IF EXISTS (
        SELECT 1
        FROM escala
        WHERE id_residente = NEW.id_residente
        AND dia_semana = NEW.dia_semana
        AND turno = NEW.turno
        AND id_unidade <> NEW.id_unidade
        AND id_escala <> NEW.id_escala
    ) THEN
        RAISE EXCEPTION 'Residente % já está escalado em outra unidade no dia % turno %.',
            NEW.id_residente, NEW.dia_semana, NEW.turno;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;