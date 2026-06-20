import socket

def digita_valor(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print(f"Digite apenas números inteiros.")


HOST = 'localhost'
PORTA = 50000
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

valor = digita_valor('Digite um valor inteiro: ')

# Converte para string e transforme em bytes
mensagem = str(valor).encode('utf-8')
cliente.sendto(mensagem, (HOST, PORTA))
print("Enviado:", valor)
