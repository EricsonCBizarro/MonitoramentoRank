# app/models.py
from app import db

class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    experiencia = db.Column(db.Integer, nullable=False)
