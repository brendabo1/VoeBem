import networkx as nx
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Recupera as variáveis de ambiente
servidor_a = os.getenv('SERVIDOR_A')
servidor_b = os.getenv('SERVIDOR_B')
servidor_c = os.getenv('SERVIDOR_C')

# Exemplo de uso
peers = [servidor_a, servidor_b, servidor_c]
print("Peers configurados com dotenv:", peers)

def construir_grafo(dicionario_rotas):
    # Inicializa um grafo direcionado
    G = nx.DiGraph()

    # Itera sobre as origens no dicionário
    for origem, destinos in dicionario_rotas.items():
        # Itera sobre cada destino e seus voos
        for destino, voos in destinos.items():
            for voo in voos:
                # Adiciona uma aresta com os dados do voo
                G.add_edge(
                    origem, 
                    destino, 
                    voo=voo['voo'], 
                    companhia=voo['companhia'],
                    duracao=voo['duracao'],
                    avaliable=voo['avaliable'],
                    assentos=voo['assentos']
                )
    return G
