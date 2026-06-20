import socket

HOST = "localhost"
PORT = 50000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cli:
    while True:
        estado = input("Digite o nome do estado (<ENTER> para sair): ").strip()
        if not estado:
            break
        cli.sendto(estado.encode("utf-8"), (HOST, PORT))
        resp, _ = cli.recvfrom(2048)
        print("Resposta:", resp.decode("utf-8"))
