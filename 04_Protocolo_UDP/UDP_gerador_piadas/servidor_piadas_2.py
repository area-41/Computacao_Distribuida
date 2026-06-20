import socket
import random
import json
import os

# Configurações do Servidor
IP = "127.0.0.1"
PORT = 5005
BUFFER_SIZE = 1024
ARQUIVO_JSON = "piadas.json"


def carregar_piadas():
    """Lê o arquivo JSON e retorna uma lista de strings."""
    if not os.path.exists(ARQUIVO_JSON):
        print(f"Erro: Arquivo {ARQUIVO_JSON} não encontrado!")
        return ["Erro: Banco de piadas offline."]

    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


# Carrega a lista do arquivo uma única vez no início
PIADAS_MASTER = carregar_piadas()

# { (ip, porta): { "pilha": [indices], "finalizado": False } }
clientes_estado = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"Servidor carregado com {len(PIADAS_MASTER)} piadas.")
print(f"Aguardando requisições em {IP}:{PORT}...")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)

    if addr not in clientes_estado:
        indices = list(range(len(PIADAS_MASTER)))
        random.shuffle(indices)
        clientes_estado[addr] = {"pilha": indices, "finalizado": False}

    estado = clientes_estado[addr]

    if estado["finalizado"]:
        resposta = "Acabaram as piadas! Todas já foram exibidas."
    elif estado["pilha"]:
        index = estado["pilha"].pop()
        resposta = PIADAS_MASTER[index]
        if not estado["pilha"]:
            estado["finalizado"] = True

    sock.sendto(resposta.encode('utf-8'), addr)