import socket

# 1. Criar socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# RECURSO IMPORTANTE: Permite reutilizar a porta imediatamente após fechar o servidor
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = 'localhost'
PORTA = 50000

servidor.bind((HOST, PORTA))
servidor.listen(1)
print(f'Servidor rodando em {HOST}:{PORTA}...')

try:
    while True:  # Loop para manter o servidor vivo
        conexao, endereco = servidor.accept()
        print(f'Conectado por {endereco}')

        try:
            mensagem = conexao.recv(1024).decode('utf-8')
            if not mensagem:
                break

            print(f"Cliente enviou: {mensagem}")

            resposta = f"Servidor recebeu sua mensagem: {mensagem.upper()}"
            conexao.send(resposta.encode('utf-8'))

        finally:
            # Garante que a conexão com o cliente feche, mas o servidor continue
            conexao.close()
            print(f"Conexão com {endereco} encerrada.")

except KeyboardInterrupt:
    print("\nDesligando o servidor...")
finally:
    servidor.close()
