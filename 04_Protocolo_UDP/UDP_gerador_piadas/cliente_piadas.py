import socket

IP = "127.0.0.1"
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:  # Pede mais vezes do que o número de piadas
    escolha = int(input("\nQuer uma piada? (1-sim, 2-não): "))
    if escolha == 1:
        # uso de b envia os bytes sem precisar encode
        # só aceita caracteres ASCII básicos
        sock.sendto(b"piada", (IP, PORT))
        #mensagem = "me mande uma piada"
        #sock.sendto(mensagem.encode('utf-8'), (IP, PORT))
        data, addr = sock.recvfrom(1024)
        print(f"\n{data.decode('utf-8')}")
    else:
        break