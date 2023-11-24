# app/service/highscore_service.py

from app.models import HighscoreEntry
from app import db
from bs4 import BeautifulSoup
import requests

def obter_dados_highscore():
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
                        'pontos': pontos
                    })

                    # Salva os dados no banco
                    salvar_highscore_no_banco(rank, nome, vocation, nivel, pontos)

        return dados_extratos
    else:
        print(f'Erro ao obter dados. Código de status: {response.status_code}')
        return None
    
def salvar_highscore_no_banco(rank, nome, vocation, nivel, pontos):
    entrada = HighscoreEntry(rank=rank , nome=nome, vocation=vocation, nivel=nivel, pontos=pontos)
    db.session.add(entrada)
    db.session.commit()

def carregar_dados_manualmente():
    
    # Limpa os dados existentes no banco
    HighscoreEntry.query.delete()

    # Obtém os dados
    dados_highscore = obter_dados_highscore()

    return dados_highscore
