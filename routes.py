# app/routes.py
from flask import render_template
from app import app

@app.route('/')
def index():
    return 'Página Inicial'

@app.route('/personagens')
def personagens():
    return 'Lista de Personagens'
