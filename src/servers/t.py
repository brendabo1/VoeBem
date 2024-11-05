from flask import Flask, request, jsonify
import json
import threading
import requests
import logging
import os
import time
from raft_algoritmo import RaftNode

app = Flask(__name__)

# Caminhos para arquivos
USUARIOS_FILE = 'usuarios.json'
ROTAS_FILE = 'rotas.json'

# Configurações do Raft
server_id = os.getenv("SERVER_ID")
outros_servidores = os.getenv("OUTROS_SERVIDORES").split(",")
raft_node = RaftNode(server_id=server_id, peers=outros_servidores)

# Configuração de log
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Funções de manipulação de usuários
def carregar_usuarios():
    with open(USUARIOS_FILE, 'r') as f:
        return json.load(f)

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

# Função de login
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    user_id = dados.get("id")
    senha = dados.get("senha")

    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["id"] == user_id and usuario["senha"] == senha:
            return jsonify({"message": "Login bem-sucedido"}), 200
    return jsonify({"message": "ID ou senha incorretos"}), 401

# Endpoint GET /grafo_rotas
@app.route('/grafo_rotas', methods=['GET'])
def get_grafo_rotas():
    rotas = carregar_rotas()
    return jsonify(rotas), 200

# Supergrafo de rotas
def atualizar_supergrafo():
    supergrafo = {}
    for servidor in outros_servidores:
        try:
            response = requests.get(f"http://{servidor}/grafo_rotas")
            if response.status_code == 200:
                grafo_outra_companhia = response.json()
                supergrafo.update(grafo_outra_companhia)
                logging.info(f"Supergrafo atualizado com rotas de {servidor}")
        except requests.RequestException as e:
            logging.error(f"Erro ao acessar {servidor}: {e}")
    return supergrafo

@app.route('/listar_supergrafo', methods=['GET'])
def listar_supergrafo():
    supergrafo = atualizar_supergrafo()
    return jsonify(supergrafo)

# Função para anexar reserva ao usuário
def anexar_pedido_usuario(user_id, reserva, arquivo_usuarios):
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["id"] == user_id:
            if "reservas" not in usuario:
                usuario["reservas"] = []
            usuario["reservas"].append(reserva)
            salvar_usuarios(usuarios)
            return
    # Se usuário não encontrado, opcionalmente adicionar ou retornar erro

# Reserva de assentos
@app.route('/reservar_assentos', methods=['POST'])
def reservar_assentos():
    data = request.json
    origem = data['origem']
    destino = data['destino']
    assentos = data['assentos']
    supergrafo = atualizar_supergrafo()

    # Realizar reserva de assentos com lock distribuído
    return jsonify({"status": "Reserva realizada com sucesso"}), 200

# Endpoints do Raft
@app.route('/request_vote', methods=['POST'])
def request_vote():
    data = request.json
    response = raft_node.handle_request_vote(data["term"], data["candidate_id"])
    return jsonify(response)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    response = raft_node.handle_heartbeat(data["term"], data["leader_id"])
    return jsonify(response)

# Início do servidor
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
