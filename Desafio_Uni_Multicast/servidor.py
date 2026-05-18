import socket
import json
import time
import random
import os
import threading

# Configurações de Rede
MCAST_GRP = '127.0.0.1'  # Direciona a transmissão para o loopback local
MCAST_PORT = 5007
UNICAST_PORT = 5008
TEMPO_RESPOSTA = 10  # X segundos para responder

ARQUIVO_QUESTOES = "questoes.json"


def carregar_questoes():
    if not os.path.exists(ARQUIVO_QUESTOES):
        print(f"[Erro] Arquivo {ARQUIVO_QUESTOES} não encontrado.")
        exit(1)
    with open(ARQUIVO_QUESTOES, 'r', encoding='utf-8') as f:
        questoes = json.load(f)
        random.shuffle(questoes)  # Lista embaralhada, sem repetição
        return questoes


respostas_rodada = {}
coletando_respostas = False


def escutar_respostas_unicast():
    """Thread dedicada a escutar os votos individuais dos clientes via Unicast UDP"""
    global coletando_respostas, respostas_rodada

    sock_uni = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_uni.bind(('0.0.0.0', UNICAST_PORT))

    while True:
        data, addr = sock_uni.recvfrom(1024)
        if coletando_respostas:
            voto = data.decode('utf-8').strip().upper()
            # Registra ou atualiza o voto do cliente (addr)
            respostas_rodada[addr] = voto


def calcular_estatisticas(respostas, alternativa_correta):
    total_votos = len(respostas)
    if total_votos == 0:
        return "Nenhum voto recebido nesta rodada."

    contagem = {}
    acertos = 0

    for voto in respostas.values():
        contagem[voto] = contagem.get(voto, 0) + 1
        if voto == alternativa_correta:
            acertos += 1

    # Monta a string de percentuais
    resultado = "\n=== RESULTADO DA RODADA ===\n"
    for alt, qtd in contagem.items():
        percentual = (qtd / total_votos) * 100
        resultado += f"Alternativa {alt}: {percentual:.1f}% ({qtd} votos)\n"

    perc_acertos = (acertos / total_votos) * 100
    resultado += f"\nTaxa Geral de Acertos: {perc_acertos:.1f}%\n"
    resultado += f"A alternativa correta era: {alternativa_correta}\n"
    return resultado


def main():
    global coletando_respostas, respostas_rodada

    questoes = carregar_questoes()

    # Configuração do Socket Multicast de Envio
    sock_mcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock_mcast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # GARANTA QUE ESTA LINHA ESTÁ ASSIM (Vincula a saída ao Loopback local):
    sock_mcast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton('127.0.0.1'))

    # Inicia a Thread Unicast para receber respostas
    t = threading.Thread(target=escutar_respostas_unicast, daemon=True)
    t.start()

    print(f"[*] Servidor de Quiz Iniciado. {len(questoes)} questões carregadas.")

    for i, q in enumerate(questoes, 1):
        print(f"\n[*] Enviando Questão {i}...")
        respostas_rodada.clear()

        # Formata o pacote da pergunta
        pacote_pergunta = {
            "tipo": "PERGUNTA",
            "texto": q["pergunta"],
            "alternativas": q["alternativas"],
            "tempo": TEMPO_RESPOSTA
        }

        # Envia via Multicast
        sock_mcast.sendto(json.dumps(pacote_pergunta).encode('utf-8'), (MCAST_GRP, MCAST_PORT))

        # Abre a janela de votação
        coletando_respostas = True
        for restante in range(TEMPO_RESPOSTA, 0, -1):
            print(f"Tempo restante para votação: {restante}s...", end="\r")
            time.sleep(1)
        coletando_respostas = False

        # Processa e distribui o resultado via Multicast
        print("\n[*] Computando votos...")
        resultado_txt = calcular_estatisticas(respostas_rodada, q["correta"])

        pacote_resultado = {
            "tipo": "RESULTADO",
            "texto": resultado_txt
        }
        sock_mcast.sendto(json.dumps(pacote_resultado).encode('utf-8'), (MCAST_GRP, MCAST_PORT))

        time.sleep(5)  # Intervalo de 5 segundos entre as questões

    # Fim do Quiz
    fim_pacote = {"tipo": "FIM", "texto": "O Quiz terminou! Obrigado por participar."}
    sock_mcast.sendto(json.dumps(fim_pacote).encode('utf-8'), (MCAST_GRP, MCAST_PORT))
    print("\n[*] Fim do Banco de Questões.")


if __name__ == "__main__":
    main()