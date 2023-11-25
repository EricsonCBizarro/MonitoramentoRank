# app/controller/powerlevel_controller.py
from flask import Blueprint, render_template
from app.service.highscore_service import carregar_lotes
from app.service.powerlevel_service import calcular_rank_powerlevel

powerlevel_bp = Blueprint('powerlevel', __name__)

@powerlevel_bp.route('/')
def powerlevel():
    dados_lotes = carregar_lotes('asc')
    ranking  = calcular_rank_powerlevel(dados_lotes)
    return render_template('powerlevel.html', ranking =ranking )
