import socket
import struct
import random
import time
import threading

GRUPO = '224.1.1.7' # endereco multicast
PORTA_ENVIO = 50000     # multicast - recebe as médias
PORTA_SERVIDOR = 50001  # unicast - envia seus valores 
SERVIDOR_IP = '127.0.0.1'  # IP do servidor

# recebe msgs multicast
def receber_multicast():
    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conexao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conexao.bind(('', PORTA_ENVIO))

    multicast = struct.pack('4s4s', socket.inet_aton(GRUPO), socket.inet_aton('0.0.0.0'))
    conexao.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast)

    print(f"Cliente aguardando médias em {GRUPO}:{PORTA_ENVIO}")
    while True:
        dados, _ = conexao.recvfrom(1024)
        print("recebe: ", dados.decode('utf-8', errors='ignore'))

# transmite dados aleatórios (entre 10 e 40)
def enviar_valores():
    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        valor = random.uniform(10.0, 40.0)
        print(f'Valor enviado: {valor:.2f}')
        conexao.sendto(f"{valor:.2f}".encode('utf-8'), (SERVIDOR_IP, PORTA_SERVIDOR))
        time.sleep(random.uniform(2.0, 4.0))

# Executa recepção e envio em paralelo
threading.Thread(target=receber_multicast, daemon=True).start()
enviar_valores()
