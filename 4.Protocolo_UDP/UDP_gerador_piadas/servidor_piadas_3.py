import socket
import random
import json
import os

# Configurações
IP = "127.0.0.1"
PORT = 5005
BUFFER_SIZE = 1024
ARQUIVO_JSON = "piadas.json"


def carregar_piadas():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


# Carrega a lista de dicionários
DADOS_PIADAS = carregar_piadas()

# Estado dos clientes
clientes_estado = {}

print("Aguardando conexões...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Evita o erro de porta ocupada ao reiniciar rapidamente
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))

print(f"Servidor iniciado com {len(DADOS_PIADAS)} piadas estruturadas.")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"Conexão de {addr}")
    if addr not in clientes_estado:
        indices = list(range(len(DADOS_PIADAS)))
        random.shuffle(indices)
        clientes_estado[addr] = {"pilha": indices, "finalizado": False}

    estado = clientes_estado[addr]

    if estado["finalizado"]:
        resposta_final = "Sem mais piadas para enviar."
    elif estado["pilha"]:
        index = estado["pilha"].pop()

        # ACESSO AOS DADOS: Pega o dicionário e formata a string
        item = DADOS_PIADAS[index]
        resposta_final = f"{item['pergunta']}\n{item['resposta']}"

        if not estado["pilha"]:
            estado["finalizado"] = True

    sock.sendto(resposta_final.encode('utf-8'), addr)