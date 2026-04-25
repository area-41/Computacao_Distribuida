import socket

# Configurações do servidor
HOST = 'localhost'
PORTA = 50000

# 1. Criar o socket e conectar
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST, PORTA))
    print("--- Conectado ao Servidor com Logger ---")
    print("Tudo o que você digitar será registrado no log do servidor.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        # 2. Entrada do usuário
        mensagem = input("Comando/Mensagem: ").strip()

        if not mensagem:
            continue

        # 3. Enviar para o servidor
        cliente.send(mensagem.encode('utf-8'))

        if mensagem.lower() == 'sair':
            print("Encerrando conexão...")
            break

        # 4. Receber confirmação do servidor
        resposta = cliente.recv(1024).decode('utf-8')
        print(f"Servidor respondeu: {resposta}")

except ConnectionRefusedError:
    print("Erro: O servidor não está rodando ou a porta está fechada.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    cliente.close()
    print("Conexão fechada.")