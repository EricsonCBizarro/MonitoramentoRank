# app/controller/powerlevel_controller.py
from flask import Blueprint, render_template
# from app.service.highscore_service import obter_dados_powerlevel

powerlevel_bp = Blueprint('powerlevel', __name__)

@powerlevel_bp.route('/')
def powerlevel():
    # dados_powerlevel = obter_dados_powerlevel()
    return render_template('powerlevel.html')
