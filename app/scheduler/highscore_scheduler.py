# scheduler/highscore_scheduler.py

import schedule
import time

from service.highscore_service import obter_dados_highscore

def atualizar_dados_agendados():
    dados_highscore = obter_dados_highscore()
    # Armazene os dados atualizados onde for apropriado

# Agendamento da atualização a cada 1 hora
schedule.every(1).hours.do(atualizar_dados_agendados)

# Função para executar o agendamento em segundo plano
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
