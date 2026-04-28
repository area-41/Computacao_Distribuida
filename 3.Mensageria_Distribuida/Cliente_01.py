from tkinter import *
from tkinter import ttk
import socket
from threading import Thread

conexao = None


def atualizar_text_area(msg):
    text_area.insert(END, msg)
    text_area.see(END)


def escreve_msg(msg):
    text_area.after(0, lambda: atualizar_text_area(msg))


# verifica conexao com servidor
def thread_receber():
    global conexao
    try:
        while True:
            dados = conexao.recv(1024)
            if not dados:
                escreve_msg("Servidor encerrou a conexão.\n")
                conectar_btn.after(0, lambda: conectar_btn.config(state=NORMAL))
                enviar_btn.after(0, lambda: enviar_btn.config(state=DISABLED))
                break
            resposta = dados.decode('utf-8')
            escreve_msg(f"Servidor: {resposta}\n")
    except Exception as e:
        escreve_msg(f"Erro de recepção: {e}\n")
        conectar_btn.after(0, lambda: conectar_btn.config(state=NORMAL))
        enviar_btn.after(0, lambda: enviar_btn.config(state=DISABLED))


# Thread executa e deixa interface gráfica livre
def iniciar_cliente():
    global conexao
    HOST = 'localhost'
    PORT = 50000
    escreve_msg(f"Conectando a {HOST}:{PORT}...\n")
    try:
        conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexao.connect((HOST, PORT))
        escreve_msg("Conexão estabelecida.\n")

        conectar_btn.config(state=DISABLED)
        enviar_btn.config(state=NORMAL)

        t = Thread(target=thread_receber, daemon=True)
        t.start()

    except Exception as e:
        escreve_msg(f"Erro na conexão: {e}\n")
        conectar_btn.config(state=NORMAL)
        enviar_btn.config(state=DISABLED)
        try:
            if conexao:
                conexao.close()
        except:
            pass
        conexao = None


def enviar_mensagem():
    global conexao
    if not conexao:
        escreve_msg("Não conectado.\n")
        return
    msg = input_text.get("1.0", END).strip()  # input)text adiciona /n ao final
    if not msg:
        return  # não envia vazio
    try:
        conexao.sendall(msg.encode('utf-8'))
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
principal.title("CLIENTE TCP")

formulario = ttk.Frame(principal, padding=10)
formulario.grid(sticky=(N, S, E, W))
principal.columnconfigure(0, weight=1)
principal.rowconfigure(0, weight=1)

ttk.Label(formulario, text="Formulário").grid(column=0, row=0, columnspan=3, pady=5)

text_area = Text(formulario, width=60, height=16, wrap=WORD, state=NORMAL)
text_area.grid(column=0, row=1, columnspan=3, pady=5, sticky=(N, S, E, W))
formulario.columnconfigure(0, weight=1)
formulario.rowconfigure(1, weight=1)

ttk.Label(formulario, text="Mensagem:").grid(column=0, row=2, sticky=W, padx=(0, 5))
input_text = Text(formulario, width=48, height=3, wrap=WORD)
input_text.grid(column=0, row=3, columnspan=2, pady=5, sticky=(E, W))

enviar_btn = ttk.Button(formulario, text="Enviar", command=enviar_mensagem, state=DISABLED)
enviar_btn.grid(column=2, row=3, padx=(5, 0), sticky=(N, S, E, W))

conectar_btn = ttk.Button(formulario, text="Conectar",
                          command=lambda: Thread(target=iniciar_cliente, daemon=True).start())
conectar_btn.grid(column=1, row=4, pady=5, sticky=E)

sair_btn = ttk.Button(formulario, text="Sair", command=sair)
sair_btn.grid(column=2, row=4, pady=5, sticky=W)

escreve_msg("Aguardando conexão com servidor...\n")
principal.protocol("WM_DELETE_WINDOW", sair)
principal.mainloop()
