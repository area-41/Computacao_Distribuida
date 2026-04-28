import socket
import threading


def gerenciar_cliente(conexao, endereco):
    """Função que rodará em uma thread separada para cada cliente."""
    print(f'[NOVA CONEXÃO] {endereco} conectado.')

    try:
        while True:
            # Recebe dados do cliente
            dados = conexao.recv(1024)
            if not dados:
                break

            mensagem = dados.decode('utf-8')
            print(f"[{endereco}] enviou: {mensagem}")

            # Processa e responde
            resposta = f"Eco: {mensagem.upper()}"
            conexao.send(resposta.encode('utf-8'))

    except Exception as e:
        print(f"[ERRO] Erro com {endereco}: {e}")
    finally:
        conexao.close()
        print(f"[DESCONECTADO] {endereco} encerrou a conexão.")


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = 'localhost'
    porta = 50000

    servidor.bind((host, porta))
    servidor.listen()
    print(f'[RODANDO] Servidor multithread em {host}:{porta}')

    try:
        while True:
            # O servidor trava aqui até alguém conectar
            conexao, endereco = servidor.accept()

            # Cria uma thread para a nova conexão
            thread = threading.Thread(target=gerenciar_cliente, args=(conexao, endereco))
            # Inicia a thread
            thread.start()

            # Mostra quantas conexões estão ativas (subtraindo a thread principal)
            print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor finalizado.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor()
