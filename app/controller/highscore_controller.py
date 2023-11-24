# app/controller/highscore_controller.py

from flask import redirect, url_for, request  # Adicione a importação do request
from flask import Blueprint, render_template
from app.service.highscore_service import carregar_dados_manualmente
from app.service.highscore_service import carregar_ultimo_dados
from app.service.highscore_service import carregar_lotes
from app.service.highscore_service import obter_lote_mais_recente

highscore_bp = Blueprint('highscore', __name__)

@highscore_bp.route('/')
def index():
    # Obtenha o número do lote a partir da query string na URL
    numero_lote = request.args.get('lote')
    dados_lotes = carregar_lotes()
    # Se não houver número de lote na query string, use o mais recente
    if not numero_lote:
        # Busca os lotes do banco de dados
        lote_mais_recente = obter_lote_mais_recente(dados_lotes)
        numero_lote = lote_mais_recente

    # Busca os dados do banco de dados
    dados_highscore = carregar_ultimo_dados(numero_lote)

    # Renderiza a página inicial com os dados obtidos
    return render_template('highscore.html', numeros_lotes=carregar_lotes(), dados_highscore=dados_highscore)

@highscore_bp.route('/carregar-dados', methods=['POST'])
def carregar_dados():
    # Carrega os dados manualmente
    carregar_dados_manualmente()

    # Redireciona de volta para a página inicial
    return redirect(url_for('highscore.index'))

@highscore_bp.route('/carregar-lote', methods=['GET'])
def carregar_lote():
    # Obtenha o número do lote a partir da query string na URL
    numero_lote = request.args.get('lote')

    # Redirecione para a página inicial com o número do lote
    return redirect(url_for('highscore.index', lote=numero_lote))
