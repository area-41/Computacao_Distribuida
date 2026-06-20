import socket
from threading import Thread

# Configurações do Servidor 01 (Onde o Cliente 01 se conecta)
HOST_S1 = '127.0.0.1'
PORTA_S1 = 50000

# Configurações do Servidor 02 (Para onde o S1 vai repassar)
HOST_S2 = '127.0.0.1'
PORTA_S2 = 50001


def handler_thread(cnx_cliente, end):
    print(f'[*] Cliente 01 conectado ao Servidor 01: {end}')

    # 1. Tenta conectar ao Servidor 02 ANTES de entrar no loop de mensagens
    try:
        s2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2_socket.connect((HOST_S2, PORTA_S2))
        print(f"[*] Ponte S1 -> S2 estabelecida com sucesso.")
    except Exception as e:
        print(f"[-] Erro ao conectar ao Servidor 02: {e}")
        cnx_cliente.sendall("Erro: Servidor 02 está offline.".encode('utf-8'))
        cnx_cliente.close()
        return

    with cnx_cliente:
        while True:
            try:
                # 2. Recebe a mensagem do Cliente 01
                dados = cnx_cliente.recv(1024)
                if not dados:
                    break

                msg = dados.decode('utf-8')
                print(f'[S1] Recebeu de {end}: {msg}')

                # 3. REPASSA para o Servidor 02 (AQUI ESTÁ A CHAVE)
                print(f'[S1] Enviando para S2 na porta {PORTA_S2}...')
                s2_socket.sendall(dados)

                # 4. ESPERA a resposta que vem do Servidor 02
                resposta_vinda_do_s2 = s2_socket.recv(1024)
                print(f'[S1] S2 respondeu: {resposta_vinda_do_s2.decode("utf-8")}')

                # 5. Só agora envia a resposta final para o Cliente 01
                # (A resposta que o cliente vê é a que veio do S2)
                cnx_cliente.sendall(resposta_vinda_do_s2)

            except Exception as e:
                print(f"[*] Erro no tráfego de dados: {e}")
                break

    print(f'[-] Encerrando conexões para {end}')
    s2_socket.close()


def Main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST_S1, PORTA_S1))
        servidor.listen(10)
        print(f"=== SERVIDOR 01 (PONTE) ATIVO NA PORTA {PORTA_S1} ===")

        while True:
            conexao, endereco = servidor.accept()
            t = Thread(target=handler_thread, args=(conexao, endereco))
            t.daemon = True
            t.start()

    except Exception as e:
        print(f"Erro no servidor 01: {e}")
    finally:
        servidor.close()


if __name__ == '__main__':
    Main()