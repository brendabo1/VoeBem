from flask import Flask, request, jsonify
import json
import threading
import logging

app = Flask(__name__)
lock = threading.Lock()

# Carrega o grafo de rotas desta companhia a partir do JSON
with open('rotas.json', 'r') as f:
    grafo_rotas = json.load(f)

# Configuração de logs
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Estado de consenso e transação
estado_raft = {'lider': None, 'eleicao': False}
transacoes_pendentes = {}

# Endpoint para verificação de saúde
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Função para eleger um líder usando o Raft
def eleger_lider():
    with lock:
        logging.info("Iniciando eleição de líder")
        estado_raft['eleicao'] = True
        # Simplificação do processo de eleição
        # Aqui, assume-se que o servidor atual é o líder para fins de implementação
        estado_raft['lider'] = "servidor_atual"
        estado_raft['eleicao'] = False
        logging.info(f"Líder eleito: {estado_raft['lider']}")

# Função para iniciar uma reserva com protocolo 3PC
def iniciar_reserva(dados_reserva):
    logging.info("Iniciando transação de reserva")
    transacao_id = dados_reserva.get("id")
    with lock:
        if transacao_id in transacoes_pendentes:
            return False  # Transação já está em andamento
        transacoes_pendentes[transacao_id] = "prepare"
    # Fase de preparação
    if preparar_reserva(dados_reserva):
        # Se a preparação for bem-sucedida, procede para commit
        transacoes_pendentes[transacao_id] = "commit"
        commit_reserva(dados_reserva)
    else:
        transacoes_pendentes[transacao_id] = "abort"
        abortar_reserva(dados_reserva)

# Função para preparação de reserva (fase 1 do 3PC)
def preparar_reserva(dados_reserva):
    logging.info("Preparando reserva")
    # Confirmação de disponibilidade dos assentos
    for trecho in dados_reserva["trechos"]:
        if not grafo_rotas.get(trecho['origem'], {}).get(trecho['destino']):
            logging.warning(f"Trecho indisponível: {trecho}")
            return False
    return True

# Função de commit de reserva (fase 2 do 3PC)
def commit_reserva(dados_reserva):
    logging.info("Confirmando reserva")
    for trecho in dados_reserva["trechos"]:
        voo = grafo_rotas[trecho['origem']][trecho['destino']][0]
        for assento in voo["assentos"]:
            if assento["cod"] in trecho["assentos"] and assento["avaliable"]:
                assento["avaliable"] = False
            else:
                abortar_reserva(dados_reserva)
                return
    logging.info("Reserva confirmada")

# Função de abortar reserva (fase de rollback do 3PC)
def abortar_reserva(dados_reserva):
    logging.warning("Abortando reserva")
    # Implementação do rollback pode ser detalhada conforme necessário

@app.route('/reservar', methods=['POST'])
def reservar_assento():
    dados_reserva = request.get_json()
    threading.Thread(target=iniciar_reserva, args=(dados_reserva,)).start()
    return jsonify({"status": "Processando reserva"}), 202

@app.route('/listar_rotas', methods=['GET'])
def listar_rotas():
    return jsonify(grafo_rotas)

if __name__ == '__main__':
    eleger_lider()  # Inicia o processo de eleição ao iniciar o servidor
    app.run(host='0.0.0.0', port=5002)  # Porta será alterada conforme o servidor
