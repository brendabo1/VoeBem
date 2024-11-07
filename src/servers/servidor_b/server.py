import re
import time
from flask import Flask, request, jsonify
import json
import threading
import requests
import logging
import os
from dotenv import load_dotenv
from raft_algoritmo import RaftNode
from flask_cors import CORS
import networkx as nx

app = Flask(__name__)
CORS(app) 

# Caminhos para arquivos
USUARIOS_FILE = "data/usuarios.json"
ROTAS_FILE = "data/rotas.json"
load_dotenv()

# def garantir_url_valida(url):
#     if not url.startswith("http://") and not url.startswith("https://"):
#         return f"http://{url}"  # Adiciona http:// se faltar
#     return url

# servidor_a = garantir_url_valida(os.getenv('SERVIDOR_A'))
# servidor_b = garantir_url_valida(os.getenv('SERVIDOR_B'))
# servidor_c = garantir_url_valida(os.getenv('SERVIDOR_C'))
# print(f"Servidor A corrigido: {servidor_a}")
# print(f"Servidor B corrigido: {servidor_b}")
# print(f"Servidor C corrigido: {servidor_c}")

# Recupera as variáveis de ambiente
servidor_a = os.getenv('SERVIDOR_A')
servidor_b = os.getenv('SERVIDOR_B')
servidor_c = os.getenv('SERVIDOR_C')

peers = [servidor_a, servidor_b, servidor_c]
#server_id = os.getenv("SERVER_ID")
#outros_servidores = os.getenv("OUTROS_SERVIDORES").split(",")
#raft_node = RaftNode(server_id=server_id, peers=outros_servidores)

# Configuração de log
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=4)

# Carregar rotas
def carregar_rotas():
    with open(ROTAS_FILE, 'r') as f:
        return json.load(f)

def salvar_rotas(rotas):
    with open(ROTAS_FILE, 'w') as f:
        json.dump(rotas, f, indent=4)

# Carregar o arquivo de usuários
def carregar_usuarios():
    try:
        with open("data/usuarios.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    if not dados:
        return jsonify({"message": "Dados de login não fornecidos"}), 400
    
    user_id = dados.get("id")
    senha = dados.get("senha")
    if not user_id or not senha:
        return jsonify({"message": "ID e senha são necessários"}), 400

    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["id"] == user_id and usuario["senha"] == senha:
            return jsonify({"message": "Login bem-sucedido"}), 200
    return jsonify({"message": "ID ou senha incorretos"}), 401


# Função para anexar o pedido ao usuário
def anexar_pedido_usuario(user_id, reserva, arquivo_usuarios):
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["id"] == user_id:
            if "reservas" not in usuario:
                usuario["reservas"] = []
            usuario["reservas"].append(reserva)
            salvar_usuarios(usuarios)
            return

# Endpoint GET /grafo_rotas
@app.route('/grafo_rotas', methods=['GET'])
def get_grafo_rotas():
    rotas = carregar_rotas()
    return jsonify(rotas), 200


def obter_grafos(peers):
    grafos = {}
    for peer in peers:
        try:
            response = requests.get(f"{peer}/grafo_rotas")
            if response.status_code == 200:
                grafos[peer] = response.json()
            else:
                logging.error(f"Erro ao obter grafo de {peer}: Status {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Erro ao conectar com o servidor {peer}: {e}")
    return grafos


def construir_grafo_from_file(dicionario_rotas):
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

def grafo_para_dicionario(grafo):
    dicionario_rotas = {}

    # Itera sobre todas as arestas do grafo e organiza no formato desejado
    for origem, destino, dados in grafo.edges(data=True):
        if origem not in dicionario_rotas:
            dicionario_rotas[origem] = {}
        if destino not in dicionario_rotas[origem]:
            dicionario_rotas[origem][destino] = []
        
        # Adiciona os dados do voo no formato desejado
        dicionario_rotas[origem][destino].append({
            "voo": dados["voo"],
            "assentos": dados["assentos"],
            "companhia": dados["companhia"],
            "duracao": dados["duracao"],
            "avaliable": dados["avaliable"]
        })

    return dicionario_rotas

def compose_supergrafo_rotas():
    response_a = requests.get(f"{servidor_a}/grafo_rotas")
    response_b = requests.get(f"{servidor_b}/grafo_rotas")
    response_c = requests.get(f"{servidor_c}/grafo_rotas")
    if response_a.status_code == 200 and response_b.status_code == 200 and response_c.status_code == 200:
        grafo_a = construir_grafo_from_file(response_a.json())
        grafo_b = construir_grafo_from_file(response_b.json())
        grafo_c = construir_grafo_from_file(response_c.json())
        
    g_ab = nx.compose(grafo_a, grafo_b)
    g_abc = nx.compose(g_ab, grafo_c)
    grafo_abc = grafo_para_dicionario(g_abc)
    return grafo_abc     


# # Função para construir supergrafo
# def construir_supergrafo(grafos_companhias):
#     supergrafo = {}

#     for grafo in grafos_companhias:
#         for origem, destinos in grafo.items():
#             if origem not in supergrafo:
#                 supergrafo[origem] = {}
#             for destino, voos in destinos.items():
#                 if destino not in supergrafo[origem]:
#                     supergrafo[origem][destino] = []
#                 for voo in voos:
#                     # Adiciona o voo ao supergrafo
#                     voo_info = {
#                         "voo": voo["voo"],
#                         "assentos": voo["assentos"],
#                         "companhia": voo["companhia"],
#                         "duracao": voo["duracao"],
#                         "avaliable": voo["avaliable"]
#                     }
#                     supergrafo[origem][destino].append(voo_info)

#     return supergrafo

def buscar_rotas_antigo(origem, destino, rotas):
    caminhos = []
    def dfs(current, target, path, visited):
        if current == target:
            caminhos.append(list(path))
            return
        if current not in rotas:
            return
        for next_dest, voos in rotas[current].items():
            if next_dest in visited:
                continue
            for voo in voos:
                if voo['avaliable']:
                    path.append({"voo": voo['voo'], "duracao": voo['duracao'], "next_dest": next_dest, "servidor": server_id})
                    visited.add(next_dest)
                    dfs(next_dest, target, path, visited)
                    path.pop()
                    visited.remove(next_dest)
    dfs(origem, destino, [], set([origem]))
    return caminhos

def converter_duracao_para_minutos(duracao_str):
    """
    Converte uma duração no formato '2h', '45m' ou '1h05m' para minutos.
    """
    horas = 0
    minutos = 0
    
    # Verifica se há horas
    if 'h' in duracao_str:
        horas = int(re.search(r'(\d+)h', duracao_str).group(1))
    
    # Verifica se há minutos
    if 'm' in duracao_str:
        minutos = int(re.search(r'(\d+)m', duracao_str).group(1))
    
    # Converte tudo para minutos
    return horas * 60 + minutos


def buscar_rotas(origem, destino, rotas):
    caminhos = []

    def dfs(current, target, path, visited, total_duracao):
        if current == target:
            caminhos.append(list(path))
            return
        if current not in rotas:
            return
        for next_dest, voos in rotas[current].items():
            if next_dest in visited:
                continue
            for voo in voos:
                if voo['avaliable']:
                    duracao_voo = converter_duracao_para_minutos(voo['duracao'])
                    assentos_disponiveis = [assento['cod'] for assento in voo['assentos'] if assento['avaliable']]
                    path.append({
                        "origem": current,
                        "voo": voo['voo'],
                        "duracao": duracao_voo,
                        "destino": next_dest,
                        "companhia": voo['companhia'],
                        "assentos_disponiveis": assentos_disponiveis
                    })
                    visited.add(next_dest)
                    dfs(next_dest, target, path, visited, total_duracao + duracao_voo)
                    path.pop()
                    visited.remove(next_dest)

    dfs(origem, destino, [], set([origem]), 0)
    return caminhos


@app.route('/supergrafo', methods=['GET'])
def get_supergrafo():
    try:
        supergrafo = compose_supergrafo_rotas()

        return jsonify({"supergrafo": supergrafo}), 200
    except Exception as e:
        logging.error(f"Erro ao construir supergrafo: {e}")
        return jsonify({"message": "Erro interno ao construir o supergrafo."}), 500


# Endpoint POST /buscar_rotas
@app.route('/buscar_rotas', methods=['POST'])
def buscar_rotas_api():
    dados = request.json
    origem = dados.get('origem')
    destino = dados.get('destino')
    
    if not origem or not destino:
        return jsonify({"message": "Origem e destino são necessários."}), 400
    try:
        supergrafo = compose_supergrafo_rotas()
        rotas = buscar_rotas(origem, destino, supergrafo)
        
        return jsonify({"rotas": rotas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/verificar_assentos', methods=['POST'])
# def verificar_assentos():
#     rota = request.json.get("rota", [])
    
#     if not rota:
#         return jsonify({"erro": "Rota não informada."}), 400

#     assentos_disponiveis = []
#     for voo in rota:
#         voo_id = voo.get("voo")
#         if voo_id:
#             assentos = consultar_assentos_disponiveis(voo_id)
#             assentos_disponiveis.append({
#                 "voo": voo_id,
#                 "assentos_disponiveis": assentos
#             })

#     return jsonify(assentos_disponiveis)

def consultar_assentos_disponiveis(rotas, voos_selecionados, arquivo_grafo):
    """
    Busca os assentos disponíveis para cada voo em uma rota selecionada.

    Parâmetros:
    - rotas (dict): Estrutura do grafo de rotas com voos e assentos.
    - voos_selecionados (list): Lista de voos selecionados na rota.

    Retorna:
    - dict: Um dicionário com os assentos disponíveis para cada voo.
    """
    assentos_disponiveis = {}

    for trecho in voos_selecionados:
        voo_selecionado = trecho['voo']
        origem = trecho['origem']
        destino = trecho['next_dest']
        # print(f"Verificando voo {voo_selecionado} de {origem} para {destino}")

        if origem in rotas and destino in rotas[origem]:
            for voo in rotas[origem][destino]:
                if voo['voo'] == voo_selecionado:
                    # if checa_disponibilidade_voo(origem, destino, voo['voo'], rotas, arquivo_grafo):
                    assentos = [assento['cod'] for assento in voo['assentos'] if assento['avaliable']]
                    assentos_disponiveis[voo_selecionado] = assentos
                    break
                else:
                    continue
            else:
                    return None
        else:
            return None

    return assentos_disponiveis


# @app.route('/selec_assento', methods=['POST'])
# def selecionaAssentos():
#     rota = request.json.get("rota", [])
#     assentos_disponiveis = []
#     for trecho in rota:
#         origem = trecho.get("origem")
#         destino = trecho.get("next_dest")
#         voo_id = trecho.get("voo")
#         # Simula busca de assentos disponíveis
#         assentos = ["A1", "A2", "B1", "B2"]  # Exemplo de assentos disponíveis
#         assentos_disponiveis.append({
#             "voo": voo_id,
#             "origem": origem,
#             "destino": destino,
#             "assentos": assentos
#         })
#     return jsonify(assentos_disponiveis)

@app.route('/confirmar_compra', methods=['POST'])
def confirmar_compra():
    assentos_selecionados = request.json.get("assentos", {})
    # Aqui, adicionar lógica para processar a compra
    return jsonify({"mensagem": "Compra confirmada com sucesso!"})

# Função para atualizar a disponibilidade do voo
def atualizar_disponibilidade_voo(rotas, origem, destino, voo_selecionado):
    if origem in rotas and destino in rotas[origem]:
        for voo in rotas[origem][destino]:
            if voo['voo'] == voo_selecionado:
                # Verifica se há ao menos um assento disponível
                voo_disponivel = any(assento['avaliable'] for assento in voo['assentos'])
                # Atualiza o status do voo com base na disponibilidade dos assentos
                voo['avaliable'] = voo_disponivel
                break


# Implementação do 3PC

reservas_pendentes = {}  # Armazena reservas pendentes
lock = threading.Lock()

# Fase de Prepare
@app.route('/prepare', methods=['POST'])
def prepare():
    dados = request.json
    reserva_id = dados.get('reserva_id')
    trechos = dados.get('trechos')
    #user_id = dados.get('user_id')
    
    with lock:
        rotas = compose_supergrafo_rotas()
        # Verificar disponibilidade de todos os trechos
        sucesso = True
        for trecho in trechos:
            origem = trecho['origem']
            destino = trecho['destino']
            voo_selecionado = trecho['voo']
            assento_escolhido = trecho['assento']
            
            if origem in rotas and destino in rotas[origem]:
                voo = next((v for v in rotas[origem][destino] if v['voo'] == voo_selecionado), None)
                if voo and voo['avaliable']:
                    assento = next((a for a in voo['assentos'] if a['cod'] == assento_escolhido and a['avaliable']), None)
                    if not assento:
                        sucesso = False
                        break
                else:
                    sucesso = False
                    break
            else:
                sucesso = False
                break
        
        if sucesso:
            # Marcar os trechos como pendentes
            reservas_pendentes[reserva_id] = trechos
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"status": "ERROR"}), 409

# Fase de Pre-Commit
@app.route('/pre_commit', methods=['POST'])
def pre_commit():
    dados = request.json
    reserva_id = dados.get('reserva_id')
    
    with lock:
        rotas = compose_supergrafo_rotas()
        if reserva_id in reservas_pendentes:
            trechos = reservas_pendentes[reserva_id]
            sucesso = True
            for trecho in trechos:
                origem = trecho['origem']
                destino = trecho['destino']
                voo_selecionado = trecho['voo']
                assento_escolhido = trecho['assento']
                
                voo = next((v for v in rotas[origem][destino] if v['voo'] == voo_selecionado), None)
                if voo:
                    assento = next((a for a in voo['assentos'] if a['cod'] == assento_escolhido and a['avaliable']), None)
                    if not assento:
                        sucesso = False
                        break
                else:
                    sucesso = False
                    break
            
            if sucesso:
                return jsonify({"status": "ACK"}), 200
            else:
                return jsonify({"status": "ERROR"}), 409
        else:
            return jsonify({"status": "ERROR"}), 409

# Fase de Commit
@app.route('/do_commit', methods=['POST'])
def do_commit():
    dados = request.json
    reserva_id = dados.get('reserva_id')
    user_id = dados.get('user_id')
    
    with lock:
        rotas = compose_supergrafo_rotas()
        if reserva_id in reservas_pendentes:
            trechos = reservas_pendentes.pop(reserva_id)
            # Reservar efetivamente os assentos
            for trecho in trechos:
                origem = trecho['origem']
                destino = trecho['destino']
                voo_selecionado = trecho['voo']
                assento_escolhido = trecho['assento']
                
                voo = next((v for v in rotas[origem][destino] if v['voo'] == voo_selecionado), None)
                if voo:
                    assento = next((a for a in voo['assentos'] if a['cod'] == assento_escolhido), None)
                    if assento:
                        assento['avaliable'] = False
                        # Atualiza a disponibilidade do voo
                        atualizar_disponibilidade_voo(rotas, origem, destino, voo_selecionado)
            
            salvar_rotas(rotas)
            # Anexa a reserva ao usuário
            pedido_completo = {
                'reserva_id': reserva_id,
                'trechos': trechos
            }
            anexar_pedido_usuario(user_id, pedido_completo, USUARIOS_FILE)
            return jsonify({"status": "sucesso"}), 200
        else:
            return jsonify({"status": "ERROR"}), 409

# Fase de Abort
@app.route('/abort', methods=['POST'])
def abort():
    dados = request.json
    reserva_id = dados.get('reserva_id')
    
    with lock:
        if reserva_id in reservas_pendentes:
            reservas_pendentes.pop(reserva_id)
    return jsonify({"status": "abortado"}), 200

# Função para iniciar a compra com 3PC (como endpoint)
@app.route('/comprar_passagem', methods=['POST'])
def comprar_passagem():
    dados = request.json
    user_id = dados.get('user_id')
    trechos = dados.get('trechos')  # Lista de trechos: [{'origem': 'SSA', 'destino': 'PAV', 'voo': 'Voo AN490', 'assento': '1A', 'servidor': 'servidorA'}, ...]
    
    if not user_id or not trechos:
        return jsonify({"message": "Usuário e trechos são necessários."}), 400
    
    reserva_id = f"reserva_{int(time.time())}"
    servidores = {
    'A': servidor_a,
    'B': servidor_b,
    'C': servidor_c
    }

    servidores_involvidos = list(set(
        servidores[trecho['companhia']] for trecho in trechos if trecho['companhia'] in servidores
    ))
    print(servidores_involvidos)
    try:
        # Fase 1: Prepare
        votos = {}
        for servidor in servidores_involvidos:
            trecho_servidor = [t for t in trechos if servidores[t['companhia']] == servidor]
            response = requests.post(f"{servidor}/prepare", json={
                "reserva_id": reserva_id,
                "user_id": user_id,
                "trechos": trecho_servidor
            })
            print(response)
            if response.status_code == 200 and response.json().get("status") == "OK":
                votos[servidor] = "commit"
            else:
                votos[servidor] = "abort"
        
        # Verificar votos
        if all(v == "commit" for v in votos.values()):
            # Fase 2: Pre-Commit
            pre_commits = {}
            for servidor in servidores_involvidos:
                response = requests.post(f"{servidor}/pre_commit", json={"reserva_id": reserva_id})
                if response.status_code == 200 and response.json().get("status") == "ACK":
                    pre_commits[servidor] = "ACK"
                else:
                    pre_commits[servidor] = "abort"
            
            if all(v == "ACK" for v in pre_commits.values()):
                # Fase 3: Do Commit
                for servidor in servidores_involvidos:
                    requests.post(f"{servidor}/do_commit", json={
                        "reserva_id": reserva_id,
                        "user_id": user_id
                    })
                return jsonify({"message": "Compra realizada com sucesso!"}), 200
            else:
                # Abort
                for servidor in servidores_involvidos:
                    requests.post(f"{servidor}/abort", json={"reserva_id": reserva_id})
                return jsonify({"message": "Compra abortada devido a votos negativos na fase de pre-commit."}), 500
        else:
            # Abort
            for servidor in servidores_involvidos:
                requests.post(f"{servidor}/abort", json={"reserva_id": reserva_id})
            return jsonify({"message": "Compra abortada devido a votos negativos na fase de prepare."}), 500
    except Exception as e:
        # Abort em caso de exceção
        for servidor in servidores_involvidos:
            try:
                requests.post(f"/{servidor}/abort", json={"reserva_id": reserva_id})
            except:
                pass
        return jsonify({"message": f"Compra abortada devido a erro: {str(e)}"}), 500


# # Endpoints do Raft
# @app.route('/request_vote', methods=['POST'])
# def request_vote():
#     data = request.json
#     response = raft_node.handle_request_vote(data["term"], data["candidate_id"])
#     return jsonify(response)

# @app.route('/heartbeat', methods=['POST'])
# def heartbeat():
#     data = request.json
#     response = raft_node.handle_heartbeat(data["term"], data["leader_id"])
#     return jsonify(response)

# Início do servidor
if __name__ == '__main__':
    #port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=5002, debug=True)
    # app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
