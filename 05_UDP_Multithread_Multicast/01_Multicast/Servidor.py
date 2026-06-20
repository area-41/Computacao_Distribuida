import socket
import time
import random

GRUPO = '224.1.1.7'
PORTA = 50000     # multicast para clientes

transmite = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Servidor enviando multicast em {GRUPO}:{PORTA}")

while True:
    time.sleep(5.0)                
    valor = random.uniform(0,50)
    msg = f"Valor gerado: {valor:.2f}"
    transmite.sendto(msg.encode('utf-8'), (GRUPO, PORTA))
    print("Enviando: ", msg)
