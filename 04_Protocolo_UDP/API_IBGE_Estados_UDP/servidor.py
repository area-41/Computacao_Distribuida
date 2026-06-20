import socket
from threading import Thread
from servico_servidor import obter_regiao

HOST = '127.0.0.1'
PORTA = 50000

# Função que processa o servico
def servidor_thread(dados, endereco, servidor):
    mensagem = dados.decode('utf-8').strip()
    print(f"Recebido de {endereco}: {mensagem}")

    if not mensagem:
        resposta = "Mensagem vazia recebida."
    else:
        regiao = obter_regiao(mensagem)
        if regiao:
            resposta = f"\n{mensagem.capitalize()} pertence à região {regiao.capitalize()}.\n"
        else:
            resposta = f"Não foi possível encontrar '{mensagem}' no IBGE.\n"

    servidor.sendto(resposta.encode('utf-8'), endereco)
    print(f"RESPOSTA: {resposta} \nenviada para {endereco}\n"
          f"==============================================\n")

def Main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORTA))
    print(f"Servidor UDP aguardando em {HOST}:{PORTA}")

    while True:
        dados, endereco = servidor.recvfrom(1024)
        t = Thread(target=servidor_thread, args=(dados, endereco, servidor))
        t.start()

if __name__ == '__main__':
    Main()
