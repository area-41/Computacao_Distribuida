import socket
from threading import Thread

# Configurações do Servidor 02
HOST = '127.0.0.1'
PORTA = 50001  # O Servidor 02 escuta nesta porta

# Lista para armazenar todos os sockets conectados
clientes_conectados = []


def handler_thread(cnx, end):
    print(f'[*] Nova conexão no Servidor 02: {end}')
    clientes_conectados.append(cnx)  # Adiciona o novo cliente à lista

    try:
        while True:
            dados = cnx.recv(1024)
            if not dados:
                break

            mensagem = dados.decode('utf-8')
            print(f"[S2 recebido de {end}]: {mensagem}")

            # FORMATANDO A RESPOSTA PARA TODOS
            resposta = f"Broadcast de {end}: {mensagem}"

            # ENVIANDO PARA TODOS OS CONECTADOS (O segredo do Chat)
            for cliente in clientes_conectados:
                try:
                    cliente.sendall(resposta.encode('utf-8'))
                except:
                    clientes_conectados.remove(cliente)

    except Exception as e:
        print(f"Erro no S2: {e}")
    finally:
        if cnx in clientes_conectados:
            clientes_conectados.remove(cnx)
        cnx.close()
        print(f'[-] Conexão encerrada com {end}')


def Main():
    # Cria o socket para escutar conexões
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PORTA))
        servidor.listen(10)
        print(f"=== SERVIDOR 02 (FINAL) ATIVO NA PORTA {PORTA} ===")
        print("Aguardando mensagens do Servidor 01 ou Cliente 02...")

        while True:
            # Aceita qualquer um que conectar na porta 50001
            conexao, endereco = servidor.accept()
            t = Thread(target=handler_thread, args=(conexao, endereco))
            t.daemon = True
            t.start()

    except Exception as e:
        print(f"Erro fatal no Servidor 02: {e}")
    finally:
        servidor.close()


if __name__ == '__main__':
    Main()