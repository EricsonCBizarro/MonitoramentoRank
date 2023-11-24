# scheduler/highscore_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.create_app import create_app
from app.service.highscore_service import obter_dados_highscore
import requests

scheduler = BackgroundScheduler()

def acionar_atualizacao_de_dados():
    url = 'http://127.0.0.1:5000/highscore/carregar-dados'  # Substitua pelo URL correto da sua rota
    resposta = requests.post(url)

    if resposta.status_code == 200:
        print("Atualização de dados bem-sucedida.")
    else:
        print(f"Falha na atualização de dados. Código de status: {resposta.status_code}")

scheduler.add_job(acionar_atualizacao_de_dados, 'interval', minutes=10)

# Inicie o scheduler em segundo plano
def run_schedule():
    scheduler.start()

if __name__ == '__main__':
    run_schedule()
