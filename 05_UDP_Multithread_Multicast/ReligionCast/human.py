import socket
import struct


def iniciar_receptor(ip='224.1.1.1', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', port))

    # Registro no grupo Multicast
    mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Ouvindo mensagens de God em \n{ip}:{port}...\n\n")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            # print(f"\n[Mensagem de {addr[0]}]: {data.decode('utf-8')}")
            print(f"\n{data.decode('utf-8')}\n")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    iniciar_receptor()