import socket
import time
import threading 

GRUPO = '224.1.1.7'
PORTA_ENVIO_DOIS = 52000  # multicast para média dos últimos dois valores
PORTA_ENVIO = 50000       # multicast para média geral
PORTA_RECEBE = 51000      # unicast para receber valores dos clientes

# Socket para receber valores dos clientes
recebe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recebe.bind(('', PORTA_RECEBE))

# Socket para enviar mensagens por multicast
transmite = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

valores = []
lock = threading.Lock()   


# Envia a média geral
def tarefa_envio_media():
    while True:
        time.sleep(5.0)
        with lock:
            if valores:
                media = sum(valores) / len(valores)
                msg = f"Média geral: {media:.2f}"
                transmite.sendto(msg.encode('utf-8'), (GRUPO, PORTA_ENVIO))
                print("Enviando (geral):", msg)


# Envia a média dos 2 últimos valores
def tarefa_envio_dois():
    while True:
        time.sleep(5.0)
        with lock:
            if len(valores) >= 2:
                ultimos = valores[-2:]
                media = sum(ultimos) / 2
                msg = f"Média dos dois últimos: {media:.2f}"
                transmite.sendto(msg.encode('utf-8'), (GRUPO, PORTA_ENVIO_DOIS))
                print("Enviando (últimos 2):", msg)        

# Iniciar threads
threading.Thread(target=tarefa_envio_media, daemon=True).start()
threading.Thread(target=tarefa_envio_dois, daemon=True).start()

print(f"Servidor recebendo na porta {PORTA_RECEBE}.")
print(f"Envia média geral para {GRUPO}:{PORTA_ENVIO}")
print(f"Envia média dos 2 últimos valores para {GRUPO}:{PORTA_ENVIO_DOIS}")

while True:
    dados, endereco = recebe.recvfrom(1024)
    try:
        valor = float(dados.decode('utf-8'))
        with lock:
            valores.append(valor)
        print(f"Recebeu {valor:.2f} de {endereco}")
    except ValueError:
        print(f"Valor inválido recebido de {endereco}: {dados}")
