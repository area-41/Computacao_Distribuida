import socket
from threading import Thread

HOST_S1 = '127.0.0.1'
PORTA_S1 = 50000
HOST_S2 = '127.0.0.1'
PORTA_S2 = 50001

# Lista de clientes conectados diretamente ao S1
clientes_locais = []


def escutar_servidor_02(s2_socket):
    """Fica ouvindo o S2 e repassa TUDO para os clientes do S1"""
    while True:
        try:
            dados = s2_socket.recv(1024)
            if not dados:
                print("[-] S2 encerrou a conexão.")
                break

            msg = dados.decode('utf-8')
            print(f"\n[S1 <- S2] {msg}")

            # Repassa a mensagem para todos os clientes que conectaram no S1
            for cliente in clientes_locais[:]:
                try:
                    cliente.sendall(dados)
                except:
                    clientes_locais.remove(cliente)
        except:
            break


def handler_cliente(cnx, end, s2_socket):
    print(f'[*] Cliente {end} entrou no S1.')
    clientes_locais.append(cnx)

    with cnx:
        while True:
            try:
                dados = cnx.recv(1024)
                if not dados:
                    break

                # O S1 não responde o cliente aqui!
                # Ele apenas joga a mensagem para o S2.
                # O S2 fará o broadcast, e a thread 'escutar_servidor_02'
                # entregará a resposta para todos.
                s2_socket.sendall(dados)

            except:
                break

    if cnx in clientes_locais:
        clientes_locais.remove(cnx)
    print(f'[-] Cliente {end} saiu do S1.')


def Main():
    # 1. Conecta ao S2 antes de tudo
    try:
        s2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2_socket.connect((HOST_S2, PORTA_S2))
        print("[+] Conectado ao Servidor 02 com sucesso.")

        # Inicia a thread que ouve o S2 permanentemente
        Thread(target=escutar_servidor_02, args=(s2_socket,), daemon=True).start()
    except Exception as e:
        print(f"[-] Erro ao conectar ao S2: {e}")
        return

    # 2. Configura a escuta para os clientes do S1
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST_S1, PORTA_S1))
    servidor.listen(10)

    print(f"=== S1 PRONTO (Porta {PORTA_S1}) ===")

    while True:
        conexao, endereco = servidor.accept()
        # Passa o s2_socket para que o handler possa enviar mensagens para o hub central
        t = Thread(target=handler_cliente, args=(conexao, endereco, s2_socket))
        t.daemon = True
        t.start()


if __name__ == '__main__':
    Main()