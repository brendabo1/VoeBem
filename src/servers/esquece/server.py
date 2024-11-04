import os
import json
import threading
import time
import requests
from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# Variáveis globais para Raft
server_id = os.getenv("SERVER_ID")
server_port = int(os.getenv("SERVER_PORT"))
flight_data = {}
all_servers = os.getenv("ALL_SERVERS").split(",")
current_leader = None
term = 0
log_file = f"/app/logs/server_{server_id}.log"

# Estado do Raft
is_leader = False
election_timeout = random.uniform(5, 10)  # Timeout de eleição

# Função para carregar o grafo de rotas
def load_flight_data(routes_file):
    with open(routes_file, "r") as file:
        return json.load(file)

# Função para replicar o supergrafo e responder às requisições
def get_supergraph():
    supergraph = {}
    for server in all_servers:
        try:
            response = requests.get(f"http://{server}/routes")
            if response.status_code == 200:
                connections = response.json()["connections"]
                supergraph.update(connections)
        except requests.exceptions.RequestException:
            continue
    return supergraph

# Rota para obter rotas locais
@app.route("/routes", methods=["GET"])
def get_routes():
    return jsonify({"connections": flight_data})

# Função de busca de rotas no supergrafo
@app.route("/search", methods=["GET"])
def search_routes():
    start = request.args.get("start")
    end = request.args.get("end")
    supergraph = get_supergraph()
    routes = find_routes_in_supergraph(supergraph, start, end)
    return jsonify({"routes": routes})

# Função de consenso em Raft
def initiate_election():
    global is_leader, term, current_leader
    term += 1
    votes = 1
    print_log(f"Servidor {server_id}: Iniciando eleição no termo {term}.")
    
    for other_server in all_servers:
        if other_server != f"localhost:{server_port}":
            try:
                response = requests.post(f"http://{other_server}/request_vote", json={"term": term, "candidate_id": f"localhost:{server_port}"})
                if response.json().get("vote_granted"):
                    votes += 1
            except requests.exceptions.RequestException:
                continue
    
    if votes > len(all_servers) // 2:
        is_leader = True
        current_leader = f"localhost:{server_port}"
        print_log(f"Servidor {server_id}: Eleito como líder no termo {term}.")
    else:
        is_leader = False

@app.route("/request_vote", methods=["POST"])
def request_vote():
    global term, current_leader
    request_data = request.get_json()
    candidate_term = request_data["term"]
    candidate_id = request_data["candidate_id"]
    
    if candidate_term > term:
        term = candidate_term
        current_leader = candidate_id
        print_log(f"Servidor {server_id}: Votando no candidato {candidate_id} para o termo {term}.")
        return jsonify({"vote_granted": True})
    return jsonify({"vote_granted": False})

def print_log(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")
    print(message)

def monitor_leader():
    global current_leader, is_leader
    while True:
        time.sleep(election_timeout)
        if not current_leader or (is_leader and current_leader == f"localhost:{server_port}"):
            initiate_election()

# Função de busca de rotas no supergrafo (DFS)
def find_routes_in_supergraph(super_graph, start_city, end_city):
    routes = []
    visited = set()
    path = []

    def dfs(current, destination):
        if current == destination:
            routes.append(list(path))
            return
        visited.add(current)
        for next_city, flights in super_graph.get(current, {}).items():
            if next_city not in visited:
                for flight in flights:
                    path.append((current, next_city, flight))
                    dfs(next_city, destination)
                    path.pop()
        visited.remove(current)

    dfs(start_city, end_city)
    return routes

def main():
    global flight_data
    flight_data = load_flight_data("/app/routes.json")
    
    print_log(f"Servidor {server_id} iniciado na porta {server_port}")
    threading.Thread(target=monitor_leader, daemon=True).start()
    app.run(host="0.0.0.0", port=server_port, threaded=True)

if __name__ == "__main__":
    main()
