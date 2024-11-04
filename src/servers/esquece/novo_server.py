import threading
import time
from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
lock = threading.Lock()

# Estados do 3PC
PENDING = "PENDING"
PREPARED = "PREPARED"
COMMIT = "COMMIT"
ABORT = "ABORT"

# Carregar o grafo de rotas
with open("rotas.json", "r") as file:
    routes = json.load(file)

# Configuração de log
logging.basicConfig(filename="server.log", level=logging.INFO)

# Função de log
def log_transaction(state, flight_id, seat_id):
    logging.info(f"{time.time()}: {state} - Voo: {flight_id}, Assento: {seat_id}")

# Função para verificar disponibilidade e iniciar o 3PC
@app.route('/reserve', methods=['POST'])
def initiate_reservation():
    data = request.json
    flight_id = data['flight_id']
    seat_id = data['seat_id']

    with lock:
        # Verificar disponibilidade do assento
        if routes[flight_id]["assentos"][seat_id]["avaliable"]:
            # Fase Pendente
            routes[flight_id]["assentos"][seat_id]["avaliable"] = False
            log_transaction(PENDING, flight_id, seat_id)

            # Confirmar que todos os servidores concordam (3PC)
            if prepare_commit(flight_id, seat_id):
                # Fase de commit
                log_transaction(COMMIT, flight_id, seat_id)
                return jsonify({"status": "success", "message": "Reserva confirmada"}), 200
            else:
                # Em caso de falha, reverter transação
                routes[flight_id]["assentos"][seat_id]["avaliable"] = True
                log_transaction(ABORT, flight_id, seat_id)
                return jsonify({"status": "error", "message": "Falha na reserva"}), 400
        else:
            return jsonify({"status": "error", "message": "Assento indisponível"}), 400

def prepare_commit(flight_id, seat_id):
    # Fase de preparação: verificar com os outros servidores
    other_servers = ["http://server2:5000", "http://server3:5000"]
    for server in other_servers:
        try:
            response = requests.post(f"{server}/prepare", json={"flight_id": flight_id, "seat_id": seat_id})
            if response.status_code != 200:
                return False
        except requests.ConnectionError:
            return False
    return True

# Fase de preparação
@app.route('/prepare', methods=['POST'])
def prepare():
    data = request.json
    flight_id = data['flight_id']
    seat_id = data['seat_id']

    with lock:
        if routes[flight_id]["assentos"][seat_id]["avaliable"]:
            log_transaction(PREPARED, flight_id, seat_id)
            return jsonify({"status": "prepared"}), 200
        else:
            return jsonify({"status": "unavailable"}), 400

# Rota de commit
@app.route('/commit', methods=['POST'])
def commit():
    data = request.json
    flight_id = data['flight_id']
    seat_id = data['seat_id']

    with lock:
        if routes[flight_id]["assentos"][seat_id]["avaliable"] == False:
            routes[flight_id]["assentos"][seat_id]["avaliable"] = False
            log_transaction(COMMIT, flight_id, seat_id)
            return jsonify({"status": "committed"}), 200
        else:
            return jsonify({"status": "failed"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
