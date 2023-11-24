# app/service/highscore_service.py

from app.models import HighscoreEntry
from app import db
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from sqlalchemy import distinct

def obter_numero_lote():
    hora_atual = datetime.now()
    formato_hora = hora_atual.strftime("%Y%m%d%H%M%S")
    numero_lote = f"Lote_{formato_hora}"
    return numero_lote

def obter_dados_highscore():
    # Obter o número de lote vinculado à hora
    numero_lote = obter_numero_lote()

    url = 'http://empera-ot.com/?highscores'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        linhas = soup.find_all('tr', {'style': 'height: 64px;'})

        dados_extratos = []

        for linha in linhas:
            colunas = linha.find_all('td')

            # Verifica se a linha possui o número esperado de colunas
            if len(colunas) >= 6:
                rank = colunas[0].text.strip()

                # Extrai o nome do jogador com tratamento para o caso de ter formatação HTML
                nome_element = colunas[2].find('span')
                nome = nome_element.text.strip() if nome_element else colunas[2].text.strip()

                # Verifica se o link do personagem começa com a URL esperada
                link_personagem = colunas[2].find('a')['href']
                if link_personagem.startswith('http://empera-ot.com/?characters/'):
                    vocation = colunas[3].text.strip()
                    nivel = colunas[4].text.strip()
                    pontos = colunas[5].find('div').text.strip()

                    dados_extratos.append({
                        'rank': rank,
                        'nome': nome,
                        'vocation': vocation,
                        'nivel': nivel,
                        'pontos': pontos,
                        'numero_lote' : numero_lote
                    })

                    # Salva os dados no banco
                    salvar_highscore_no_banco(rank, nome, vocation, nivel, pontos,numero_lote)

        return dados_extratos
    else:
        print(f'Erro ao obter dados. Código de status: {response.status_code}')
        return None
    
def salvar_highscore_no_banco(rank, nome, vocation, nivel, pontos, numero_lote):
    entrada = HighscoreEntry(rank=rank , nome=nome, vocation=vocation, nivel=nivel, pontos=pontos, numero_lote=numero_lote)
    db.session.add(entrada)
    db.session.commit()

def carregar_dados_manualmente():

    # Obtém os dados
    dados_highscore = obter_dados_highscore()

    return dados_highscore

def carregar_ultimo_dados(numero_lote):
    
    dados_highscore = HighscoreEntry.query.filter_by(numero_lote=numero_lote).all()
    
    return dados_highscore

def carregar_lotes():
    
    todos_os_lotes = db.session.query(HighscoreEntry.numero_lote).distinct().order_by(HighscoreEntry.numero_lote.desc()).all()
    return [lote[0] for lote in todos_os_lotes]

def obter_lote_mais_recente(lista_de_lotes):
    # Converta os timestamps de string para objetos datetime
    lotes_com_datetimes = [datetime.strptime(lote.split('_')[1], '%Y%m%d%H%M%S') for lote in lista_de_lotes]

    # Encontre o lote mais recente usando a função max
    lote_mais_recente = max(lista_de_lotes, key=lambda x: datetime.strptime(x.split('_')[1], '%Y%m%d%H%M%S'))

    return lote_mais_recente