import tkinter as tk
from tkinter import ttk
import redis
from threading import Thread

class AppDistribuida:
    def __init__(self, root):
        self.root = root
        self.root.title("UTFPR - Computação Distribuída (Redis)")
        self.root.geometry("500x400")
        
        # 🔌 Inicializa a conexão com o Redis local (Docker)
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.canal = 'chat_distribuido'
        
        # 🛠️ Construção da Interface Gráfica (Tkinter/TTK)
        self.setup_ui()
        
        # 🧵 Inicia a Thread em segundo plano para escutar o Redis
        self.thread_ativa = True
        self.thread_escuta = Thread(target=self.escutar_redis, daemon=True)
        self.thread_escuta.start()

    def setup_ui(self):
        # Painel de exibição de mensagens
        self.frame_chat = ttk.Frame(self.root, padding=10)
        self.frame_chat.pack(fill=tk.BOTH, expand=True)
        
        self.txt_mensagens = tk.Text(self.frame_chat, state=tk.DISABLED, height=15)
        self.txt_mensagens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(self.frame_chat, command=self.txt_mensagens.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_mensagens['yscrollcommand'] = scroll.set
        
        # Painel de envio (input e botão)
        self.frame_envio = ttk.Frame(self.root, padding=10)
        self.frame_envio.pack(fill=tk.X)
        
        self.entry_texto = ttk.Entry(self.frame_envio, font=("Arial", 11))
        self.entry_texto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_texto.bind("<Return>", lambda event: self.enviar_mensagem())
        
        self.btn_enviar = ttk.Button(self.frame_envio, text="Enviar", command=self.enviar_mensagem)
        self.btn_enviar.pack(side=tk.RIGHT)

    def enviar_mensagem(self):
        texto = self.entry_texto.get().strip()
        if texto:
            # Publica no canal do Redis
            self.r.publish(self.canal, texto)
            self.entry_texto.delete(0, tk.END)

    def escutar_redis(self):
        """ Roda em segundo plano coletando dados do container """
        pubsub = self.r.pubsub()
        pubsub.subscribe(self.canal)
        
        for msg in pubsub.listen():
            if not self.thread_ativa:
                break
            if msg['type'] == 'message':
                texto_recebido = msg['data']
                # Atualiza o componente visual de forma segura usando o root.after
                self.root.after(0, self.atualizar_chat, texto_recebido)

    def atualizar_chat(self, mensagem):
        self.txt_mensagens.config(state=tk.NORMAL)
        self.txt_mensagens.insert(tk.END, f"• {mensagem}\n")
        self.txt_mensagens.config(state=tk.DISABLED)
        self.txt_mensagens.see(tk.END) # Auto-scroll para a última mensagem

if __name__ == "__main__":
    root = tk.Tk()
    app = AppDistribuida(root)
    root.mainloop()