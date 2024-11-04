# raft_algorithm.py

import threading
import time
import logging
import requests

class RaftNode:
    def __init__(self, server_id, peers):
        self.server_id = server_id
        self.peers = peers
        self.current_term = 0
        self.voted_for = None
        self.leader_id = None
        self.commit_index = 0
        self.state = "follower"  # follower, candidate, leader
        self.log = []
        self.lock = threading.Lock()
        self.election_timeout = 5  # segundos

    def start_election(self):
        with self.lock:
            self.state = "candidate"
            self.current_term += 1
            self.voted_for = self.server_id
            votes_received = 1

        def request_vote(peer):
            try:
                response = requests.post(f"http://{peer}/request_vote", json={
                    "term": self.current_term,
                    "candidate_id": self.server_id
                })
                if response.status_code == 200 and response.json().get("vote_granted"):
                    nonlocal votes_received
                    votes_received += 1
            except requests.RequestException:
                logging.error(f"Erro ao solicitar voto de {peer}")

        threads = []
        for peer in self.peers:
            t = threading.Thread(target=request_vote, args=(peer,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if votes_received > len(self.peers) // 2:
            self.state = "leader"
            self.leader_id = self.server_id
            self.send_heartbeat()
        else:
            self.state = "follower"

    def send_heartbeat(self):
        def heartbeat(peer):
            try:
                requests.post(f"http://{peer}/heartbeat", json={
                    "term": self.current_term,
                    "leader_id": self.leader_id
                })
            except requests.RequestException:
                logging.error(f"Erro ao enviar heartbeat para {peer}")

        while self.state == "leader":
            for peer in self.peers:
                threading.Thread(target=heartbeat, args=(peer,)).start()
            time.sleep(self.election_timeout)

    def handle_request_vote(self, term, candidate_id):
        with self.lock:
            if term > self.current_term:
                self.current_term = term
                self.voted_for = candidate_id
                return {"term": self.current_term, "vote_granted": True}
            return {"term": self.current_term, "vote_granted": False}

    def handle_heartbeat(self, term, leader_id):
        with self.lock:
            if term >= self.current_term:
                self.current_term = term
                self.leader_id = leader_id
                self.state = "follower"
        return {"term": self.current_term, "success": True}

