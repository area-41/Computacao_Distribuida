import socket

# Criar socket (UDP - IPV4)
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definir a porta e endereco
HOST = 'localhost'
PORTA = 50000

# Associar ao socket
servidor.bind((HOST, PORTA))
print(f'Servidor aguardando conexao em {HOST}:{PORTA}')

while True:
    # Receber dados do cliente
    dados, endereco = servidor.recvfrom(1024)
    mensagem = dados.decode('utf-8')
    print(f'Recebeu do cliente {endereco}: {mensagem}')

    # Responder ao cliente
    resposta = 'mensagem recebido com sucesso'
    servidor.sendto(resposta.encode('utf-8'),endereco)
