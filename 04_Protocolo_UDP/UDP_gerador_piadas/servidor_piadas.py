import socket
import random

# Configurações do Servidor
HOST = "127.0.0.1"
PORT = 5005
BUFFER_SIZE = 1024

# Banco de dados de piadas
PIADAS_MASTER = [
    "Por que o desenvolvedor faliu? Porque não tinha classe.",
    "O que o Python disse para o Java? Você não tem estilo.",
    "Por que o computador foi ao médico? Porque estava com vírus.",
    "O que o bit disse para o byte? Você anda meio cheio ultimamente.",
    "Quantos programadores são necessários para trocar uma lâmpada? Nenhum, é problema de hardware."
]

# Dicionário para rastrear o estado de cada cliente: { (ip, porta): [lista_de_indices_restantes] }
clientes_estado = {}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"Servidor de piadas rodando em {HOST}:{PORT}...")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)

        # Se o cliente não está no dicionário, inicializamos sua lista de piadas aleatoriamente
        if addr not in clientes_estado:
            indices = list(range(len(PIADAS_MASTER)))  # cria uma lista do tamanho da qtd de itens
            random.shuffle(indices)  # mistura os indices
            clientes_estado[addr] = indices

        # Verifica se ainda restam piadas para este cliente
        if clientes_estado[addr]:
            # Remove e retorna o último índice da lista embaralhada
            index_piada = clientes_estado[addr].pop()
            resposta = PIADAS_MASTER[index_piada]
        else:
            resposta = "Acabaram as piadas! Todas já foram exibidas."
            # Opcional: remover o cliente para reiniciar o ciclo no próximo request
            del clientes_estado[addr]

        sock.sendto(resposta.encode('utf-8'), addr)
        print(f"Piada enviada para {addr}. Restantes: {len(clientes_estado.get(addr, []))}")


if __name__ == "__main__":
    main()
