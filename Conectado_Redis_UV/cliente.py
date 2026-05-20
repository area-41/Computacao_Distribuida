import redis

def enviar_mensagem():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    print("[CLIENTE] Conectado ao cluster local do Redis.")
    while True:
        texto = input("Digite a mensagem para a rede distribuída (ou 'sair'): ")
        if texto.lower() == 'sair':
            break
            
        # Publica a mensagem no canal que o servidor está escutando
        r.publish('chat_distribuido', texto)

if __name__ == "__main__":
    enviar_mensagem()