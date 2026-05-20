from tkinter import *
from tkinter import ttk
import socket
from threading import Thread
import random
import time
from pathlib import Path


conexao = None
HOST = '127.0.0.1'
PORTA = 50000

laco_ativo = False   # Controle while


def iniciar_cliente_udp():
    global conexao
    try:
        conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # --- CORREÇÃO AQUI: Vínculo explícito para evitar WinError 10022 ---
        conexao.bind(('', 0))
        porta_local = conexao.getsockname()[1]
        escreve_msg(f"Cliente pronto na porta local: {porta_local}\n")
        # -----------------------------------------------------------------

        enviar_btn.config(state=NORMAL)
        laco_btn.config(state=NORMAL)

        # Thread para receber respostas
        t = Thread(target=thread_receber, daemon=True)
        t.start()
    except Exception as e:
        escreve_msg(f"Erro ao iniciar cliente UDP: {e}\n")
        if conexao:
            conexao.close()


def thread_laco_envio():
    global laco_ativo, conexao
    escreve_msg("Enviando estados continuamente...\n")
    while laco_ativo:
        try:
            # Verifica se o socket ainda existe antes de enviar
            if not conexao or conexao._closed:
                break

            estado = escolher_estado()
            if not estado:
                escreve_msg("Arquivo de estados vazio ou não encontrado.\n")
                break

            conexao.sendto(estado.encode('utf-8'), (HOST, PORTA))
            escreve_msg(f"Cliente (Laço): {estado}\n")

        except Exception as e:
            escreve_msg(f"Erro no laço de envio: {e}\n")
            break

        time.sleep(1.0)  # Aumentado para 1s para não sobrecarregar a API do IBGE

    laco_ativo = False
    enviar_btn.after(0, lambda: enviar_btn.config(state=NORMAL))
    laco_btn.after(0, lambda: laco_btn.config(text="Laço", state=NORMAL))
    escreve_msg("Laço encerrado.\n")


def atualizar_text_area(msg):
    text_area.insert(END, msg)
    text_area.see(END)

def escreve_msg(msg):
    text_area.after(0, lambda: atualizar_text_area(msg))

def escolher_estado():
    # Ecolhe estado aleatório
    # Arquivo esperado: s4/ex4/palavras.txt (um estado por linha)
    caminho_arquivo = Path(__file__).resolve().parent / "palavras.txt"
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        estados = arquivo.readlines()
        estados = [estado.strip() for estado in estados if estado.strip()]
        return random.choice(estados) if estados else ""

def thread_receber():
    # situação bloqueante. Aguarda resposta do servidor
    global conexao
    try:
        while True:
            dados, end = conexao.recvfrom(2048)   # bloqueante
            resposta = dados.decode('utf-8', errors='replace')
            escreve_msg(f"Servidor ({end[0]}:{end[1]}): {resposta}\n")
    except OSError:
        # socket fechado em sair()
        pass
    except Exception as e:
        escreve_msg(f"Erro de recepção: {e}\n")


def enviar_mensagem():
    global conexao
    if not conexao:
        escreve_msg("Cliente não inicializado.\n")
        return
    msg = input_text.get("1.0", END).strip()
    if not msg:
        return
    try:
        conexao.sendto(msg.encode('utf-8'), (HOST, PORTA))
        escreve_msg(f"Cliente: {msg}\n")
        input_text.delete("1.0", END)
    except Exception as e:
        escreve_msg(f"Erro ao enviar: {e}\n")


def alternar_laco():
    global laco_ativo
    if not laco_ativo:
        laco_ativo = True
        enviar_btn.config(state=DISABLED)
        laco_btn.config(text="Parar Laço")
        t = Thread(target=thread_laco_envio, daemon=True)
        t.start()
    else:
        laco_ativo = False
        laco_btn.config(state=DISABLED)  # evita múltiplos cliques até encerrar

def sair():
    global conexao, laco_ativo
    laco_ativo = False
    try:
        if conexao:
            conexao.close()
    except:
        pass
    principal.destroy()

principal = Tk()
principal.title("CLIENTE UDP")

formulario = ttk.Frame(principal, padding=10)
formulario.grid(sticky=(N, S, E, W))
principal.columnconfigure(0, weight=1)
principal.rowconfigure(0, weight=1)

ttk.Label(formulario, text="Cliente UDP - Consultar Região do IBGE").grid(column=0, row=0, columnspan=4, pady=5)

text_area = Text(formulario, width=72, height=16, wrap=WORD, state=NORMAL)
text_area.grid(column=0, row=1, columnspan=4, pady=5, sticky=(N, S, E, W))
formulario.columnconfigure(0, weight=1)
formulario.rowconfigure(1, weight=1)

ttk.Label(formulario, text="Estado:").grid(column=0, row=2, sticky=W, padx=(0,5))
input_text = Text(formulario, width=56, height=3, wrap=WORD)
input_text.grid(column=0, row=3, columnspan=2, pady=5, sticky=(E, W))

enviar_btn = ttk.Button(formulario, text="Enviar", command=enviar_mensagem, state=DISABLED)
enviar_btn.grid(column=2, row=3, padx=(5,0), sticky=(N, S, E, W))

laco_btn = ttk.Button(formulario, text="Laço", command=alternar_laco, state=DISABLED)
laco_btn.grid(column=3, row=3, padx=(5,0), sticky=(N, S, E, W))

sair_btn = ttk.Button(formulario, text="Sair", command=sair)
sair_btn.grid(column=3, row=4, pady=5, sticky=E)

escreve_msg(f"Aguardando servidor UDP em {HOST}:{PORTA}...\n")

principal.protocol("WM_DELETE_WINDOW", sair)

# Inicializa o socket UDP do cliente automaticamente
iniciar_cliente_udp()

principal.mainloop()
