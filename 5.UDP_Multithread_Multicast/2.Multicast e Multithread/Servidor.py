import socket
import time
import threading 

GRUPO = '224.1.1.7'
PORTA_ENVIO = 50000     # multicast para clientes
PORTA_RECEBE = 50001    # unicast de clientes

recebe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recebe.bind(('', PORTA_RECEBE))

transmite = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

valores = []
lock = threading.Lock() # evita inconsistência nos dados

def tarefa_envio():
    while True:
        time.sleep(5.0)
        with lock:
            if valores:
                media = sum(valores) / len(valores)
                msg = f"Média atual : {media:.2f}"
                transmite.sendto(msg.encode('utf-8'), (GRUPO, PORTA_ENVIO))
                print("Enviando: ", msg)

threading.Thread(target=tarefa_envio, daemon=True).start()

print(f"Servidor recebendo em na porta {PORTA_RECEBE} e enviando em {GRUPO}:{PORTA_ENVIO}")

while True:
    dados, addr = recebe.recvfrom(1024)
    try:
        valor = float(dados.decode('utf-8'))
        with lock:
            valores.append(valor)
        print(f"recebeu {valor:.2f} de {addr}")
    except ValueError:
        pass
