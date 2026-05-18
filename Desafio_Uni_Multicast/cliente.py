import socket
import struct
import json

MCAST_GRP = '127.0.0.1'
#MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
SERVER_UNICAST_PORT = 5008


def main():
    # 1. Cria o socket UDP
    sock_mcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 2. Permite reuso de porta para abrir vários clientes
    sock_mcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Escuta o canal local na porta 5007
    sock_mcast.bind(('127.0.0.1', MCAST_PORT))

    # [Opcional] Pode apagar ou comentar a linha do struct.pack e setsockopt(IP_ADD_MEMBERSHIP)

    # Socket Unicast para responder (permanece igual)
    sock_uni = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("[*] Conectado ao canal do Quiz. Aguardando perguntas...")

    while True:
        data, addr = sock_mcast.recvfrom(4096)
        pacote = json.loads(data.decode('utf-8'))

        if pacote["tipo"] == "PERGUNTA":
            print("\n" + "=" * 40)
            print(f"PERGUNTA: {pacote['texto']}\n")
            for alt in pacote["alternativas"]:
                print(alt)
            print("=" * 40)

            # Captura a resposta do usuário
            escolha = input(f"Sua resposta (Envio automático em {pacote['tempo']}s): ").strip().upper()

            # Envia a resposta via Unicast diretamente para o IP do servidor
            # Usamos o IP do emissor do multicast (addr[0]) e a porta de escuta Unicast do servidor
            if escolha:
                sock_uni.sendto(escolha.encode('utf-8'), (addr[0], SERVER_UNICAST_PORT))
                print("[*] Resposta enviada! Aguardando encerramento do tempo...")

        elif pacote["tipo"] == "RESULTADO":
            print(pacote["texto"])

        elif pacote["tipo"] == "FIM":
            print(f"\n[SISTEMA]: {pacote['texto']}")
            break


if __name__ == "__main__":
    main()