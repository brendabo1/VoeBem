import requests
import os

def login(server_url, user_id, senha):
    response = requests.post(f"{server_url}/login", json={"id": user_id, "senha": senha})
    print(response.json())

def listar_supergrafo(server_url):
    response = requests.get(f"{server_url}/listar_supergrafo")
    print(response.json())

def reservar_assentos(server_url, origem, destino, assentos):
    response = requests.post(f"{server_url}/reservar_assentos", json={
        "origem": origem,
        "destino": destino,
        "assentos": assentos
    })
    print(response.json())


def login_antigo():
    valido = False
    while not valido:
        os.system('cls||clear')
        print('=' * 22 +  "LOGIN " + '=' * 22 +"\n\n" )
        print("\033[31m" +"Para Sair ID: 'x'" +"\033[0m")
     
        user_id = input("ID: ")
        if user_id == 'x' or user_id == 'X':
            enviar_mensagem(socket, 'LOGOUT', None)
            break
        senha = input("Senha: ")
        if not user_id or not senha:
            print("Usuário e senha não podem estar vazios.") 
            pausa()
            continue
        elif autenticar(socket, user_id, senha):  
            return True

        

def autenticar(sock, user_id, senha):
    """
    Função para fazer login e capturar o ID do usuário.
    
    Parâmetros:
    - sock (socket.socket): O socket TCP conectado ao servidor.
    - user_id (str): id do usuário.
    - senha (str): A senha do usuário.
    
    Retorna:
    - str: O ID do usuário se o login for bem-sucedido.
    """
    # Envia a mensagem de login para o servidor
    enviar_mensagem(sock, 'LOGIN', {'id': user_id, 'senha': senha})

    # Recebe a resposta do servidor
    tipo, dados = receber_mensagem(sock)

    if tipo == 'LOGIN_SUCESSO':
        print(f"Login realizado com sucesso! ID do usuário: {dados['id']}")
        pausa()
        return dados['id']  # Retorna o ID do usuário
    else:
        print(f"Erro no login: {dados['mensagem']}")
        pausa()
        return None

def buscar_supergrafo():
    for server in servers:
        try:
            response = requests.get(f"http://{server}/listar_supergrafo")
            if response.status_code == 200:
                supergrafo = response.json()
                print("Supergrafo obtido com sucesso:")
                print(supergrafo)
                return supergrafo
        except requests.exceptions.RequestException as e:
            print(f"Falha ao se conectar com {server}: {e}")
    print("Não foi possível obter o supergrafo de nenhum servidor.")
    return None


def exibe_todas_rotas(socket):
    enviar_mensagem(socket, "LISTAR_TODAS_ROTAS", None)
    tipo, dados = receber_mensagem(socket)
    
    if tipo == 'TODAS_ROTAS_RESP':
        os.system('cls||clear')

        if not dados:
            print(f"Nenhuma rota encontrada.\n")
            if voltar_menu():
                return None
        
        print('=' * 22 + " ROTAS " + '=' * 22 +"\n\n")
        print(f"{'Origem':<10} {'Destino':<10} {'Voo':<15} {'Duração':<10}")
        print('-' * 44)
        for rota in dados:
            origem_str = str(rota['origem'])
            destino_str = str(rota['destino'])
            voo_str = str(rota['voo'])
            duracao_str = str(rota['duracao'])
            print(f"{origem_str:<10} {destino_str:<10} {voo_str:<15} {duracao_str:<10}")
        print('-' * 44)
        legenda_aeroportos()
        if voltar_menu():
            return True
    else:
        mensagem = dados.get('mensagem')
        print(mensagem)
        pausa()
        return None

if __name__ == "__main__":
    origem = input("Digite a cidade de origem: ")
    destino = input("Digite a cidade de destino: ")
    buscar_rotas(origem, destino)
