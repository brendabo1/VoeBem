from flask import Flask, request, jsonify
import json
import threading
import requests
import logging
import os
import time
from raft_algoritmo import RaftNode
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

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

# Supergrafo de rotas
# def atualizar_supergrafo():
#     supergrafo = {}
#     for servidor in outros_servidores:
#         try:
#             response = requests.get(f"http://{servidor}/grafo_rotas")
#             if response.status_code == 200:
#                 grafo_outra_companhia = response.json()
#                 supergrafo.update(grafo_outra_companhia)
#                 logging.info(f"Supergrafo atualizado com rotas de {servidor}")
#         except requests.RequestException as e:
#             logging.error(f"Erro ao acessar {servidor}: {e}")
#     return supergrafo

# # Função para construir supergrafo
# def construir_supergrafo(origem, destino):
#     supergrafo = {}
#     rotas_local = carregar_rotas()
#     supergrafo.update(rotas_local)
    
#     for peer in raft_node.peers:
#         try:
#             response = requests.get(f"http://{peer}/grafo_rotas")
#             if response.status_code == 200:
#                 rotas_peer = response.json()
#                 supergrafo.update(rotas_peer)
#         except requests.RequestException as e:
#             logging.error(f"Erro ao obter grafo de {peer}: {e}")
#     return supergrafo

# def buscar_rotas(origem, destino, rotas):
#     caminhos = []
#     def dfs(current, target, path, visited):
#         if current == target:
#             caminhos.append(list(path))
#             return
#         if current not in rotas:
#             return
#         for next_dest, voos in rotas[current].items():
#             if next_dest in visited:
#                 continue
#             for voo in voos:
#                 if voo['avaliable']:
#                     path.append({"voo": voo['voo'], "duracao": voo['duracao'], "next_dest": next_dest, "servidor": server_id})
#                     visited.add(next_dest)
#                     dfs(next_dest, target, path, visited)
#                     path.pop()
#                     visited.remove(next_dest)
#     dfs(origem, destino, [], set([origem]))
#     return caminhos

# # @app.route('/listar_supergrafo', methods=['GET'])
# # def listar_supergrafo():
# #     supergrafo = atualizar_supergrafo()
# #     return jsonify(supergrafo)

# # Endpoint POST /buscar_rotas
# @app.route('/buscar_rotas', methods=['POST'])
# def buscar_rotas_api():
#     dados = request.json
#     origem = dados.get('origem')
#     destino = dados.get('destino')
    
#     if not origem or not destino:
#         return jsonify({"message": "Origem e destino são necessários."}), 400
    
#     supergrafo = construir_supergrafo(origem, destino)
#     rotas = buscar_rotas(origem, destino, supergrafo)
    
#     return jsonify({"rotas": rotas}), 200

# # Função para atualizar a disponibilidade do voo
# def atualizar_disponibilidade_voo(rotas, origem, destino, voo_selecionado):
#     if origem in rotas and destino in rotas[origem]:
#         for voo in rotas[origem][destino]:
#             if voo['voo'] == voo_selecionado:
#                 # Verifica se há ao menos um assento disponível
#                 voo_disponivel = any(assento['avaliable'] for assento in voo['assentos'])
#                 # Atualiza o status do voo com base na disponibilidade dos assentos
#                 voo['avaliable'] = voo_disponivel
#                 break


# # Implementação do 3PC

# reservas_pendentes = {}  # Armazena reservas pendentes
# lock = threading.Lock()

# # Fase de Prepare
# @app.route('/prepare', methods=['POST'])
# def prepare():
#     dados = request.json
#     reserva_id = dados.get('reserva_id')
#     trechos = dados.get('trechos')
#     user_id = dados.get('user_id')
    
#     with lock:
#         # Verificar disponibilidade de todos os trechos
#         sucesso = True
#         for trecho in trechos:
#             origem = trecho['origem']
#             destino = trecho['destino']
#             voo_selecionado = trecho['voo']
#             assento_escolhido = trecho['assento']
            
#             if origem in rotas and destino in rotas[origem]:
#                 voo = next((v for v in rotas[origem][destino] if v['voo'] == voo_selecionado), None)
#                 if voo and voo['avaliable']:
#                     assento = next((a for a in voo['assentos'] if a['cod'] == assento_escolhido and a['avaliable']), None)
#                     if not assento:
#                         sucesso = False
#                         break
#                 else:
#                     sucesso = False
#                     break
#             else:
#                 sucesso = False
#                 break
        
#         if sucesso:
#             # Marcar os trechos como pendentes
#             reservas_pendentes[reserva_id] = trechos
#             return jsonify({"status": "OK"}), 200
#         else:
#             return jsonify({"status": "ERROR"}), 409

# # Fase de Pre-Commit
# @app.route('/pre_commit', methods=['POST'])
# def pre_commit():
#     dados = request.json
#     reserva_id = dados.get('reserva_id')
    
#     with lock:
#         if reserva_id in reservas_pendentes:
#             trechos = reservas_pendentes[reserva_id]
#             sucesso = True
#             for trecho in trechos:
#                 origem = trecho['origem']
#                 destino = trecho['destino']
#                 voo_selecionado = trecho['voo']
#                 assento_escolhido = trecho['assento']
                
#                 voo = next((v for v in rotas[origem][destino] if v['voo'] == voo_selecionado), None)
#                 if voo:
#                     assento = next((a for a in voo['assentos'] if a['cod'] == assento_escolhido and a['avaliable']), None)
#                     if not assento:
#                         sucesso = False
#                         break
#                 else:
#                     sucesso = False
#                     break
            
#             if sucesso:
#                 return jsonify({"status": "ACK"}), 200
#             else:
#                 return jsonify({"status": "ERROR"}), 409
#         else:
#             return jsonify({"status": "ERROR"}), 409

# # Fase de Commit
# @app.route('/do_commit', methods=['POST'])
# def do_commit():
#     dados = request.json
#     reserva_id = dados.get('reserva_id')
#     user_id = dados.get('user_id')
    
#     with lock:
#         if reserva_id in reservas_pendentes:
#             trechos = reservas_pendentes.pop(reserva_id)
#             # Reservar efetivamente os assentos
#             for trecho in trechos:
#                 origem = trecho['origem']
#                 destino = trecho['destino']
#                 voo_selecionado = trecho['voo']
#                 assento_escolhido = trecho['assento']
                
#                 voo = next((v for v in rotas[origem][destino] if v['voo'] == voo_selecionado), None)
#                 if voo:
#                     assento = next((a for a in voo['assentos'] if a['cod'] == assento_escolhido), None)
#                     if assento:
#                         assento['avaliable'] = False
#                         # Atualiza a disponibilidade do voo
#                         atualizar_disponibilidade_voo(rotas, origem, destino, voo_selecionado)
            
#             salvar_rotas(rotas)
#             # Anexa a reserva ao usuário
#             pedido_completo = {
#                 'reserva_id': reserva_id,
#                 'trechos': trechos
#             }
#             anexar_pedido_usuario(user_id, pedido_completo, USUARIOS_FILE)
#             return jsonify({"status": "sucesso"}), 200
#         else:
#             return jsonify({"status": "ERROR"}), 409

# # Fase de Abort
# @app.route('/abort', methods=['POST'])
# def abort():
#     dados = request.json
#     reserva_id = dados.get('reserva_id')
    
#     with lock:
#         if reserva_id in reservas_pendentes:
#             reservas_pendentes.pop(reserva_id)
#     return jsonify({"status": "abortado"}), 200

# # Função para iniciar a compra com 3PC (como endpoint)
# @app.route('/comprar_passagem', methods=['POST'])
# def comprar_passagem():
#     dados = request.json
#     user_id = dados.get('user_id')
#     trechos = dados.get('trechos')  # Lista de trechos: [{'origem': 'SSA', 'destino': 'PAV', 'voo': 'Voo AN490', 'assento': '1A', 'servidor': 'servidorA'}, ...]
    
#     if not user_id or not trechos:
#         return jsonify({"message": "Usuário e trechos são necessários."}), 400
    
#     reserva_id = f"reserva_{int(time.time())}"
    
#     # Identificar servidores envolvidos
#     servidores_involvidos = list(set([trecho['servidor'] for trecho in trechos]))
    
#     try:
#         # Fase 1: Prepare
#         votos = {}
#         for servidor in servidores_involvidos:
#             trecho_servidor = [t for t in trechos if t['servidor'] == servidor]
#             response = requests.post(f"http://{servidor}/prepare", json={
#                 "reserva_id": reserva_id,
#                 "user_id": user_id,
#                 "trechos": trecho_servidor
#             })
#             if response.status_code == 200 and response.json().get("status") == "OK":
#                 votos[servidor] = "commit"
#             else:
#                 votos[servidor] = "abort"
        
#         # Verificar votos
#         if all(v == "commit" for v in votos.values()):
#             # Fase 2: Pre-Commit
#             pre_commits = {}
#             for servidor in servidores_involvidos:
#                 response = requests.post(f"http://{servidor}/pre_commit", json={"reserva_id": reserva_id})
#                 if response.status_code == 200 and response.json().get("status") == "ACK":
#                     pre_commits[servidor] = "ACK"
#                 else:
#                     pre_commits[servidor] = "abort"
            
#             if all(v == "ACK" for v in pre_commits.values()):
#                 # Fase 3: Do Commit
#                 for servidor in servidores_involvidos:
#                     requests.post(f"http://{servidor}/do_commit", json={
#                         "reserva_id": reserva_id,
#                         "user_id": user_id
#                     })
#                 return jsonify({"message": "Compra realizada com sucesso!"}), 200
#             else:
#                 # Abort
#                 for servidor in servidores_involvidos:
#                     requests.post(f"http://{servidor}/abort", json={"reserva_id": reserva_id})
#                 return jsonify({"message": "Compra abortada devido a votos negativos na fase de pre-commit."}), 500
#         else:
#             # Abort
#             for servidor in servidores_involvidos:
#                 requests.post(f"http://{servidor}/abort", json={"reserva_id": reserva_id})
#             return jsonify({"message": "Compra abortada devido a votos negativos na fase de prepare."}), 500
#     except Exception as e:
#         # Abort em caso de exceção
#         for servidor in servidores_involvidos:
#             try:
#                 requests.post(f"http://{servidor}/abort", json={"reserva_id": reserva_id})
#             except:
#                 pass
#         return jsonify({"message": f"Compra abortada devido a erro: {str(e)}"}), 500


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
    #port = int(os.getenv("PORT", 5003))
    app.run(host="0.0.0.0", port=5003)
    # app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
