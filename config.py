# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # ou 'sqlite:///:memory:' para banco de dados na memória
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # ou 'sqlite:///site.db' para salvar em arquivo
    SQLALCHEMY_TRACK_MODIFICATIONS = False
