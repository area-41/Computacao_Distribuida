import socket
from datetime import datetime

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = 'localhost'
PORTA = 50000
servidor.bind((HOST, PORTA))
servidor.listen(1)

print(f'Servidor pronto em {PORTA}...')

conexao, endereco = servidor.accept()
print(f'Conectado por {endereco}')

# 1. Enviar o menu LOGO APÓS a conexão
menu = "\n--- MENU ---\n1. Hora\n2. Nome\n3. Ajuda\n(Ou 'sair')\n"
conexao.send(menu.encode('utf-8'))

while True:
    try:
        dados = conexao.recv(1024)
        if not dados: break

        opcao = dados.decode('utf-8').strip().lower()

        if opcao == 'sair': break

        # 2. Lógica de resposta síncrona
        if opcao in ['1', 'hora']:
            resposta = f"HORA: {datetime.now().strftime('%H:%M:%S')}"
        elif opcao in ['2', 'nome']:
            resposta = "NOME: Servidor de Estudos Python v2.0"
        elif opcao in ['3', 'ajuda']:
            resposta = "COMANDOS: 1 (Hora), 2 (Nome), 3 (Ajuda)"
        else:
            resposta = "Opção inválida!"

        conexao.send(resposta.encode('utf-8'))

    except ConnectionResetError:
        break

conexao.close()
servidor.close()