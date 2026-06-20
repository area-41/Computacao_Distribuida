import socket
from datetime import datetime


def salvar_log(mensagem):
    # O modo 'a' (append) adiciona ao final do arquivo sem apagar o anterior
    with open("log_atividades.txt", "a", encoding="utf-8") as arquivo:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        arquivo.write(f"[{timestamp}] {mensagem}\n")


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('localhost', 50000))
servidor.listen(1)

print("Servidor com Logger rodando...")

while True:
    conexao, endereco = servidor.accept()
    log_msg = f"Conexão estabelecida com: {endereco}"
    print(log_msg)
    salvar_log(log_msg)  # Salva a conexão no arquivo

    try:
        while True:
            dados = conexao.recv(1024)
            if not dados: break

            comando = dados.decode('utf-8').strip()
            # Salva o comando recebido no log
            salvar_log(f"Cliente {endereco} solicitou: {comando}")

            resposta = f"Processado: {comando.upper()}"
            conexao.send(resposta.encode('utf-8'))

    except Exception as e:
        salvar_log(f"Erro com {endereco}: {e}")
    finally:
        salvar_log(f"Conexão encerrada com {endereco}")
        conexao.close()
