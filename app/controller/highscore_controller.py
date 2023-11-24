# app/controller/highscore_controller.py

from flask import redirect, url_for
from flask import Blueprint, render_template
from app.models.highscore_entry import HighscoreEntry
from app.service.highscore_service import carregar_dados_manualmente

highscore_bp = Blueprint('highscore', __name__)

@highscore_bp.route('/')
def index():
    # Busca os dados do banco de dados
    dados_highscore = HighscoreEntry.query.all()

    # Renderiza a página inicial com os dados obtidos
    return render_template('index.html', dados_highscore=dados_highscore)

@highscore_bp.route('/carregar-dados', methods=['POST'])
def carregar_dados():
    # Carrega os dados manualmente
    carregar_dados_manualmente()

    # Redireciona de volta para a página inicial
    return redirect(url_for('highscore.index'))
