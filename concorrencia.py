import time
import threading
import logging
from flask import Flask, Blueprint
from sqlalchemy import text
from models import db, Escala, Pessoa

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

def simular_concorrencia(app):
    
    def tentar_escalar(id_res, id_unidade, dia, turno, id_preceptor, tempo_espera):

        with app.app_context():
            try:
                logging.info("Iniciando transação...")
                
                # Tranca o registro do residente (lock pessimista)
                residente = db.session.query(Pessoa).filter_by(id_pessoa=id_res).with_for_update().first()
                logging.info(f"Lock adquirido no residente {id_res}. Analisando escala...")
                
                # Uma das threads tem um atraso para simular o conflito
                if tempo_espera > 0:
                    logging.info(f"Processando dados (simulando lentidão de {tempo_espera}s)...")
                    time.sleep(tempo_espera)
                
                # Verifica se a escala já existe antes de inserir
                escala_existente = db.session.query(Escala).filter_by(
                    id_unidade=id_unidade,
                    dia_semana=dia,
                    turno=turno,
                    id_residente=id_res
                ).first()
                
                if escala_existente:
                    logging.warning("O residente já está escalado neste dia/turno/unidade.")
                    db.session.rollback()
                    return
                
                nova_escala = Escala(
                    id_unidade=id_unidade,
                    dia_semana=dia,
                    turno=turno,
                    id_residente=id_res,
                    id_preceptor=id_preceptor
                )
                db.session.add(nova_escala)
                db.session.commit()
                logging.info("Escala INSERIDA com sucesso!")
                
            except Exception as e:
                db.session.rollback()
                logging.error(f"Erro na transação: {e}")


    # Thread 1: Vai segurar o lock por 3 segundos
    t1 = threading.Thread(target=tentar_escalar, name="Thread 1 (Lenta)", args=(6, 1, 'Sexta-feira', 'Noite', 11, 3))
    
    # Thread 2: Vai tentar rodar sem espera, mas será bloqueada pelo banco até a T1 acabar
    t2 = threading.Thread(target=tentar_escalar, name="Thread 2 (Rápida)", args=(6, 1, 'Sexta-feira', 'Noite', 11, 0))


    t1.start()
    t2.start()


    t1.join()
    t2.join()

    return "Simulação concluída"