
from app.models import HighscoreEntry
from datetime import datetime
from collections import defaultdict

def calcular_rank_powerlevel(dados_lotes):
    dados_powerlevel = monta_informações_power_level(dados_lotes)
    ranking = calcular_rank_global_com_experiencia(dados_powerlevel)
    rank_powerlevel_ordenado = formatar_ranking_para_front(ranking)
    return rank_powerlevel_ordenado
    
def monta_informações_power_level(dados_lotes):
    dados_powerlevel = []

    for lote in dados_lotes:
        
        campo_nivel = HighscoreEntry.nivel

        # Extraia o número do lote do formato Lote_20231124171319
        numero_lote = lote.split('_')[1]
        
        # Converta o número do lote para um formato de data e hora
        datahora_lote = datetime.strptime(numero_lote, '%Y%m%d%H%M%S')

        # Consulte os dados para o lote atual
        dados_por_lote = HighscoreEntry.query.filter_by(numero_lote=lote).filter(campo_nivel > 7200).all()
        
        # Adicione os dados do lote ao resultado
        dados_powerlevel.append({
            'dados': dados_por_lote,
            'datahora': datahora_lote,
            'numero_lote': lote
        })

    return dados_powerlevel

def calcular_rank_global_com_experiencia(dados_powerlevel):
    dados_powerlevel_ordenado = sorted(dados_powerlevel, key=lambda x: x['datahora'])
    experiencia_por_jogador = {}

    # Coloca todos os dados em variavel para interação
    for lote_data in dados_powerlevel_ordenado:   
        dados_por_lote = lote_data['dados']

        # Dentro do loop onde você verifica a existência da primeira experiência
        for personagem_data in dados_por_lote:
            nome_jogador = personagem_data.nome
            # Remover vírgulas da string antes de converter para inteiro
            pontos_experiencia = int(personagem_data.pontos.replace(',', ''))

            # Verificar se o jogador já possui uma entrada
            if nome_jogador not in experiencia_por_jogador:
                experiencia_por_jogador[nome_jogador] = {'primeira_experiencia': pontos_experiencia, 'experiencia_total': 0}
            else:
                # Converter a primeira experiência para inteiro antes de realizar a subtração
                primeira_experiencia = int(experiencia_por_jogador[nome_jogador]['primeira_experiencia'])
                # Calcular a diferença entre a experiência atual e a anterior
                diferenca_experiencia = pontos_experiencia - primeira_experiencia
                # Adicionar ou subtrair a diferença à experiência total do jogador
                experiencia_por_jogador[nome_jogador]['experiencia_total'] += diferenca_experiencia

    # Ordenar o dicionário de experiência por jogador com base na experiência total
    ranking = sorted(experiencia_por_jogador.items(), key=lambda x: x[1]['experiencia_total'], reverse=True)

    return ranking

def formatar_ranking_para_front(ranking):
    ranking_ordenado = []
    
    for posicao, (nome_jogador, dados_jogador) in enumerate(ranking, start=1):
        
        experiencia_formatada = "{:,}".format(dados_jogador['experiencia_total'])

        jogador_formatado = {
            'rank': posicao,
            'nome': nome_jogador,
            'experiencia_total': experiencia_formatada
        }
        ranking_ordenado.append(jogador_formatado)
    
    return ranking_ordenado    