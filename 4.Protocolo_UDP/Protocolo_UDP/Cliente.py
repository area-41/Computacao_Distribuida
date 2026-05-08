import socket

# Criar o socket (IPV4 e UDP)
conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definir o endereço e a porta do servidor
HOST = 'localhost'
PORTA = 50000

# Mensagem a ser enviada
mensagem = 'Ola servidor'

# Enviar a mensagem ao servidor
conexao.sendto(mensagem.encode('utf-8'),(HOST, PORTA))
print(f'Mensagem enviada para {HOST}:{PORTA}')

# Aguardar a resposta
dados, endereco = conexao.recvfrom(1024)
print(f"Resposta do servidor {endereco}: {dados.decode('utf-8')}")

# Fechar o socket
conexao.close()