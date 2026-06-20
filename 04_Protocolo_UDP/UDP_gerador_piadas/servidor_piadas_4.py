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
        # Retorna uma lista padrão caso o arquivo não exista para não quebrar o código
        return [{"pergunta": "Por que o computador foi ao médico?", "resposta": "Porque estava com vírus!"}]
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


# Carrega a lista de dicionários
DADOS_PIADAS = carregar_piadas()

# Estado dos clientes
clientes_estado = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))

print(f"Servidor iniciado em {IP}:{PORT} com {len(DADOS_PIADAS)} piadas.")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    # Decodifica a mensagem para verificar se é um comando
    mensagem_cliente = data.decode('utf-8').strip().lower()

    print(f"Recebido de {addr}: {mensagem_cliente}")

    # LÓGICA DE REINICIALIZAÇÃO OU NOVO CLIENTE
    if addr not in clientes_estado or mensagem_cliente == "reiniciar":
        indices = list(range(len(DADOS_PIADAS)))
        random.shuffle(indices)
        clientes_estado[addr] = {"pilha": indices, "finalizado": False}

        if mensagem_cliente == "reiniciar":
            resposta_final = "Ciclo reiniciado! Aqui vai a primeira:\n"
        else:
            resposta_final = ""  # Início padrão
    else:
        resposta_final = ""

    estado = clientes_estado[addr]

    # LÓGICA DE ENVIO
    if estado["finalizado"]:
        resposta_final = "Sem mais piadas p ara enviar. Digite 'reiniciar' para resetar sua lista."
    elif estado["pilha"]:
        index = estado["pilha"].pop()
        item = DADOS_PIADAS[index]

        # Monta a piada (concatenando com o aviso de reinício se houver)
        resposta_final += f"{item['pergunta']}\n{item['resposta']}"

        if not estado["pilha"]:
            estado["finalizado"] = True
            resposta_final += "\nSem mais piadas para enviar. Digite 'reiniciar' para ler de novo)"

    sock.sendto(resposta_final.encode('utf-8'), addr)