import socket

# Criar socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Opcional: permite reiniciar o servidor sem erro de "porta em uso"
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Definir endereco e porta
HOST = 'localhost'
PORTA = 50000

# Associar a conexao ao endereco
servidor.bind((HOST, PORTA))

# servidor aguardar conexões
servidor.listen(1)
print(f'Servidor aguardando conexão em {HOST}:{PORTA}...')

# Aceitar conexao e processar pedido do cliente
conexao, endereco = servidor.accept()
print(f'Conectado por {endereco}')

# laço principal de comunicação
while True:
    try:
        # tentar receber dados do cliente
        dados = conexao.recv(1024)

        # Se recv retornar vazio, o cliente fechou a conexão de forma limpa
        if not dados:
            print('Cliente encerrou a conexão de forma limpa...')
            break

        mensagem = dados.decode('utf-8')
        print(f"Cliente enviou: {mensagem}")

        # Se cliente deseja encerrar conexao via comando
        if mensagem.lower() == 'sair':
            print('Comando "sair" recebido. Encerrando servidor...')
            break

        # Processar resposta
        resposta = f"Servidor recebeu sua mensagem: {mensagem.upper()}"
        conexao.send(resposta.encode('utf-8'))

    except ConnectionResetError:
        # Trata o caso do cliente fechar o terminal ou perder a conexão subitamente
        print("Erro: O cliente desconectou forçadamente (conexão resetada).")
        break
    except Exception as e:
        # Trata outros possíveis erros inesperados
        print(f"Ocorreu um erro inesperado: {e}")
        break

# Encerrar recursos
print("Fechando sockets...")
conexao.close()
servidor.close()