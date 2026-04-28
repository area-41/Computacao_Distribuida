import socket

# Estabelecer o socket - IPv4 e TCP
conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Colocar IP e Porta do servidor
HOST = 'localhost'
PORTA = 50000

# Conectar ao servidor
conexao.connect((HOST, PORTA))

# fazer um laço para mensagens ao servidor
print('Conexão estabelecida. Digite "sair" para encerrar.')
while True:
    # Enviar msg ao servidor
    mensagem = input('Digite algo: ')

    if mensagem.lower() == 'sair':
        print('Cliente encerra conexão...')
        break

    conexao.send(mensagem.encode('utf-8'))

    # aguardar resposta
    resposta = conexao.recv(1024).decode('utf-8')
    print(f'Resposta do servidor: {resposta}')

# fechar conexao
conexao.close
