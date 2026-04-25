import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 50000))

cliente.send("olá servidor".encode('utf-8'))
resposta = cliente.recv(1024).decode('utf-8')

print(f"Resposta: {resposta}")
cliente.close()