import socket
from threading import Thread
from servicoServidor import obter_regiao 

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
            resposta = f"{mensagem} pertence à região {regiao}."
        else:
            resposta = f"Não foi possível encontrar '{mensagem}' no IBGE."

    servidor.sendto(resposta.encode('utf-8'), endereco)
    print(f"Resposta enviada para {endereco}")

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
