import socket
import struct
import threading

GRUPO = "224.1.1.8" # endreco multicast
PORTA = 50000

def receptor(usuario: str):
    # Recebe mensagens multicast
    recebe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recebe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recebe.bind(("", PORTA))

    multicast = struct.pack("4s4s", socket.inet_aton(GRUPO), socket.inet_aton("0.0.0.0"))
    recebe.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast)

    while True:
        dados, _ = recebe.recvfrom(2048)
        msg = dados.decode("utf-8", errors="ignore").strip()
        # ignora as próprias msg enviadas com o ";". Separo o usuário
        remetente, conteudo = msg.split(";", 1)
        if remetente != usuario:
            print(f"\n{remetente} diz: {conteudo}\nDigite a mensagem: ", end="", flush=True)

def main():
    usuario = input("Digite o seu nome: ").strip()
    if not usuario:
        print("Nome vazio não é permitido.")
        return

    # Thread para receber mensagens enquanto o main envia
    threading.Thread(target=receptor, args=(usuario,), daemon=True).start()

    transmite = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Conectado ao grupo {GRUPO}:{PORTA}. Digite 'sair' para encerrar.")

    while True:
        try:
            texto = input("Digite a mensagem: ")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break

        if texto.lower().strip() == "sair":
            break
        # estou enviando o nome do usuário e o texto separados para 
        # identificar quem é o usuário
        pacote = f"{usuario};{texto}".encode("utf-8")
        transmite.sendto(pacote, (GRUPO, PORTA))

if __name__ == "__main__":
    main()
