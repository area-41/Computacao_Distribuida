from tkinter import *
from tkinter import ttk
import socket
from threading import Thread

conexao = None
HOST = '127.0.0.1' 
PORTA = 50000 

def atualizar_text_area(msg):
    text_area.insert(END, msg)
    text_area.see(END)

def escreve_msg(msg):
    text_area.after(0, lambda: atualizar_text_area(msg))

# def thread_receber():
#     # não para a execução da interface
#     global conexao
#     try:
#         while True:
#             dados, end = conexao.recvfrom(2048)   # bloqueante
#             resposta = dados.decode('utf-8', errors='replace')
#             escreve_msg(f"Servidor ({end[0]}:{end[1]}): {resposta}\n")
#     except OSError:
#         # socket fechado em sair()
#         print(f"Ocorreu o erro {OSError}")
#     except Exception as e:
#         escreve_msg(f"Erro de recepção: {e}\n")

def thread_receber():
    global conexao
    print("Thread de recepção iniciada...")
    try:
        while True:
            if conexao:
                dados, end = conexao.recvfrom(2048)
                resposta = dados.decode('utf-8', errors='replace')
                print(f"MSG RECEBIDA: {resposta}") # Isso aparecerá apenas no console do PyCharm
                escreve_msg(f"Servidor ({end[0]}:{end[1]}): {resposta}\n")
    except Exception as e:
        print(f"A thread de recepção parou: {e}")

# def iniciar_cliente_udp():
#     # receber dados
#     global conexao
#     try:
#         conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         escreve_msg(f"Cliente aguardando mensagens...\n")
#         enviar_btn.config(state=NORMAL)
#         # Thread para receber respostas
#         t = Thread(target=thread_receber, daemon=True)
#         t.start()
#     except Exception as e:
#         escreve_msg(f"Erro ao iniciar cliente UDP: {e}\n")
#         try:
#             if conexao:
#                 conexao.close()
#         except:
#             pass

def iniciar_cliente_udp():
    global conexao
    try:
        conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # SOLUÇÃO: Faz um bind para a porta 0.
        # Isso força o SO a atribuir uma porta ao socket IMEDIATAMENTE.
        conexao.bind(('', 0))

        porta_escolhida = conexao.getsockname()[1]
        escreve_msg(f"Cliente pronto na porta local {porta_escolhida}...\n"
                    f"==================================================\n"
                    f"Escreva o nome do ESTADO que deseja consultar à qual região pertence:\n\n")

        enviar_btn.config(state=NORMAL)

        t = Thread(target=thread_receber, daemon=True)
        t.start()
    except Exception as e:
        escreve_msg(f"Erro ao iniciar cliente UDP: {e}\n")

def enviar_mensagem():
    global conexao
    if not conexao:
        escreve_msg("Cliente não inicializado.\n")
        return
    msg = input_text.get("1.0", END).strip()
    if not msg:
        return
    try:
        # Envia datagrama ao servidor
        conexao.sendto(msg.encode('utf-8'), (HOST, PORTA))
        escreve_msg(f"Cliente: {msg}\n")
        input_text.delete("1.0", END)
    except Exception as e:
        escreve_msg(f"Erro ao enviar: {e}\n")

def sair():
    global conexao
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

ttk.Label(formulario, text="Cliente UDP - Consultar Região do IBGE").grid(column=0, row=0, columnspan=3, pady=5)

text_area = Text(formulario, width=60, height=16, wrap=WORD, state=NORMAL)
text_area.grid(column=0, row=1, columnspan=3, pady=5, sticky=(N, S, E, W))
formulario.columnconfigure(0, weight=1)
formulario.rowconfigure(1, weight=1)

ttk.Label(formulario, text="Estado:").grid(column=0, row=2, sticky=W, padx=(0,5))
input_text = Text(formulario, width=48, height=3, wrap=WORD)
input_text.grid(column=0, row=3, columnspan=2, pady=5, sticky=(E, W))

enviar_btn = ttk.Button(formulario, text="Enviar", command=enviar_mensagem, state=DISABLED)
enviar_btn.grid(column=2, row=3, padx=(5,0), sticky=(N, S, E, W))


sair_btn = ttk.Button(formulario, text="Sair", command=sair)
sair_btn.grid(column=2, row=4, pady=5, sticky=W)


escreve_msg(f"Aguardando servidor UDP em {HOST}:{PORTA}...\n")

principal.protocol("WM_DELETE_WINDOW", sair)

# Inicializa o socket UDP do cliente automaticamente
iniciar_cliente_udp()

principal.mainloop()
