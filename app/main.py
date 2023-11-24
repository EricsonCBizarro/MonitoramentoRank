# app/main.py
from flask import Flask
from app.controller import highscore_bp, powerlevel_bp
from app.scheduler.highscore_scheduler import run_schedule
from app import db  # Adicione este import

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db.init_app(app)  # Inicialize o db aqui

# Registra os blueprints
app.register_blueprint(highscore_bp, url_prefix='/highscore')
app.register_blueprint(powerlevel_bp, url_prefix='/powerlevel')

if __name__ == '__main__':
    with app.app_context():
        # Cria o banco de dados e as tabelas
        db.create_all()

    # Inicia o agendamento em segundo plano
    run_schedule()

    # Inicia a aplicação Flask
    app.run(debug=True)
