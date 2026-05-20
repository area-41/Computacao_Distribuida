import redis
import time

def iniciar_servidor():
    # Conecta ao container Redis que está rodando na sua máquina
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    pubsub = r.pubsub()
    
    # Se inscreve no canal de comunicação distribuída
    pubsub.subscribe('chat_distribuido')
    print("[SERVIDOR] Aguardando mensagens no canal 'chat_distribuido'...")

    for mensagem in pubsub.listen():
        if mensagem['type'] == 'message':
            print(f"[NOVA MENSAGEM] {mensagem['data']}")

if __name__ == "__main__":
    iniciar_servidor()