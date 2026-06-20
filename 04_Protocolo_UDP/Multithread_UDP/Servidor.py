import socket

# Cria o socket do servidor (IPv4 + UDP)
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define o endereço e porta de escuta
HOST = 'localhost'
PORTA = 50000

# Associa o socket ao endereço
servidor.bind((HOST, PORTA))
print(f"Servidor UDP aguardando em {HOST}:{PORTA}")

while True:
    # Recebe dados e endereço do cliente
    dados, endereco = servidor.recvfrom(1024)
    texto = dados.decode('utf-8')
    valor = int(texto)
    print(f"Recebido de {endereco}: {valor}")

    # Responde ao cliente
    resposta = "mensagem recebida com sucesso"
    servidor.sendto(resposta.encode('utf-8'), endereco)
