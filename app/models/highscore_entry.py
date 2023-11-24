from datetime import datetime
from app import db

class HighscoreEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    vocation = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.String(10), nullable=False)
    pontos = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return f"<HighscoreEntry nome={self.nome}, rank={self.rank}, vocation={self.vocation}, nivel={self.nivel}, pontos={self.pontos}>"
