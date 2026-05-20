import socket

IP = "127.0.0.1"
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=" * 30)
print("   MENU DE PIADAS UDP   ")
print("=" * 30)
print("Opções:")
print("1 - Pedir piada")
print("2 - Sair")
print("'reiniciar' - Resetar o ciclo")

while True:
    # Captura como texto puro
    escolha = input("\nEscolha uma opção: ").strip().lower()

    if escolha == '2':
        print("Encerrando conexão...")
        break

    if escolha == '1' or escolha == 'reiniciar':
        # Enviamos o comando (seja '1' ou 'reiniciar')
        sock.sendto(escolha.encode('utf-8'), (IP, PORT))

        # Recebe e exibe a resposta
        try:
            sock.settimeout(2.0)  # 2 segundos de limite para resposta
            data, addr = sock.recvfrom(1024)
            print(f"\n{data.decode('utf-8')}")
        except socket.timeout:
            print("\n[Erro]: Servidor não respondeu.")
    else:
        print("\n[!] Entrada inválida. Digite 1, 2 ou 'reiniciar'.")