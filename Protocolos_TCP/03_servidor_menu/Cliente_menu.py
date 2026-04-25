import socket

conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao.connect(('localhost', 50000))

# 1. Primeiro, recebe o menu enviado pelo servidor
boas_vindas = conexao.recv(1024).decode('utf-8')
print(boas_vindas)

while True:
    msg = input('Escolha uma opção: ')

    if not msg: continue

    conexao.send(msg.encode('utf-8'))

    if msg.lower() == 'sair':
        print('Encerrando...')
        break

    # 2. Recebe a resposta específica daquela opção
    resposta = conexao.recv(1024).decode('utf-8')
    print(f'>>> {resposta}')

conexao.close()