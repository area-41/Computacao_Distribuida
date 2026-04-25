import socket
import time

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 50000))

print("Conectado! Enviando mensagens a cada 2 segundos...")

try:
    for i in range(5):
        msg = f"Mensagem {i+1}"
        cliente.send(msg.encode('utf-8'))
        print(f"Enviado: {msg} -> {cliente.recv(1024).decode('utf-8')}")
        time.sleep(2)  # Mantém a conexão aberta por 10 segundos no total

finally:
    cliente.close()
    print("Conexão encerrada.")
