import socket
import struct
import random
import time
import threading

GRUPO = '224.1.1.7' # endereço multicast 
PORTA_GERAL = 50000  # média geral
PORTA_DOIS = 52000  # média dos dois últimos valores
PORTA_SERVIDOR = 51000 # unicast para enviar valores ao servidor
SERVIDOR_IP = '127.0.0.1'  # IP do servidor

# recebe qq valor multicast
def receber_multicast(nome, porta):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conexao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conexao.bind(('', porta))

    multicast = struct.pack('4s4s', socket.inet_aton(GRUPO), socket.inet_aton('0.0.0.0'))
    conexao.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast)

    print(f"[{nome}] Aguardando mensagens em {GRUPO}:{porta}")

    while True:
        dados, _ = conexao.recvfrom(1024)
        print(f"[{nome}] recebe: {dados.decode('utf-8', errors='ignore')}")

# envia valores p servidor
def enviar_valores():
    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        valor = random.uniform(10.0, 40.0)
        print(f"Valor enviado: {valor:.2f}")
        conexao.sendto(f"{valor:.2f}".encode('utf-8'), (SERVIDOR_IP, PORTA_SERVIDOR))
        time.sleep(random.uniform(2.0, 4.0))

threading.Thread(target=receber_multicast, args=("MEDIA GERAL", PORTA_GERAL), daemon=True).start()
threading.Thread(target=receber_multicast, args=("ULTIMOS 2", PORTA_DOIS), daemon=True).start()

# Envia valores 
enviar_valores()
